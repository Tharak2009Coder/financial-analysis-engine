class ProfAnalyzer:

    def __init__(self):
        # These values belong to this ProfAnalyzer object.
        self.userRevenue = None
        self.revRight = None

    # =====================================================
    # REVENUE ANALYSIS
    # =====================================================

    def analyze_revenue(
        self,
        compRevenue,
        revRightPeerRevenue
    ):

        # Store the revenue values so other methods can use them.
        self.userRevenue = compRevenue
        self.revRight = revRightPeerRevenue

        # Check whether the higher peer exists.
        if revRightPeerRevenue is None:
            return (
                "Revenue data for the higher-ranked "
                "competitor is not available."
            )

        # Prevent division by zero.
        if revRightPeerRevenue == 0:
            return (
                "Revenue comparison cannot be calculated "
                "because the higher peer's revenue is zero."
            )

        # Calculate how far the company is below the higher peer.
        revGapPercent = (
            (revRightPeerRevenue - compRevenue)
            / revRightPeerRevenue
        ) * 100

        if revGapPercent > 0:
            return (
                f"The company's revenue is "
                f"{revGapPercent:.2f}% lower than "
                f"its closest higher-ranked peer."
            )

        elif revGapPercent == 0:
            return (
                "The company's revenue is equal to "
                "its closest higher-ranked peer."
            )

        else:
            return (
                f"Revenue is ({revGapPercent:.2f}%) below "
                f"the closest higher-ranked peer. To close this gap, investigate "
                f"expanding sales in higher-demand customer segments, improving "
                f"customer retention and repeat purchases, increasing pricing where "
                f"the market supports it, or developing complementary products and "
                f"channels. Revenue growth can strengthen net income and free cash "
                f"flow only if the associated costs remain proportionate."
            )

    # =====================================================
    # NET INCOME ANALYSIS
    # =====================================================

    def analyze_net_income(
        self,
        compRevenue,
        compNetIncome,
        revRightPeerRevenue,
        revRightPeerNetIncome
    ):

        # Check that all required values exist.
        if revRightPeerRevenue is None:
            return (
                "Revenue data for the higher-ranked "
                "competitor is not available."
            )

        if revRightPeerNetIncome is None:
            return (
                "Net income data for the higher-ranked "
                "competitor is not available."
            )

        # Prevent division by zero.
        if compRevenue == 0:
            return (
                "The company's net profit margin cannot "
                "be calculated because revenue is zero."
            )

        if revRightPeerRevenue == 0:
            return (
                "The peer's net profit margin cannot "
                "be calculated because its revenue is zero."
            )

        # Calculate the company's net profit margin.
        net_prof_margin = (
            compNetIncome / compRevenue
        ) * 100

        # Calculate the higher peer's net profit margin.
        net_prof_margin_peer = (
            revRightPeerNetIncome
            / revRightPeerRevenue
        ) * 100

        # Calculate the difference in percentage points.
        marginGap = (
            net_prof_margin_peer
            - net_prof_margin
        )

        if marginGap > 0:
            return (
                f"The company's net profit margin is "
                f"{marginGap:.2f} percentage points lower "
                f"than its closest higher-ranked peer. "
                f"The company has a net profit margin of "
                f"{net_prof_margin:.2f}%, compared with "
                f"{net_prof_margin_peer:.2f}% for the peer."
            )

        elif marginGap == 0:
            return (
                f"The company and its closest higher-ranked "
                f"peer have the same net profit margin of "
                f"{net_prof_margin:.2f}%."
            )

        else:
            return (
                f"The company's net profit margin is "
                f"{abs(marginGap):.2f} percentage points "
                f"higher than its selected peer. "
                f"The company has a net profit margin of "
                f"{net_prof_margin:.2f}%, compared with "
                f"{net_prof_margin_peer:.2f}% for the peer."
            )

    # =====================================================
    # EBITDA ANALYSIS
    # =====================================================

    def analyze_ebitda(
        self,
        compRevenue,
        compEBITDA,
        revRightPeerRevenue,
        revRightPeerEBITDA
    ):

        # Check that the peer data exists.
        if revRightPeerRevenue is None:
            return (
                "Revenue data for the higher-ranked "
                "competitor is not available."
            )

        if revRightPeerEBITDA is None:
            return (
                "EBITDA data for the higher-ranked "
                "competitor is not available."
            )

        # Prevent division by zero.
        if compRevenue == 0:
            return (
                "The company's EBITDA margin cannot "
                "be calculated because revenue is zero."
            )

        if revRightPeerRevenue == 0:
            return (
                "The peer's EBITDA margin cannot "
                "be calculated because its revenue is zero."
            )

        # Calculate EBITDA margins.
        ebitda_margin = (
            compEBITDA / compRevenue
        ) * 100

        ebitda_margin_peer = (
            revRightPeerEBITDA
            / revRightPeerRevenue
        ) * 100

        # Calculate the difference in percentage points.
        marginGap = (
            ebitda_margin_peer
            - ebitda_margin
        )

        if marginGap > 0:
            return (
                f"The company's EBITDA margin is "
                f"{marginGap:.2f} percentage points lower "
                f"than its closest higher-ranked peer. "
                f"The company has an EBITDA margin of "
                f"{ebitda_margin:.2f}%, compared with "
                f"{ebitda_margin_peer:.2f}% for the peer."
            )

        elif marginGap == 0:
            return (
                f"The company and its closest higher-ranked "
                f"peer have the same EBITDA margin of "
                f"{ebitda_margin:.2f}%."
            )

        else:
            return (
                f"The company's EBITDA margin is "
                f"{abs(marginGap):.2f} percentage points "
                f"higher than its selected peer. "
                f"The company has an EBITDA margin of "
                f"{ebitda_margin:.2f}%, compared with "
                f"{ebitda_margin_peer:.2f}% for the peer."
            )