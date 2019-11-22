import feedparser


class Feed:
    def __init__(self, url):
        self.url = url
        self.parsed = feedparser.parse(self.url)

    def get_source(self):
        feed = self.parsed['feed']
        return {
            'link': feed['link'],
            'title': feed['title'],
            'subtitle': feed['subtitle'],
        }

    def get_articles(self):
        articles = []
        entries = self.parsed['entries']
        for entry in entries:
            articles.append({
                'id': entry['id'],
                'link': entry['link'],
                'title': entry['title'],
                'summary': entry['summary'],
                'published': entry['published_parsed'],
            })
        return articles
