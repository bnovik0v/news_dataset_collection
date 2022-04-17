from collection.dataset import NewsDatasetCollector


if __name__ == '__main__':
    financial_crime_topics = ['fraud', 'money-laundering', 'scam', 'financial crime', 'offshore',
                              'bribe', 'panama papers', 'bankrupt', 'mismanagement',
                              'pandora paper', 'mossack fonseca', 'corruption', 'tax evasion',
                              'hiding wealth', 'tax cheat', 'shell company',
                              'british virgin islands']
    financial_news_sites = ['theguardian.com']  # 'bbc.com','reuters.com', 'theguardian.com']

    ndc = NewsDatasetCollector()
    ndc.collect_news(topics=financial_crime_topics,
                     sites=financial_news_sites,
                     reset=False,
                     num_samples=40)
    ndc.parse_text()
    ndc.to_csv()
