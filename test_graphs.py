from DataVisualization import DataVisualization

visualizer = DataVisualization()

# =====================================================
# Revenue Graph
# =====================================================

visualizer.plotRevenueGraph(
    companyName="Nova Analytics",
    compRevenue=95_000_000,

    revTitle="Revenue Benchmark",
    revRank="Ranked #152 of 500 Companies",

    revLeftPeerTitle="GenTech",
    revLeftPeerRevenue=82_000_000,

    revRightPeerTitle="CloudCore",
    revRightPeerRevenue=118_000_000
)

# =====================================================
# Net Income Graph
# =====================================================

visualizer.plotNetIncomeGraph(
    companyName="Nova Analytics",
    compNetIncome=22_400_000,

    netIncomeTitle="Net Income Benchmark",
    netIncomeRank="Ranked #168 of 500 Companies",

    netIncomeLeftPeerTitle="GenTech",
    netIncomeLeftPeerRevenue=19_700_000,

    netIncomeRightPeerTitle="CloudCore",
    netIncomeRightPeerRevenue=27_900_000
)

# =====================================================
# EBITDA Graph
# =====================================================

visualizer.plotEBITDAGraph(
    companyName="Nova Analytics",
    compEBITDA=25_300_000,

    ebitdaTitle="EBITDA Benchmark",
    ebitdaRank="Ranked #147 of 500 Companies",

    ebitdaLeftPeerTitle="GenTech",
    ebitdaLeftPeerRevenue=23_100_000,

    ebitdaRightPeerTitle="CloudCore",
    ebitdaRightPeerRevenue=31_600_000
)

print("Graphs generated successfully!")