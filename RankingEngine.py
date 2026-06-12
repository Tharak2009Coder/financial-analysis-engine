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