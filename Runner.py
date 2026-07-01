from CompanyProfMetrics import CompanyProfMetrics
from CompanyCashFlowMetrics import CompanyCashFlowMetrics
from DecisionNode import DecisionNode
from CashFlowAnalyzer import CashFlowAnalyzer
from RecommendationEngine import RecommendationEngine
from RankingEngine import RankingEngine

import os

import pandas as pd
import yfinance as yf


class Runner:

    REQUIRED_METRIC_COLUMNS = [
        "Revenue",
        "Net Income",
        "EBITDA",
        "Working Capital",
        "Operating Cash Flow",
        "Free Cash Flow",
    ]

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

    def dataset_has_metrics(self, df):

        return all(
            column in df.columns
            for column in self.REQUIRED_METRIC_COLUMNS
        )

    def ensure_financial_metrics(self, df):

        if self.dataset_has_metrics(df):

            print("Financial metrics already loaded.")

            return df

        print("\nLoading company financial data...\n")

        for index, row in df.iterrows():

            ticker = row["Symbol"]

            try:

                stock = yf.Ticker(ticker)

                financials = stock.financials
                cashflow = stock.cashflow
                balance_sheet = stock.balance_sheet
                info = stock.fast_info

                ticker_revenue = None
                net_income = None
                ebitda = None
                working_capital = None
                operating_cash_flow = None
                free_cash_flow = None

                if (
                    "Total Revenue" in financials.index
                    and not financials.loc["Total Revenue"].dropna().empty
                ):

                    ticker_revenue = (
                        financials
                        .loc["Total Revenue"]
                        .dropna()
                        .iloc[0]
                    )

                if (
                    "Net Income" in financials.index
                    and not financials.loc["Net Income"].dropna().empty
                ):

                    net_income = (
                        financials
                        .loc["Net Income"]
                        .dropna()
                        .iloc[0]
                    )

                ebitda = info.get(
                    "ebitda",
                    None
                )

                if (
                    "Operating Cash Flow" in cashflow.index
                    and not cashflow.loc["Operating Cash Flow"].dropna().empty
                ):

                    operating_cash_flow = (
                        cashflow
                        .loc["Operating Cash Flow"]
                        .dropna()
                        .iloc[0]
                    )

                if (
                    "Operating Cash Flow" in cashflow.index
                    and "Capital Expenditure" in cashflow.index
                    and not cashflow.loc["Operating Cash Flow"].dropna().empty
                    and not cashflow.loc["Capital Expenditure"].dropna().empty
                ):

                    ocf = (
                        cashflow
                        .loc["Operating Cash Flow"]
                        .dropna()
                        .iloc[0]
                    )

                    capex = (
                        cashflow
                        .loc["Capital Expenditure"]
                        .dropna()
                        .iloc[0]
                    )

                    free_cash_flow = (
                        ocf - abs(capex)
                    )

                if (
                    "Current Assets" in balance_sheet.index
                    and "Current Liabilities" in balance_sheet.index
                    and not balance_sheet.loc["Current Assets"].dropna().empty
                    and not balance_sheet.loc["Current Liabilities"].dropna().empty
                ):

                    current_assets = (
                        balance_sheet
                        .loc["Current Assets"]
                        .dropna()
                        .iloc[0]
                    )

                    current_liabilities = (
                        balance_sheet
                        .loc["Current Liabilities"]
                        .dropna()
                        .iloc[0]
                    )

                    working_capital = (
                        current_assets
                        - current_liabilities
                    )

                df.at[index, "Revenue"] = ticker_revenue
                df.at[index, "Net Income"] = net_income
                df.at[index, "EBITDA"] = ebitda
                df.at[index, "Working Capital"] = working_capital
                df.at[index, "Operating Cash Flow"] = operating_cash_flow
                df.at[index, "Free Cash Flow"] = free_cash_flow

                print(f"Processed {ticker}")

            except Exception as error:

                print(
                    f"Could not process "
                    f"{ticker}: {error}"
                )

        df.to_csv(
            "updated_financial_dataset.csv",
            index=False
        )

        print("\nFinancial dataset loaded.\n")

        return df

    def get_float(self, prompt):

        while True:

            try:
                return float(input(prompt))

            except ValueError:
                return{
                    "Please enter a valid numeric value."
                }

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

        return self.evaluate_tree(
            node.no,
            context
        )

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

    def explain_classification(
        self,
        label
    ):

        explanations = {
            "Industry Leader":
                "Industry Leader: "
                "The company demonstrates strong revenue scale, "
                "profitability, and operational efficiency relative "
                "to industry peers. Its financial positioning suggests "
                "competitive advantages, efficient cost management, "
                "and strong earnings potential.",

            "Efficient but Under-Scaled":
                "Efficient but Under-Scaled: "
                "The company maintains healthy profitability and "
                "operational discipline but operates at a smaller "
                "revenue scale compared to larger industry competitors. "
                "This may indicate future growth potential if scale expands.",

            "Margin Strong but Operationally Weak":
                "Margin Strong but Operationally Weak: "
                "The company reports solid profitability margins but "
                "weaker EBITDA performance relative to peers, suggesting "
                "that operational cash generation and core operating "
                "efficiency may require improvement.",

            "Scale Without Efficiency":
                "Scale Without Efficiency: "
                "The company generates significant revenue relative "
                "to competitors but exhibits weaker profitability "
                "and operational efficiency. This may indicate margin "
                "pressure, elevated costs, or inefficient resource allocation.",

            "Underperformer":
                "Underperformer: "
                "The company trails industry peers across revenue, "
                "profitability, and operational performance metrics. "
                "This may reflect weaker market positioning, limited "
                "scale advantages, or operational inefficiencies."
        }

        return explanations[label]

    def analyze_company(
        self,
        name,
        industry,
        revenue,
        cogs,
        sga,
        marketing,
        rd,
        depreciation,
        amortization,
        current_assets,
        liabilities,
        non_cash,
        change_wc,
        capex,
        df=None
    ):

        if df is None:

            df = self.load_dataset()
            df = self.ensure_financial_metrics(df)

        df = df.sort_values(by="GICS Sector")

        company = CompanyProfMetrics(
            name,
            industry
        )

        company.set_financials(
            revenue,
            cogs,
            sga,
            marketing,
            rd
        )

        company.calculate_profitability()

        company.calculate_ebitda(
            depreciation,
            amortization
        )

        peers_df = (
            df[
                df["GICS Sector"]
                == industry
            ]
        )

        if peers_df.empty:

            available_sectors = ", ".join(
                sorted(df["GICS Sector"].dropna().unique())
            )

            raise ValueError(
                f"No peer companies found for '{industry}'. "
                f"Available sectors: {available_sectors}"
            )

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

        avg_working_capital = (
            peers_df["Working Capital"]
            .dropna()
            .mean()
        )

        avg_operating_cf = (
            peers_df["Operating Cash Flow"]
            .dropna()
            .mean()
        )

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
            "industry_workingCapital": avg_working_capital,
            "industry_operatingCF": avg_operating_cf
        }

        tree = self.build_profitability_tree()
        classification = self.evaluate_tree(
            tree,
            context
        )

        cash = CompanyCashFlowMetrics(
            company.net_income
        )

        cash.set_financials(
            current_assets,
            liabilities,
            non_cash,
            change_wc,
            capex
        )
        
        summary = company.summary()

        titleProf = f"\nProfitability Classification:"
        classification =  self.explain_classification(
                classification
            )
        

        ranking_engine = RankingEngine()

        ranking1 = ranking_engine.rank_by_revenue(
            peers_df,
            company.revenue
        )
        revTitle = ""
        revRank = ""
        revExplanation = ""

        revLeftPeerTitle = ""
        revLeftPeerRevenue = ""

        revRightPeerTitle = ""
        revRightPeerRevenue = ""

        revTitle = f"\nRevenue Ranking:"
        
        revRank = (
            f"Rank {ranking1['rank']}"
            f" out of {ranking1['total']} companies."
        )

        if ranking1["rank"] == 1:

            revExplanation = f"{name} ranks at the bottom of the {industry} "
            "sector by revenue."
            
        elif ranking1["rank"] == ranking1["total"]:

            revExplanation = f"{name} ranks at the top of the {industry} "
            "sector by revenue."
            

        if ranking1["left_peer"] is not None:

            revLeftPeerTitle = (
                f"\nClosest company with LOWER revenue:"
                f" {ranking1['left_peer']['Security']}"
            )
        
        
            revLeftPeerRevenue = (
                f"Revenue: "
                f"{ranking1['left_peer']['Revenue']}"
            )

        if ranking1["right_peer"] is not None:

            revRightPeerTitle = (
                f"\nClosest company with HIGHER revenue:"
                f" {ranking1['right_peer']['Security']}"
            )
        
            revRightPeerRevenue = (
                f"Revenue: "
                f"{ranking1['right_peer']['Revenue']}"
            )

        ranking2 = ranking_engine.rank_by_netIncome(
            peers_df,
            company.net_income
        )

        nITitle = ""
        nIRank = ""
        nIExplanation = ""

        nILeftPeerTitle = ""
        nILeftPeerNetIncome = ""

        nIRightPeerTitle = ""
        nIRightPeerNetIncome = ""

        nITitle = f"\nNet Income Ranking:"
        
        nIRank = (
            f"Rank {ranking2['rank']}"
            f" out of {ranking2['total']} companies"
        )
        
        if ranking2["rank"] == 1:

            
            nIExplanation = (
                f"{name} ranks at the bottom of the {industry} "
                "sector by net income."
            )

        elif ranking2["rank"] == ranking2["total"]:

            nIExplanation = (
                f"{name} ranks at the top of the {industry} "
                f"sector by net income."
            )

        if ranking2["left_peer"] is not None:

            
            nILeftPeerTitle = (
                f"\nClosest company with LOWER Net Income:"
                f" {ranking2['left_peer']['Security']}"
            )
        
        
            nILeftPeerNetIncome = (
                f"Net Income: "
                f"{ranking2['left_peer']['Net Income']}"
            )
            

        if ranking2["right_peer"] is not None:

            
            nIRightPeerTitle = (
                f"\nClosest company with HIGHER Net Income:"
                f" {ranking2['right_peer']['Security']}"
            )
        
        
            nIRightPeerNetIncome = (
                f"Net Income: "
                f"{ranking2['right_peer']['Net Income']}"
            )
            

        ranking3 = ranking_engine.rank_by_ebitda(
            peers_df,
            company.ebitda
        )

        ebTitle = ""
        ebRank = ""
        ebExplanation = ""

        ebLeftPeerTitle = ""
        ebLeftPeerEBITDA = ""

        ebRightPeerTitle = ""
        ebRightPeerEBITDA = ""

        ebTitle = f"\nEBITDA Ranking:"
        
        ebRank = (
            f"Rank {ranking3['rank']}"
            f" out of {ranking3['total']} companies"
        )

        if ranking3["rank"] == 1:

            
            ebExplanation = (
                f"{name} ranks at the bottom of the {industry} "
                f"sector by EBITDA."
            )

        elif ranking3["rank"] == ranking3["total"]:

            
            ebExplanation = (
                f"{name} ranks at the top of the {industry} "
                f"sector by EBITDA."
            )

        if ranking3["left_peer"] is not None:
            ebLeftPeerTitle = (
                f"\nClosest company with LOWER EBITDA:"
                f" {ranking3['left_peer']['Security']}"
            )
        
            ebLeftPeerEBITDA = (
                f"EBITDA: "
                f"{ranking3['left_peer']['EBITDA']}"
            )

        if ranking3["right_peer"] is not None:
            ebRightPeerTitle = (
                f"\nClosest company with HIGHER EBITDA:"
                f" {ranking3['right_peer']['Security']}"
            )
        
            ebRightPeerEBITDA = (
                f"EBITDA: "
                f"{ranking3['right_peer']['EBITDA']}"
            )

        cash_ctx = cash.get_context(
            revenue,
            avg_fcf,
            avg_working_capital,
            avg_operating_cf
        )

        

        cash_analyzer = CashFlowAnalyzer()
        cash_analyzer.explain_cash_flow(cash_ctx)

        rec_engine = RecommendationEngine()
        recommendations = rec_engine.build_recommendations(
            ranking1,
            ranking2,
            ranking3,
            cash_ctx
        )

        return {
            "company": name,
            "industry": industry,
            "classification": classification,
            "summary": summary,
            "revenue":
            {
                "title": revTitle,
                "rank": revRank,
                "explanation": revExplanation,
                "lpTitle": revLeftPeerTitle,
                "lpRevenue": revLeftPeerRevenue,
                "rpTitle": revRightPeerTitle,
                "rpRevenue": revRightPeerRevenue,
            },
            "net_income":
            {
                "title": nITitle,
                "rank": nIRank,
                "explanation": nIExplanation,
                "lpTitle": nILeftPeerTitle,
                "lpNetIncome": nILeftPeerNetIncome,
                "rpTitle": nIRightPeerTitle,
                "rpNetIncome": nIRightPeerNetIncome,
            },
            "ebitda":
            {
                "title": ebTitle,
                "rank": ebRank,
                "explanation": ebExplanation,
                "lpTitle": ebLeftPeerTitle,
                "lpEBITDA": ebLeftPeerEBITDA,
                "rpTitle": ebRightPeerTitle,
                "rpEBITDA": ebRightPeerEBITDA,
                
            },
            "cash_context": cash_ctx,
            "recommendations": recommendations
        }

    def run(self):

        df = self.load_dataset()
        df = df.sort_values(by="GICS Sector")
        df = self.ensure_financial_metrics(df)

        return{"\nAvailable GICS Sectors:\n"}

        for sector in sorted(df["GICS Sector"].dropna().unique()):
            return{f"- {sector}"}

        return{"\nEnter your company's financial information.\n"}

        name = input("Enter Company Name: ")
        industry = input("Enter GICS Sector: ")

        revenue = self.get_float("Enter Revenue: ")
        cogs = self.get_float("Enter COGS: ")
        sga = self.get_float("Enter SG&A Expense: ")
        marketing = self.get_float("Enter Marketing Expense: ")
        rd = self.get_float("Enter R&D Expense: ")
        depreciation = self.get_float("Enter Depreciation: ")
        amortization = self.get_float("Enter Amortization: ")
        current_assets = self.get_float("Enter Current Assets: ")
        liabilities = self.get_float("Enter Current Liabilities: ")
        non_cash = self.get_float("Enter Non-Cash Expenses: ")
        change_wc = self.get_float("Enter Change in Working Capital: ")
        capex = self.get_float("Enter Capital Expenditures: ")

        self.analyze_company(
            name=name,
            industry=industry,
            revenue=revenue,
            cogs=cogs,
            sga=sga,
            marketing=marketing,
            rd=rd,
            depreciation=depreciation,
            amortization=amortization,
            current_assets=current_assets,
            liabilities=liabilities,
            non_cash=non_cash,
            change_wc=change_wc,
            capex=capex,
            df=df
        )


if __name__ == "__main__":
    try:
        Runner().run()
    except Exception as e:
        print("\nERROR:")
        print(type(e).__name__)
        print(e)
        input("\nPress Enter to exit...")
