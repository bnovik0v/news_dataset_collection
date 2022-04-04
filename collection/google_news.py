""" Methods to collect news from Google News """

from typing import Optional, List, Dict, Union, Tuple
from pathlib import Path
import csv

from pygooglenews import GoogleNews
from tqdm import tqdm

from collection import utils


def collect_by_topic(topic: str,
                     *,
                     language: Optional[str] = None,
                     results_num: int = 10) -> List[Dict]:
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

    general_name = topic.replace(' ', '_')
    return [{'title': entity.get('title'),
             'link': entity.get('link'),
             'name': f'{general_name}_{i}'}
            for i, entity
            in enumerate(found_news)]


def collect_from_list_of_topics(topics: Union[List[str], List[Tuple]],
                                *,
                                language: Optional[str] = None) -> List[Dict]:
    """
    Collect news related to the given topics provided by Google News
    :param topics: list of topics or list of tuples of topic and search language
    :param language: language of topics, if not specified in topics
    :return: titles and urls of founded news
    """
    if isinstance(topics[0], str):
        return [{'topic': topic,
                 'language': language,
                 'news': collect_by_topic(topic, language=language)}
                for topic
                in tqdm(topics, desc='Collecting news urls and headlines from Google News')]
    else:
        return [{'topic': topic,
                 'language': lang,
                 'news': collect_by_topic(topic, language=lang)}
                for topic, lang
                in tqdm(topics, desc='Collecting news urls and headlines from Google News')]


def read_topics_from_csv(path: str) -> List[Tuple]:
    """
    Read topics and language of search from csv file
    :param path: path to csv file
    :return: list of tuples of topics and search language
    """
    path = Path(path)
    with path.open() as file:
        reader = csv.DictReader(file)
        return [(row['topic'], row['language'])
                for row
                in reader]


def collect_from_file(source_file: str,
                      *,
                      output_file: Optional[str] = None) -> List[Dict]:
    """
    Collect news related to topics provided in file
    :param source_file: path to csv file with topics
    :param output_file: if specified, result will be placed in it
    :return: titles and urls of founded news
    """
    topics = read_topics_from_csv(source_file)
    news = collect_from_list_of_topics(topics)
    if output_file:
        utils.save_json(news, output_file)
    return news
