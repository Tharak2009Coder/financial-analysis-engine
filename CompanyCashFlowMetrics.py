class CompanyCashFlowMetrics:
    
    '''
    The inputs to perform certain calculations and provide an explanation about the
    Company's cash flow and liquidity to serve as a guide to liquidating certain assets:
    
     1) Net Income (get that information from CompanyProfMetrics)
     2) Current Assets & Liabalities (to calculate Working Capital)
     3) Non-Cash Expenses & Changes in Working Capital (to calculate OCF)
     4) Capital Expenditures (to calculate FCF)
    '''
    def __init__(self, netIncome):
        self.netIncome = netIncome
        self.currentAssets = None
        self.liabilities = None
        self.ncExp = None
        self.changeWC = None
        self.capex = None
        self.workingCapital = None
        self.operatingCF = None
        self.fcf = None
    
    def set_financials(self, cA, liab, nc, wc, cap):
        self.currentAssets = cA
        self.liabilities = liab
        self.ncExp = nc
        self.changeWC = wc
        self.capex = cap
        self.workingCapital = self.currentAssets - self.liabilities
        self.operatingCF = (self.netIncome + self.ncExp) - self.changeWC
        self.fcf = self.operatingCF - self.capex
        # later see how could you calculate CCC (essential to see how much days it takes for a company to liquidate its assets)
        
    
    
    def get_context(self):
        """
        Returns cash-flow context ready for interpretation, ranking, or a decision tree.
        """
        earnings_quality_gap = abs(self.fcf - self.netIncome)

        return {
            # Core metrics
            "working_capital": self.workingCapital,
            "operating_cash_flow": self.operatingCF,
            "free_cash_flow": self.fcf,

            # Health flags
            "positive_operating_cf": self.operatingCF > 0,
            "positive_free_cash_flow": self.fcf > 0,

            # Quality & liquidity signals
            "strong_liquidity": self.workingCapital > 0 and self.fcf > 0,
            "earnings_quality_strong": (
                self.netIncome > 0 and earnings_quality_gap / self.netIncome < 0.25
            ),
            "cash_flow_pressure": self.fcf < 0
        }
    """
    Evaluates cash flow strength, liquidity, and earnings quality.
    Designed to mirror profitability evaluation style.
    """