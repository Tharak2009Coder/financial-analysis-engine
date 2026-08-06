import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from pathlib import Path


class DataVisualization:

    STATIC_FOLDER = Path("static")

    def _plot_ranking_graph(
        self,
        company_name,
        company_value,
        title,
        rank,
        left_peer_title,
        left_peer_value,
        right_peer_title,
        right_peer_value,
        y_label,
        output_filename,
    ):
        # A peer can be missing for the lowest/highest-ranked company.
        # Do not add a bar for that missing peer.
        entries = [
            (left_peer_title, left_peer_value, "lightgray"),
            (company_name, company_value, "#00BFFF"),
            (right_peer_title, right_peer_value, "lightgray"),
        ]

        valid_entries = [
            (label, float(value), color)
            for label, value, color in entries
            if value is not None
        ]

        labels = [label for label, _, _ in valid_entries]
        values = [value for _, value, _ in valid_entries]
        colors = [color for _, _, color in valid_entries]

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(labels, values, color=colors)

        ax.set_title(f"{title}\n{rank}", fontsize=14)
        ax.set_xlabel("Companies")
        ax.set_ylabel(y_label)

        ax.yaxis.set_major_formatter(
            FuncFormatter(lambda x, _: f"${x:,.0f}")
        )

        for bar in bars:
            height = bar.get_height()

            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"${height:,.0f}",
                ha="center",
                va="bottom" if height >= 0 else "top",
                fontsize=9,
            )

        # Prevent value labels from touching the top edge.
        ax.margins(y=0.15)

        self.STATIC_FOLDER.mkdir(parents=True, exist_ok=True)

        fig.tight_layout()
        fig.savefig(
            self.STATIC_FOLDER / output_filename,
            dpi=300,
        )
        plt.close(fig)

    def plotRevenueGraph(
        self,
        companyName,
        compRevenue,
        revTitle,
        revRank,
        revLeftPeerTitle,
        revLeftPeerRevenue,
        revRightPeerTitle,
        revRightPeerRevenue,
    ):
        self._plot_ranking_graph(
            companyName,
            compRevenue,
            revTitle,
            revRank,
            revLeftPeerTitle,
            revLeftPeerRevenue,
            revRightPeerTitle,
            revRightPeerRevenue,
            "Revenue",
            "revenue_ranking.png",
        )

    def plotNetIncomeGraph(
        self,
        companyName,
        compNetIncome,
        netIncomeTitle,
        netIncomeRank,
        netIncomeLeftPeerTitle,
        netIncomeLeftPeerNetIncome,
        netIncomeRightPeerTitle,
        netIncomeRightPeerNetIncome,
    ):
        self._plot_ranking_graph(
            companyName,
            compNetIncome,
            netIncomeTitle,
            netIncomeRank,
            netIncomeLeftPeerTitle,
            netIncomeLeftPeerNetIncome,
            netIncomeRightPeerTitle,
            netIncomeRightPeerNetIncome,
            "Net Income",
            "net_income_ranking.png",
        )

    def plotEBITDAGraph(
        self,
        companyName,
        compEBITDA,
        ebitdaTitle,
        ebitdaRank,
        ebitdaLeftPeerTitle,
        ebitdaLeftPeerEBITDA,
        ebitdaRightPeerTitle,
        ebitdaRightPeerEBITDA,
    ):
        self._plot_ranking_graph(
            companyName,
            compEBITDA,
            ebitdaTitle,
            ebitdaRank,
            ebitdaLeftPeerTitle,
            ebitdaLeftPeerEBITDA,
            ebitdaRightPeerTitle,
            ebitdaRightPeerEBITDA,
            "EBITDA",
            "ebitda_ranking.png",
        )