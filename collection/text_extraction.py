import newspaper

from collection import utils


def extract(html: str, language: str) -> str:
    """
    Extract text from html document
    :param html: html document
    :param language: language of document
    :return: extracted text
    """
    return newspaper.fulltext(html, language)


def extract_and_save(html: str, language: str, filename: str, dest: str):
    """
    Extract text and save locally
    :param html: html document to extract text from
    :param language: language of html document
    :param filename: filename
    :param dest: destination directory
    """
    utils.save_text(extract(html, language), filename, dest)

if __name__ == '__main__':
    extract_and_save()