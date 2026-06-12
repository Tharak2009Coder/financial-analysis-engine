from CompanyProfMetrics import CompanyProfMetrics
from CompanyCashFlowMetrics import CompanyCashFlowMetrics
from DecisionNode import DecisionNode
from CashFlowAnalyzer import CashFlowAnalyzer
from RecommendationEngine import RecommendationEngine
from RankingEngine import RankingEngine

import pandas as pd
import yfinance as yf
import os


class Runner:

    def load_dataset(self):

        if os.path.exists("updated_financial_dataset.csv"):

            print("Loading cached dataset...")

            return pd.read_csv(
                "updated_financial_dataset.csv"
            )

        print("Building financial dataset...")

        df = pd.read_csv(
            "financial_dataset.csv"
        )

        df.to_csv(
            "updated_financial_dataset.csv",
            index=False
        )

        return df
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
    # Decision-tree evaluation
    # ----------------------------------

    """
    In the evaluate_tree method, you have to ensure that the node
    """
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
                "The company demonstrates strong revenue scale, "
                "profitability, and operational efficiency relative "
                "to industry peers. Its financial positioning suggests "
                "competitive advantages, efficient cost management, "
                "and strong earnings potential.",

            "Efficient but Under-Scaled":
                "The company maintains healthy profitability and "
                "operational discipline but operates at a smaller "
                "revenue scale compared to larger industry competitors. "
                "This may indicate future growth potential if scale expands.",

            "Margin Strong but Operationally Weak":
                "The company reports solid profitability margins but "
                "weaker EBITDA performance relative to peers, suggesting "
                "that operational cash generation and core operating "
                "efficiency may require improvement.",

            "Scale Without Efficiency":
                "The company generates significant revenue relative "
                "to competitors but exhibits weaker profitability "
                "and operational efficiency. This may indicate margin "
                "pressure, elevated costs, or inefficient resource allocation.",

            "Underperformer":
                "The company trails industry peers across revenue, "
                "profitability, and operational performance metrics. "
                "This may reflect weaker market positioning, limited "
                "scale advantages, or operational inefficiencies."
        }

        return explanations[label]

    # ----------------------------------
    # Main workflow
    # ----------------------------------
    def run(self):
        # ----------------------------------
        # Load dataset
        # ----------------------------------

        df = self.load_dataset()

        df = df.sort_values(by="GICS Sector")

        if "Revenue" in df.columns:

            print(
                "Financial metrics already loaded."
            )

        else:

    # Yahoo Finance loop

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
                    info = stock.fast_info

                    net_income = None
                    ebitda = None

                    working_capital = None
                    operating_cash_flow = None
                    free_cash_flow = None

                    # ------------------------------
                    # Revenue
                    # ------------------------------
                    ticker_revenue = None
                    if (
                        "Total Revenue" in financials.index and not financials.loc["Total Revenue"].dropna().empty
                    ):

                        ticker_revenue = (
                            financials
                            .loc["Total Revenue"]
                            .iloc[0]
                        )

                    # ------------------------------
                    # Net Income
                    # ------------------------------

                    if "Net Income" in financials.index and not financials.loc["Net Income"].dropna().empty:

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
                        in cashflow.index and not cashflow.loc["Operating Cash Flow"].dropna().empty
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
                        in balance_sheet.index and not cashflow.loc["Current Assets"].dropna().empty
                        and "Current Liabilities"
                        in balance_sheet.index and not cashflow.loc["Current Liabilities"].dropna().empty
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
                    print(ticker, ticker_revenue)
                    df.at[index, "Revenue"] = ticker_revenue
                
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
        print(df[["Symbol", "Revenue"]].head(20))
        df.to_csv(
            "updated_financial_dataset.csv",
            index=False
        )

        # ----------------------------------
        # User inputs
        # ----------------------------------
        print("""
Welcome to the Financial Performance Analysis Engine.

This project was developed to evaluate a company's financial performance by combining financial 
statement analysis, industry benchmarking, ranking algorithms, and decision-tree 
classification techniques.

Using a dataset of S&P 500 companies and financial data retrieved through the Yahoo Finance API, the 
engine compares a company's performance against industry peers across several key metrics, including:

• Revenue
• Net Income
• EBITDA
• Working Capital
• Operating Cash Flow
• Free Cash Flow

The program provides:

• Profitability Analysis
• Industry Benchmarking
• Revenue, Net Income, and EBITDA Rankings
• Cash Flow & Liquidity Evaluation
• Decision-Tree Based Performance Classification
• Peer-to-Peer Competitive Comparisons

Rather than simply calculating financial metrics, the engine interprets company performance relative 
to industry averages and neighboring competitors, helping users identify operational strengths, 
profitability trends, and potential areas for improvement.
""")
        name = input(
            "Enter company name: "
        ).strip()

        print("\nAvailable GICS Sectors:\n")

        for sector in sorted(df["GICS Sector"].unique()):
            print(f"- {sector}")

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

        rankingEngine = RankingEngine()

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

        margins = peers_df["Net Income"] / peers_df["Revenue"]

        margins = margins.replace(
            [float("inf"), float("-inf")],
            pd.NA
        )

        avg_margin = margins.dropna().mean()

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

        avg_workingCapital = (
            peers_df["Working Capital"]
            .dropna()
            .mean()
        )
        avg_operatingCF = (
            peers_df["Operating Cash Flow"]
            .dropna()
            .mean()
        )

        # ----------------------------------
        # Decision tree context
        # ----------------------------------

        company_margin = (
            company.net_income / company.revenue
            if company.revenue
            else 0.0
        )

        context = {
            "company_margin": company_margin,
            "industry_margin": avg_margin,
            "company_revenue": company.revenue,
            "industry_revenue": avg_revenue,
            "company_ebitda": company.ebitda,
            "industry_ebitda": avg_ebitda,
            "industry_workingCapital": avg_workingCapital,
            "industry_operatingCF": avg_operatingCF
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

        ranking1 = rankingEngine.rank_by_revenue(peers_df, company.revenue)

        print("\nRevenue Ranking:")

        print(
            f"Rank {ranking1['rank']}"
            f" out of {ranking1['total']} companies."
        )

        if ranking1["rank"] == ranking1["total"]:
            print("""
                The company ranks in the bottom of the """, industry, """ sector by Revenue.
                This conveys that the company has not been making significant sales and profits compared 
                to other companies in the same industry.""")
        elif ranking1["rank"] == 1:
            print(""" 
                The company ranks in the top of the """, industry, """ sector by Revenue. """
                , name, """ has the highest revenue compared to other companies found in the S&P 500 financial
                dataset. This conveys that company has been implementing strategic decisions like acquisitions, investments,
                or sales strategy that led to higher profit margin over industry's competitors.""")

        if ranking1["left_peer"] is not None:

            print(
                f"\nClosest company with LOWER revenue:"
                f" {ranking1['left_peer']['Security']}"
            )

            print(
                f"Revenue: "
                f"{ranking1['left_peer']['Revenue']}"
            )

        if ranking1["right_peer"] is not None:

            print(
                f"\nClosest company with HIGHER revenue:"
                f" {ranking1['right_peer']['Security']}"
            )

            print(
                f"Revenue: "
                f"{ranking1['right_peer']['Revenue']}"
            )

        # ----------------------------------
        # Net income ranking
        # ----------------------------------

        ranking2 = rankingEngine.rank_by_netIncome(
            peers_df,
            company.net_income
        )

        print("\nNet Income Ranking")

        print(
            f"Rank {ranking2['rank']}"
            f" out of {ranking2['total']} companies"
        )
        
        if ranking2["rank"] == ranking2["total"]:
            print("""
                The company ranks in the bottom of the """, industry, """ sector by Net Income.
                This suggests that there is an overall decreased profitability for your organization compared
                to the S&P 500 organizations. """, name, """ would need to decrease annual expenses, expenditure
                , and increase sales per product/service.""")
        elif ranking2["rank"] == 1:
            print(""" 
                The company ranks in the top of the """, industry, """ sector by Net Income.
                This suggests that the operational efficiency of the business is the highest compared to the companies
                as part of the S&P 500.""")
        if ranking2["left_peer"] is not None:

            print(
                f"\nClosest company with LOWER Net Income:"
                f" {ranking2['left_peer']['Security']}"
            )

            print(
                f"Net Income: "
                f"{ranking2['left_peer']['Net Income']}"
            )

        if ranking2["right_peer"] is not None:

            print(
                f"\nClosest company with HIGHER Net Income:"
                f" {ranking2['right_peer']['Security']}"
            )

            print(
                f"Net Income: "
                f"{ranking2['right_peer']['Net Income']}"
            )

        # ----------------------------------
        # EBITDA ranking
        # ----------------------------------

        ranking3 = rankingEngine.rank_by_ebitda(
            peers_df,
            company.ebitda
        )

        print("\nEBITDA Ranking:")
        print(
            f"Rank {ranking3['rank']}"
            f" out of {ranking3['total']} companies"
        )
        if ranking3["rank"] == ranking3["total"]:
            print("""
                The company ranks in the bottom of the """, industry, """ sector by EBITDA.
                This suggests that the operational efficiency of the business is lower compared to the companies
                as part of the S&P 500. 
                    """)
        elif ranking3["rank"] == 1:
            print(""" 
                The company ranks in the top of the """, industry, """ sector by EBITDA.
                This suggests that the operational efficiency of the business is the highest compared to the companies
                as part of the S&P 500.""")
        if ranking3["left_peer"] is not None:
            print(
                f"\nClosest company with LOWER EBITDA:"
                f" {ranking3['left_peer']['Security']}"
            )

            print(
                f"EBITDA: "
                f"{ranking3['left_peer']['EBITDA']}"
            )

        if ranking3["right_peer"] is not None:

            print(
                f"\nClosest company with HIGHER EBITDA:"
                f" {ranking3['right_peer']['Security']}"
            )

            print(
                f"EBITDA: "
                f"{ranking3['right_peer']['EBITDA']}"
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

        cash_ctx = cash.get_context(revenue, avg_fcf, avg_workingCapital, avg_operatingCF )

        cashAnalyzer = CashFlowAnalyzer()
        cashAnalyzer.explain_cash_flow(cash_ctx)

        recEngine = RecommendationEngine()
        recommendations = recEngine.build_recommendations(ranking1, ranking2, ranking3, cash_ctx)
        for rec in recommendations:
            print(f"•{rec}")
        
if __name__ == "__main__":
    Runner().run()