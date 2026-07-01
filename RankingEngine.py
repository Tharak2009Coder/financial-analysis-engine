"""
This is a sub-runner class that's responsible for the specific ranking systems to show the user where
their organization is standing (& which competitors) using the S&P 500 dataset
"""
class RankingEngine:
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
        # Filter out peers with missing Revenue first so indices align
        valid_df = peers_df.dropna(subset=["Revenue"]).sort_values(by="Revenue").reset_index(drop=True)

        # If no valid peers with revenue, return a clear empty result
        if valid_df.empty:
            return {
                "rank": 1,
                "total": 1,
                "left_peer": None,
                "right_peer": None,
            }

        revenues = valid_df["Revenue"].tolist()

        position = self.binary_search_position(revenues, company_revenue)

        left_peer = valid_df.iloc[position - 1].to_dict() if position - 1 >= 0 else None
        right_peer = valid_df.iloc[position].to_dict() if position < len(valid_df) else None

        return {
            "rank": position + 1,
            "total": len(revenues) + 1,
            "left_peer": left_peer,
            "right_peer": right_peer,
        }

    # ----------------------------------
    # Net income ranking
    # ----------------------------------
    def rank_by_netIncome(
        self,
        peers_df,
        company_netIncome
    ):
        valid_df = peers_df.dropna(subset=["Net Income"]).sort_values(by="Net Income").reset_index(drop=True)

        if valid_df.empty:
            return {
                "rank": 1,
                "total": 1,
                "left_peer": None,
                "right_peer": None,
            }

        net_incomes = valid_df["Net Income"].tolist()

        position = self.binary_search_position(net_incomes, company_netIncome)

        left_peer = valid_df.iloc[position - 1].to_dict() if position - 1 >= 0 else None
        right_peer = valid_df.iloc[position].to_dict() if position < len(valid_df) else None

        return {
            "rank": position + 1,
            "total": len(net_incomes) + 1,
            "left_peer": left_peer,
            "right_peer": right_peer,
        }

    # ----------------------------------
    # EBITDA ranking
    # ----------------------------------
    def rank_by_ebitda(
        self,
        peers_df,
        company_ebitda
    ):
        valid_df = peers_df.dropna(subset=["EBITDA"]).sort_values(by="EBITDA").reset_index(drop=True)

        if valid_df.empty:
            return {
                "rank": 1,
                "total": 1,
                "left_peer": None,
                "right_peer": None,
            }

        ebitdas = valid_df["EBITDA"].tolist()

        position = self.binary_search_position(ebitdas, company_ebitda)

        left_peer = valid_df.iloc[position - 1].to_dict() if position - 1 >= 0 else None
        right_peer = valid_df.iloc[position].to_dict() if position < len(valid_df) else None

        return {
            "rank": position + 1,
            "total": len(ebitdas) + 1,
            "left_peer": left_peer,
            "right_peer": right_peer,
        }