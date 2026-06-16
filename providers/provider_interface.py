from abc import ABC, abstractmethod
import pandas as pd


class DataProvider(ABC):

    """
    Base interface for all market data providers.

    Every provider must return a standardized dataframe
    so that the rest of MarketMind remains unchanged,
    regardless of the underlying data source.
    """

    @abstractmethod
    def fetch_products(
        self,
        keyword: str,
        limit: int = 20
    ) -> pd.DataFrame:
        """
        Fetch products related to a keyword.

        Parameters
        ----------
        keyword : str
            Search keyword/category to monitor.

        limit : int
            Maximum number of products to return.

        Returns
        -------
        pd.DataFrame
            DataFrame containing the following columns:

            keyword
            product_name
            price
            rating
            review_count
            timestamp
        """
        pass