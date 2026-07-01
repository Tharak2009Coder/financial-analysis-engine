class RecommendationEngine:
    def build_recommendations(self, ranking1, ranking2, ranking3, cash_ctx):
        recommendations = []

        def is_bottom_half(ranking):
            return ranking["rank"] <= ranking["total"] / 2

        # ranking 1 represents revenue
        if is_bottom_half(ranking1):
            recommendations.append(
                "Revenue trails many industry peers. "
                "Management may consider expanding market "
                "share through product innovation, customer "
                "acquisition initiatives, strategic partnerships, "
                "or geographic expansion."
            )
        
        # ranking 2 represents net income

        if is_bottom_half(ranking2):

            recommendations.append(
                "Net income performance is below many competitors. "
                "Management should evaluate operating expenses, "
                "pricing strategies, and cost controls to improve "
                "overall profitability."
            )
        
        # ranking 3 represents EBITDA

        if is_bottom_half(ranking3):

            recommendations.append(
                "EBITDA performance suggests weaker operational "
                "efficiency relative to peers. The company may "
                "benefit from process improvements, automation, "
                "supply-chain optimization, and tighter expense "
                "management."
            )
        if not cash_ctx["strong_liquidity"]:

            recommendations.append(
                "Working capital is below desired levels. "
                "Management should monitor receivables, "
                "inventory levels, and short-term obligations "
                "to strengthen liquidity."
            )
        
        if not cash_ctx["above_average_operating_cf"]:

            recommendations.append(
                "Operating cash flow trails industry peers. "
                "Improving collections, reducing operating "
                "costs, and increasing cash-generating activities "
                "may enhance financial flexibility."
            )
        
        if not cash_ctx["above_average_free_cash_flow"]:

            recommendations.append(
                "Free cash flow is below the industry average. "
                "Management may consider optimizing capital "
                "expenditures and improving operating cash flow "
                "generation to support future investments."
            )
        
        if cash_ctx["cash_flow_pressure"]:

            recommendations.append(
                "Negative cash flow pressure was identified. "
                "Management should prioritize liquidity planning, "
                "expense control, and sustainable cash generation."
            )

        """
        The above recommendations are fully based upon negative circumstances like below average
        fcf compared to industry, having cash flow pressure, or not having enough working capital

        If the recommendations don't have any single element, we can conclude that the company is in
        a healthy position in terms of profitability & cash flow metrics
        """
        print("\n--- STRATEGIC RECOMMENDATIONS ---")

        if recommendations:

            for recommendation in recommendations:
                print(f"• {recommendation}")

        else:

            print(
                "• The company demonstrates strong performance "
                "across profitability and cash-flow metrics. "
                "Management should continue focusing on growth, "
                "operational excellence, and capital allocation."
            )
        return recommendations
