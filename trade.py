"""
Algorithmic trading testing.

"""
import pandas as pd
import strategy
from backtesting.barfeed import yahoofeed

def show_clustered_equities(exchange):
    """
    Show details for the clustered equities
    :param exchange: Exchange name
    :return: None
    """
    df_clustered_equities = pd.read_csv('dataset/{}_clustered_equities.csv'.format(exchange))
    print(df_clustered_equities.groupby(['cluster']).symbol.nunique())


def get_equities_by_cluster(df_equities, cluster):
    print("Get equities by clusters")


def main():
    """
    Main script.
    """
    # show_clustered_equities('KLS')

    # Load the yahoo feed from the CSV file
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV("ytlpowr", "dataset/6742.KL.csv")

    # Evaluate the strategy with the feed's bars.
    myStrategy = strategy.TestStrategy(feed, "ytlpowr")
    myStrategy.run()


if __name__ == "__main__":
    main()
