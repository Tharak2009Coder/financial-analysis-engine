from CompanyProfMetrics import CompanyProfMetrics
from CompanyCashFlowMetrics import CompanyCashFlowMetrics
from DecisionNode import DecisionNode

import pandas as pd
import yfinance as yf


class Runner:

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
    # Cash flow explanation layer
    # ----------------------------------
    def explain_cash_flow(
        self,
        cash_ctx,
        revenue,
        industry_avg_fcf
    ):

        fcf_margin = (
            cash_ctx["free_cash_flow"] / revenue
        )

        print("\n--- CASH FLOW ANALYSIS ---")

        print(
            f"Operating Cash Flow: "
            f"{cash_ctx['operating_cash_flow']}"
        )

        print(
            f"Free Cash Flow: "
            f"{cash_ctx['free_cash_flow']}"
        )

        print(
            f"Free Cash Flow Margin: "
            f"{fcf_margin:.2%}"
        )

        if cash_ctx["earnings_quality_strong"]:

            print(
                "• Free cash flow closely "
                "tracks earnings."
            )

        else:

            print(
                "• Earnings and cash flow "
                "are diverging."
            )

        if cash_ctx["strong_liquidity"]:

            print("• Strong liquidity position.")

        elif cash_ctx["cash_flow_pressure"]:

            print("• Liquidity pressure detected.")

        else:

            print("• Neutral liquidity profile.")

        if (
            cash_ctx["free_cash_flow"]
            > industry_avg_fcf
        ):

            print(
                "• Cash generation exceeds "
                "industry average."
            )

        else:

            print(
                "• Cash generation trails "
                "industry average."
            )

    # ----------------------------------
    # Binary search helper
    # ----------------------------------
    def binary_search_position(
        self,
        sorted_values,
        target
    ):

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
    def rank_by_revenue(
        self,
        peers_df,
        company_revenue
    ):

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
    # Net income ranking
    # ----------------------------------
    def rank_by_netIncome(
        self,
        peers_df,
        company_netIncome
    ):

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
    def rank_by_ebitda(
        self,
        peers_df,
        company_ebitda
    ):

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
    def evaluate_tree(
        self,
        node,
        context
    ):

        if node.result is not None:

            return node.result

        if node.condition(context):

            return self.evaluate_tree(
                node.yes,
                context
            )

        else:

            return self.evaluate_tree(
                node.no,
                context
            )

    # ----------------------------------
    # Profitability decision tree
    # ----------------------------------
    def build_profitability_tree(self):

        margin_above = (
            lambda ctx:
            ctx["company_margin"]
            > ctx["industry_margin"]
        )

        revenue_above = (
            lambda ctx:
            ctx["company_revenue"]
            > ctx["industry_revenue"]
        )

        ebitda_above = (
            lambda ctx:
            ctx["company_ebitda"]
            > ctx["industry_ebitda"]
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
    def explain_classification(
        self,
        label
    ):

        explanations = {

            "Industry Leader":
                "The company demonstrates strong "
                "operational efficiency and "
                "competitive scale relative to "
                "industry peers.",

            "Efficient but Under-Scaled":
                "The company maintains healthy "
                "profitability margins but operates "
                "at a smaller revenue scale.",

            "Margin Strong but Operationally Weak":
                "The company reports healthy margins "
                "but weaker EBITDA performance "
                "relative to peers.",

            "Scale Without Efficiency":
                "The company generates significant "
                "revenue but exhibits weaker "
                "profitability efficiency.",

            "Underperformer":
                "The company trails peers in both "
                "profitability and scale."
        }

        return explanations[label]

    # ----------------------------------
    # Main workflow
    # ----------------------------------
    def run(self):

        print("""
Welcome to the Company Performance Analysis Engine.

This tool evaluates:
• Profitability
• Peer benchmarking
• Ranking systems
• Decision-tree logic
""")

        # ----------------------------------
        # Load dataset
        # ----------------------------------

        df = pd.read_csv("sample_data.csv")

        df = df.sort_values(by="GICS Sector")

        # ----------------------------------
        # Add financial columns
        # ----------------------------------

        df["Revenue"] = None
        df["Net Income"] = None
        df["EBITDA"] = None

        # Cash flow metrics
        df["Working Capital"] = None
        df["Operating Cash Flow"] = None
        df["Free Cash Flow"] = None

        # ----------------------------------
        # Pull Yahoo Finance metrics
        # ----------------------------------

        print("\nLoading company financial data...\n")

        for index, row in df.iterrows():

            ticker = row["Symbol"]

            try:

                stock = yf.Ticker(ticker)

                financials = stock.financials
                cashflow = stock.cashflow
                balance_sheet = stock.balance_sheet
                info = stock.info

                revenue = None
                net_income = None
                ebitda = None

                working_capital = None
                operating_cash_flow = None
                free_cash_flow = None

                # ------------------------------
                # Revenue
                # ------------------------------

                if "Total Revenue" in financials.index:

                    revenue = (
                        financials
                        .loc["Total Revenue"]
                        .iloc[0]
                    )

                # ------------------------------
                # Net Income
                # ------------------------------

                if "Net Income" in financials.index:

                    net_income = (
                        financials
                        .loc["Net Income"]
                        .iloc[0]
                    )

                # ------------------------------
                # EBITDA
                # ------------------------------

                ebitda = info.get(
                    "ebitda",
                    None
                )

                # ------------------------------
                # Operating Cash Flow
                # ------------------------------

                if (
                    "Operating Cash Flow"
                    in cashflow.index
                ):

                    operating_cash_flow = (
                        cashflow
                        .loc["Operating Cash Flow"]
                        .iloc[0]
                    )

                # ------------------------------
                # Free Cash Flow
                # ------------------------------

                if (
                    "Operating Cash Flow"
                    in cashflow.index
                    and
                    "Capital Expenditure"
                    in cashflow.index
                ):

                    ocf = (
                        cashflow
                        .loc["Operating Cash Flow"]
                        .iloc[0]
                    )

                    capex = (
                        cashflow
                        .loc["Capital Expenditure"]
                        .iloc[0]
                    )

                    free_cash_flow = (
                        ocf - abs(capex)
                    )

                # ------------------------------
                # Working Capital
                # ------------------------------

                if (
                    "Current Assets"
                    in balance_sheet.index
                    and
                    "Current Liabilities"
                    in balance_sheet.index
                ):

                    current_assets = (
                        balance_sheet
                        .loc["Current Assets"]
                        .iloc[0]
                    )

                    current_liabilities = (
                        balance_sheet
                        .loc["Current Liabilities"]
                        .iloc[0]
                    )

                    working_capital = (
                        current_assets
                        - current_liabilities
                    )

                # ------------------------------
                # Store metrics
                # ------------------------------

                df.at[index, "Revenue"] = revenue

                df.at[index, "Net Income"] = net_income

                df.at[index, "EBITDA"] = ebitda

                df.at[index, "Working Capital"] = (
                    working_capital
                )

                df.at[index, "Operating Cash Flow"] = (
                    operating_cash_flow
                )

                df.at[index, "Free Cash Flow"] = (
                    free_cash_flow
                )

                print(f"Processed {ticker}")

            except Exception as e:

                print(
                    f"Could not process "
                    f"{ticker}: {e}"
                )

        print("\nFinancial dataset loaded.\n")

        # ----------------------------------
        # Save enriched dataset
        # ----------------------------------

        df.to_csv(
            "sample_data.csv",
            index=False
        )

        # ----------------------------------
        # User inputs
        # ----------------------------------

        name = input(
            "Enter company name: "
        ).strip()

        industry = input(
            "Enter GICS Sector exactly "
            "as shown in dataset: "
        ).strip()

        if (
            industry
            not in df["GICS Sector"].unique()
        ):

            print("Industry sector not found.")

            return

        company = CompanyProfMetrics(
            name,
            industry
        )

        # ----------------------------------
        # Profitability inputs
        # ----------------------------------

        revenue = self.get_float(
            "Enter Net Revenue: "
        )

        cogs = self.get_float(
            "Enter COGS: "
        )

        sga = self.get_float(
            "Enter SG&A: "
        )

        marketing = self.get_float(
            "Enter Marketing: "
        )

        rd = self.get_float(
            "Enter R&D: "
        )

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
        # Industry peer dataset
        # ----------------------------------

        peers_df = (
            df[
                df["GICS Sector"]
                == industry
            ]
        )

        # ----------------------------------
        # Industry averages
        # ----------------------------------

        avg_margin = (
            (
                peers_df["Net Income"]
                /
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

        avg_fcf = (
            peers_df["Free Cash Flow"]
            .dropna()
            .mean()
        )

        # ----------------------------------
        # Decision tree context
        # ----------------------------------

        context = {

            "company_margin":
                company.net_income
                / company.revenue,

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
        # Decision tree
        # ----------------------------------

        tree = self.build_profitability_tree()

        classification = self.evaluate_tree(
            tree,
            context
        )

        print("\n----------------------------------")

        print(company.summary())

        print("\nProfitability Classification:")

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
            f"out of {ranking1['total']} "
            f"companies in {industry}."
        )

        # ----------------------------------
        # Net income ranking
        # ----------------------------------

        ranking2 = self.rank_by_netIncome(
            peers_df,
            company.net_income
        )

        print("\nNet Income Ranking:")

        print(
            f"Rank {ranking2['rank']} "
            f"out of {ranking2['total']} "
            f"companies in {industry}."
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
            f"out of {ranking3['total']} "
            f"companies in {industry}."
        )

        # ----------------------------------
        # Cash flow analysis
        # ----------------------------------

        print("""
Now the program will evaluate
cash flow metrics.
""")

        cash = CompanyCashFlowMetrics(
            company.net_income
        )

        current_assets = self.get_float(
            "Enter Current Assets: "
        )

        liabilities = self.get_float(
            "Enter Current Liabilities: "
        )

        non_cash = self.get_float(
            "Enter Non-Cash Expenses: "
        )

        change_wc = self.get_float(
            "Enter Change in Working Capital: "
        )

        capex = self.get_float(
            "Enter Capital Expenditures: "
        )

        cash.set_financials(
            current_assets,
            liabilities,
            non_cash,
            change_wc,
            capex
        )

        cash_ctx = cash.get_context()

        self.explain_cash_flow(
            cash_ctx,
            revenue,
            avg_fcf
        )


if __name__ == "__main__":

    CompanyRunner().run()
    
