from collection import google_news, html_loading

if __name__ == '__main__':
    # [{'topic': ...,
    #   'language': ...,
    #   'news': [{'title': ..., 'link': ..., 'name': ...}, ...]
    #   }, ...]
    news_headlines = google_news.collect_from_file('data/news_topics.csv',
                                                   output_file='data/news_mapping.json')

    filenames, links = zip(*[(f"{news['name']}.html", news['link'])
                             for topic in news_headlines
                             for news in topic['news']])
    html_loading.load_and_save_from_list(links, filenames, 'data/news')


