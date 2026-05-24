from CompanyProfMetrics import CompanyProfMetrics
from CompanyCashFlowMetrics import CompanyCashFlowMetrics
from DecisionNode import DecisionNode

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


class CompanyRunner:

    # ----------------------------------
    # Utility: safe numeric input
    # ----------------------------------

    def get_float(self, prompt):

        while True:

            try:
                return float(input(prompt))

            except ValueError:
                print("Please enter a valid numeric value.")

    # ----------------------------------
    # Binary search helper
    # ----------------------------------

    def binary_search_position(self, sorted_values, target):

        low = 0
        high = len(sorted_values)

        while low < high:

            mid = (low + high) // 2

            if sorted_values[mid] < target:
                low = mid + 1

            else:
                high = mid

        return low

    # ----------------------------------
    # Revenue ranking
    # ----------------------------------

    def rank_by_revenue(self, peers_df, company_revenue):

        sorted_df = (
            peers_df
            .sort_values(by="Revenue")
            .reset_index(drop=True)
        )

        revenues = (
            sorted_df["Revenue"]
            .dropna()
            .tolist()
        )

        position = self.binary_search_position(
            revenues,
            company_revenue
        )

        left_peer = (
            sorted_df.iloc[position - 1].to_dict()
            if position - 1 >= 0 else None
        )

        right_peer = (
            sorted_df.iloc[position].to_dict()
            if position < len(sorted_df) else None
        )

        return {
            "rank": position + 1,
            "total": len(revenues) + 1,
            "left_peer": left_peer,
            "right_peer": right_peer
        }

    # ----------------------------------
    # Net Income ranking
    # ----------------------------------

    def rank_by_netIncome(self, peers_df, company_netIncome):

        sorted_df = (
            peers_df
            .sort_values(by="Net Income")
            .reset_index(drop=True)
        )

        net_incomes = (
            sorted_df["Net Income"]
            .dropna()
            .tolist()
        )

        position = self.binary_search_position(
            net_incomes,
            company_netIncome
        )

        left_peer = (
            sorted_df.iloc[position - 1].to_dict()
            if position - 1 >= 0 else None
        )

        right_peer = (
            sorted_df.iloc[position].to_dict()
            if position < len(sorted_df) else None
        )

        return {
            "rank": position + 1,
            "total": len(net_incomes) + 1,
            "left_peer": left_peer,
            "right_peer": right_peer
        }

    # ----------------------------------
    # EBITDA ranking
    # ----------------------------------

    def rank_by_ebitda(self, peers_df, company_ebitda):

        sorted_df = (
            peers_df
            .sort_values(by="EBITDA")
            .reset_index(drop=True)
        )

        ebitdas = (
            sorted_df["EBITDA"]
            .dropna()
            .tolist()
        )

        position = self.binary_search_position(
            ebitdas,
            company_ebitda
        )

        left_peer = (
            sorted_df.iloc[position - 1].to_dict()
            if position - 1 >= 0 else None
        )

        right_peer = (
            sorted_df.iloc[position].to_dict()
            if position < len(sorted_df) else None
        )

        return {
            "rank": position + 1,
            "total": len(ebitdas) + 1,
            "left_peer": left_peer,
            "right_peer": right_peer
        }

    # ----------------------------------
    # Decision-tree evaluation
    # ----------------------------------

    def evaluate_tree(self, node, context):

        if node.result is not None:
            return node.result

        if node.condition(context):
            return self.evaluate_tree(node.yes, context)

        return self.evaluate_tree(node.no, context)

    # ----------------------------------
    # Profitability tree
    # ----------------------------------

    def build_profitability_tree(self):

        margin_above = (
            lambda ctx:
            ctx["company_margin"] > ctx["industry_margin"]
        )

        revenue_above = (
            lambda ctx:
            ctx["company_revenue"] > ctx["industry_revenue"]
        )

        ebitda_above = (
            lambda ctx:
            ctx["company_ebitda"] > ctx["industry_ebitda"]
        )

        return DecisionNode(

            condition=margin_above,

            yes=DecisionNode(

                condition=ebitda_above,

                yes=DecisionNode(

                    condition=revenue_above,

                    yes=DecisionNode(
                        result="Industry Leader"
                    ),

                    no=DecisionNode(
                        result="Efficient but Under-Scaled"
                    )
                ),

                no=DecisionNode(
                    result="Margin Strong but Operationally Weak"
                )
            ),

            no=DecisionNode(

                condition=revenue_above,

                yes=DecisionNode(
                    result="Scale Without Efficiency"
                ),

                no=DecisionNode(
                    result="Underperformer"
                )
            )
        )

    # ----------------------------------
    # Explanation layer
    # ----------------------------------

    def explain_classification(self, label):

        explanations = {

            "Industry Leader":
                "Strong operational efficiency and revenue "
                "scale relative to industry peers.",

            "Efficient but Under-Scaled":
                "Strong profitability but smaller revenue "
                "scale than competitors.",

            "Margin Strong but Operationally Weak":
                "Healthy accounting profitability but weaker "
                "EBITDA performance relative to peers.",

            "Scale Without Efficiency":
                "Strong revenue generation but weak "
                "profitability efficiency.",

            "Underperformer":
                "Weak profitability and revenue relative "
                "to industry benchmarks."
        }

        return explanations[label]

    # ----------------------------------
    # Graphing function
    # ----------------------------------

    def graph_industry_metrics(self, peers_df):

        top_companies = (
            peers_df
            .sort_values(by="Revenue", ascending=False)
            .head(10)
        )

        x = top_companies["Security"]

        plt.figure(figsize=(14, 7))

        plt.plot(
            x,
            top_companies["Revenue"],
            label="Revenue"
        )

        plt.plot(
            x,
            top_companies["Net Income"],
            label="Net Income"
        )

        plt.plot(
            x,
            top_companies["EBITDA"],
            label="EBITDA"
        )

        plt.xticks(rotation=45)

        plt.xlabel("Companies")
        plt.ylabel("Financial Metrics")

        plt.title("Industry Competitive Analysis")

        plt.legend()

        plt.tight_layout()

        plt.show()

    # ----------------------------------
    # Main workflow
    # ----------------------------------

    def run(self):

        print("""
Welcome to the Company Performance Analysis Engine.
""")

        # ----------------------------------
        # Load dataset
        # ----------------------------------

        df = pd.read_csv("sample_data.csv")

        df["Revenue"] = None
        df["Net Income"] = None
        df["EBITDA"] = None

        # ----------------------------------
        # Pull Yahoo Finance data
        # ----------------------------------

        print("\nLoading financial dataset...\n")

        for index, row in df.iterrows():

            ticker = row["Symbol"]

            try:

                stock = yf.Ticker(ticker)

                financials = stock.financials
                info = stock.info

                revenue = None
                net_income = None
                ebitda = info.get("ebitda", None)

                if "Total Revenue" in financials.index:
                    revenue = (
                        financials
                        .loc["Total Revenue"]
                        .iloc[0]
                    )

                if "Net Income" in financials.index:
                    net_income = (
                        financials
                        .loc["Net Income"]
                        .iloc[0]
                    )

                df.at[index, "Revenue"] = revenue
                df.at[index, "Net Income"] = net_income
                df.at[index, "EBITDA"] = ebitda

                print(f"Processed {ticker}")

            except Exception as e:

                print(f"Could not process {ticker}: {e}")

        print("\nFinancial dataset loaded.\n")

        # ----------------------------------
        # User inputs
        # ----------------------------------

        name = input("Enter company name: ").strip()

        industry = input(
            "Enter GICS Sector exactly as shown: "
        ).strip()

        if industry not in df["GICS Sector"].unique():

            print("Industry sector not found.")
            return

        company = CompanyProfMetrics(name, industry)

        revenue = self.get_float("Enter Revenue: ")
        cogs = self.get_float("Enter COGS: ")
        sga = self.get_float("Enter SG&A: ")
        marketing = self.get_float("Enter Marketing: ")
        rd = self.get_float("Enter R&D: ")

        company.set_financials(
            revenue,
            cogs,
            sga,
            marketing,
            rd
        )

        company.calculate_profitability()

        depreciation = self.get_float(
            "Enter Depreciation: "
        )

        amortization = self.get_float(
            "Enter Amortization: "
        )

        company.calculate_ebitda(
            depreciation,
            amortization
        )

        # ----------------------------------
        # Peer dataset
        # ----------------------------------

        peers_df = (
            df[df["GICS Sector"] == industry]
        )

        # ----------------------------------
        # Industry averages
        # ----------------------------------

        avg_margin = (
            (
                peers_df["Net Income"] /
                peers_df["Revenue"]
            )
            .dropna()
            .mean()
        )

        avg_revenue = (
            peers_df["Revenue"]
            .dropna()
            .mean()
        )

        avg_ebitda = (
            peers_df["EBITDA"]
            .dropna()
            .mean()
        )

        # ----------------------------------
        # Decision-tree context
        # ----------------------------------

        context = {

            "company_margin":
                company.net_income / company.revenue,

            "industry_margin":
                avg_margin,

            "company_revenue":
                company.revenue,

            "industry_revenue":
                avg_revenue,

            "company_ebitda":
                company.ebitda,

            "industry_ebitda":
                avg_ebitda
        }

        # ----------------------------------
        # Classification
        # ----------------------------------

        tree = self.build_profitability_tree()

        classification = self.evaluate_tree(
            tree,
            context
        )

        print("\n----------------------------------")

        print(company.summary())

        print("\nClassification:")

        print(
            self.explain_classification(
                classification
            )
        )

        # ----------------------------------
        # Revenue ranking
        # ----------------------------------

        ranking1 = self.rank_by_revenue(
            peers_df,
            company.revenue
        )

        print("\nRevenue Ranking:")

        print(
            f"Rank {ranking1['rank']} "
            f"out of {ranking1['total']}"
        )

        # ----------------------------------
        # Net Income ranking
        # ----------------------------------

        ranking2 = self.rank_by_netIncome(
            peers_df,
            company.net_income
        )

        print("\nNet Income Ranking:")

        print(
            f"Rank {ranking2['rank']} "
            f"out of {ranking2['total']}"
        )

        # ----------------------------------
        # EBITDA ranking
        # ----------------------------------

        ranking3 = self.rank_by_ebitda(
            peers_df,
            company.ebitda
        )

        print("\nEBITDA Ranking:")

        print(
            f"Rank {ranking3['rank']} "
            f"out of {ranking3['total']}"
        )

        # ----------------------------------
        # Graph visualization
        # ----------------------------------

        graph_choice = input(
            "\nShow industry graph? (yes/no): "
        ).lower()

        if graph_choice == "yes":

            self.graph_industry_metrics(
                peers_df
            )


if __name__ == "__main__":

    CompanyRunner().run()