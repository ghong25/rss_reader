from app import app, db
from models import Article, Source
import routes
from feed import Feed
from threading import Thread
import time


def update_loop():
    while True:
        with app.app_context():
            query = Source.query
            for src in query.all():
                try:
                    update_source(src)
                except:
                    continue
        time.sleep(60 * 60)


def update_source(src):
    src_obj = Feed(src.feed)
    feed_articles = src_obj.get_articles()
    # insert the articles into the db
    Article.insert_from_feed(src.id, feed_articles)
    print('Updated ' + src.feed)


thread = Thread(target=update_loop())
thread.start()
