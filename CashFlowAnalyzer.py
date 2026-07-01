class CashFlowAnalyzer:
    def explain_cash_flow(self, cash_ctx):

        if cash_ctx["earnings_quality_strong"]:

            print(
                "- Operating cash generation closely "
                "tracks reported earnings, indicating "
                "strong earnings quality and limited "
                "reliance on accounting adjustments."
            )

        else:

            print(
                "- Cash generation differs materially "
                "from reported earnings, suggesting "
                "that investors should further examine "
                "working capital movements and non-cash "
                "accounting adjustments."
            )
        
        if cash_ctx["strong_liquidity"]:

            print(
                "- The company maintains a strong "
                "liquidity position, supported by "
                "positive working capital and healthy "
                "cash generation from operations."
            )

        elif cash_ctx["cash_flow_pressure"]:

            print(
                "- The company may be experiencing "
                "liquidity pressure due to negative "
                "free cash flow and constrained cash "
                "generation."
            )

        else:

            if cash_ctx["above_average_operating_cf"]:
                print(
                    "- Operating cash flow exceeds the "
                    "industry average, demonstrating "
                    "stronger cash generation from core "
                    "business operations.")
            else:
                print(
                    "- Operating cash flow trails the "
                    "industry average, suggesting that "
                    "core operations generate less cash "
                    "than many industry peers.")
                
            if cash_ctx["above_average_free_cash_flow"]:
                print(
                    "- Free cash flow exceeds the industry "
                    "average, providing greater financial "
                    "flexibility for investments, debt "
                    "repayment, acquisitions, and future "
                    "growth initiatives.")
            else:
                print(
                    "- Free cash flow trails the industry "
                    "average, which may limit the company's "
                    "ability to internally finance growth "
                    "and strategic investments."
                )
        
        if cash_ctx["above_average_working_capital"]:

            print(
                "- Working capital exceeds the industry "
                "average, indicating a stronger ability "
                "to meet short-term obligations and "
                "support ongoing operations."
            )

        else:

            print(
                "- Working capital trails the industry "
                "average, which may suggest tighter "
                "short-term liquidity management."
            )
        
