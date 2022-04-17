""" Dataset module """

from typing import Sequence, Optional
import itertools
from tqdm import tqdm
import pathlib

import pandas as pd

from collection.requests import create_request, collect_news
from collection.html import get_html, extract_text

tqdm.pandas()


class NewsDatasetCollector:
    """ News Dataset Collector """

    def __init__(self):
        self.reqs = []
        self._df = pd.DataFrame()

    @property
    def df(self) -> pd.DataFrame:
        """ News DataFrame """
        return self._df

    @df.setter
    def df(self, df: pd.DataFrame):
        self._df = df

    def collect_news(self,
                     topics: Sequence[str],
                     sites: Sequence[str] = None,
                     reset: bool = False,
                     num_samples: int = 40):
        """
        Collect news by given topics
        :param topics: topics, e.g., 'crime', 'fraud'
        :param sites: sites, e.g., 'reuters.com', 'bbc.com'
        :param reset: clean collected news
        :param num_samples: number of samples to return by one request
        """
        if sites:
            new_reqs = list(
                map(lambda topic_site: create_request(topic_site[0], topic_site[1]),
                    itertools.product(topics, sites))
            )
        else:
            new_reqs = list(map(create_request, topics))

        if reset:
            self.reqs = new_reqs
            self.df = collect_news(self.reqs, num_samples)
        else:
            self.reqs.extend(new_reqs)
            self.df = pd.concat([self.df,
                                 collect_news(new_reqs, num_samples)],
                                ignore_index=True)

        self.df.drop_duplicates('link', inplace=True)

        print('total number of news: %s' % self.df.shape[0])

    def parse_text(self):
        """
        Parse text from url
        """
        self.df['text'] = self.df.link.progress_apply(
            lambda l: extract_text(get_html(l))
        )

    def to_csv(self, filepath: Optional[str] = None):
        """
        Save df
        :param filepath: filepath where to save
        """
        if not filepath:
            filepath = pathlib.Path.cwd() / 'dataset.csv'
        self.df.to_csv(filepath, index=False)
