from typing import Optional, List

import requests
from tqdm import tqdm

from collection import utils


def retrieve(url: str) -> str:
    """
    Retrieve html from url
    :param url: url
    :return: html
    """
    return requests.get(url).text


def load_and_save(url: str, filename: str, dest: Optional[str] = None):
    """
    Load html from url and save locally
    :param url: url
    :param filename: filename
    :param dest: destination directory
    """
    utils.save_text(retrieve(url), filename, dest)


def load_and_save_from_list(urls: List[str], filenames: List[str], dest: str):
    """
    Load and save html documents from url
    :param urls: list of urls
    :param filenames: filenames
    :param dest: destination directory
    """
    if len(urls) != len(filenames):
        raise ValueError('The number of urls and filenames must be the same.')

    for url, filename in tqdm(zip(urls, filenames),
                              desc='Loading and saving news locally',
                              total=len(urls)):
        try:
            load_and_save(url, filename, dest)
        except:
            pass
