class CompanyProfMetrics:
    def __init__(self, name, industry):
        # Identity
        self.name = name
        self.industry = industry

        # Financial inputs
        self.revenue = None
        self.cogs = None
        self.sga = None
        self.marketing = None
        self.rd = None
        self.operating_costs = None

        # Profitability metrics
        self.gross_profit = None
        self.net_income = None
        self.net_income_margin = None

        # EBITDA components
        self.depreciation = 0.0
        self.amortization = 0.0
        self.ebitda = None

    # -------------------------------
    # Input layer
    # -------------------------------
    def set_financials(self, revenue, cogs, sgaCosts, marketingCosts, rdCosts):
        self.revenue = revenue
        self.cogs = cogs
        self.sga = sgaCosts
        self.marketing = marketingCosts
        self.rd = rdCosts
        self.operating_costs = self.sga + self.marketing + self.rd

    # -------------------------------
    # Calculations
    # -------------------------------
    def calculate_profitability(self):
        self.gross_profit = self.revenue - self.cogs
        self.net_income = self.revenue - self.cogs - self.operating_costs
        self.net_income_margin = self.net_income / self.revenue if self.revenue != 0 else 0

    def calculate_ebitda(self, depreciation, amortization):
        self.depreciation = depreciation
        self.amortization = amortization
        self.ebitda = self.net_income + self.depreciation + self.amortization
        return self.ebitda;

    # -------------------------------
    # Evaluation
    # -------------------------------
    def evaluate_against_benchmark(self, industry_avg_margin):
        if self.revenue == 0:
            return "Revenue is zero; cannot evaluate performance."

        if self.net_income_margin > industry_avg_margin:
            return "\nYour company is outperforming the industry average net income margin."
        elif self.net_income_margin == industry_avg_margin:
            return "\nYour company is performing on par with the industry average."
        else:
            return "\nYour company is underperforming the industry average net income margin."

    # -------------------------------
    # Reporting
    # -------------------------------
    
    def getNetIncome(self):
        return self.net_income
    
        
    def summary(self):
        return (
            f"\n--- Profitability Metrics Evaluation for {self.name} ---\n"
            f"Industry: {self.industry}\n"
            f"Revenue: {self.revenue}\n"
            f"COGS: {self.cogs}\n"
            f"Gross Profit: {self.gross_profit}\n"
            f"Net Income: {self.net_income}\n"
            f"Net Income Margin: {self.net_income_margin:.4f}\n"
            f"EBITDA: {self.ebitda}\n"
        )