""" Requests module """
from typing import Sequence, Dict

import pandas as pd
from tqdm import tqdm
from pygooglenews import GoogleNews


def create_request(topic: str, site_url: str = None, in_title: bool = False) -> str:
    """
    Creates request based on the given topic, site url
    :param topic: topic
    :param site_url: site url
    :param in_title: topic should be in title?
    :return: request
    """
    req = ''
    if site_url:
        req += f'site:{site_url} '
    if in_title:
        req += 'intitle:'
    req += topic
    return req


def collect_by_topic(topic: str,
                     *,
                     language: str = 'en',
                     results_num: int = 10) -> Sequence[Dict]:
    """
    Collect news related to the given topic provided by Google News
    :param topic: news topic
    :param language: language of search
    :param results_num: number of results to return
    :return: titles and urls of founded news
    """
    if language:
        gn = GoogleNews(lang=language)
    else:
        gn = GoogleNews()
    search_result = gn.search(topic)
    found_news = search_result['entries'][:results_num]
    return [{'topic': topic,
             'title': entity.get('title'),
             'link': entity.get('link'),
             'language': language}
            for entity
            in found_news]


def collect_news(reqs: Sequence[str], num_samples=40) -> pd.DataFrame:
    """
    Collect news by requests
    :param reqs: requests
    :param num_samples: number of samples for each request to collect
    :return: news dataframe
    """
    news_df = pd.DataFrame()
    for req in tqdm(reqs):
        news_df = pd.concat([news_df, pd.DataFrame(collect_by_topic(req, results_num=num_samples))],
                            ignore_index=True)
    return news_df
