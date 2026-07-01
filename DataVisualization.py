"""
5 Bar Graphs:
1. Revenue Ranking Bar Graph: This graph will display the company's revenue ranking compared to its peers in the industry. 
2. Net Income Ranking Bar Graph: Similar to the revenue graph, this will show the company's net income ranking compared to its peers.
3. EBITDA Ranking Bar Graph: This graph will display the company's EBITDA ranking compared to its peers
4. Cash Flow Ranking Bar Graph: This graph will display the company's operating cash flow ranking compared to its peers
5. Free Cash Flow Ranking Bar Graph: This graph will display the company's free cash flow ranking compared to its peers

Use matplotlib and categorize each of the 5 graphs presented under each category 
(Revenue, Net Income, EBITDA, Cash Flow, Free Cash Flow) into 3 categories:

3 graphs will be under Revenue, 3 under Net Income, and so on

Use different colors to represent each category and include a legend for clarity. 
The x-axis will represent the company and its peers, while the y-axis will represent the ranking 
position. Each bar will be labeled with the company's name and its specific ranking position for 
better visualization.
"""

import matplotlib.pyplot as plt

class DataVisualization:
    def plotData(self, ranking1, ranking2, ranking3):
        categories = ['Revenue', 'Net Income', 'EBITDA']
        revenue_percentile = (
        (ranking1["total"] - ranking1["rank"] + 1)
        / ranking1["total"]
        ) * 100

        net_income_percentile = (
            (ranking2["total"] - ranking2["rank"] + 1)
            / ranking2["total"]
        ) * 100

        ebitda_percentile = (
            (ranking3["total"] - ranking3["rank"] + 1)
            / ranking3["total"]
        ) * 100


        
        colors = ['blue', 'orange', 'green']
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(categories, [revenue_percentile, net_income_percentile, ebitda_percentile], color=colors)
        
        plt.xlabel('Financial Metrics')
        plt.ylabel('Percentile Rank')
        plt.title('Company Ranking Compared to Industry Peers')
        plt.ylim(0, 100)
        
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1, int(yval), ha='center', va='bottom')
        
        plt.legend(categories)
        plt.show()