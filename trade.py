"""
Algorithmic trading testing.

"""
import pandas as pd


def show_clustered_equities(exchange):
    """
    Show details for the clustered equities
    :param exchange: Exchange name
    :return: None
    """
    df_clustered_equities = pd.read_csv('dataset/{}_clustered_equities.csv'.format(exchange))
    print(df_clustered_equities)

def main():
    """
    Main script.
    """
    show_clustered_equities('KLS')



if __name__ == "__main__":
    main()