""" HTML module """

import requests
import newspaper


def get_html(url: str) -> str:
    """
    Returns html document from url
    :param url: url
    :return: html document
    """
    return requests.get(url).text


def extract_text(html: str, language='en') -> str:
    """
    Extract text from html document
    :param html: html document
    :param language: language of html document
    :return: text
    """
    return newspaper.fulltext(html, language)
