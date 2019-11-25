"""
data models
"""
from app import db
from time import mktime
from datetime import datetime


# model for article
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    link = db.Column(db.Text, nullable=False)
    guid = db.Column(db.String(255), nullable=False)
    unread = db.Column(db.Boolean, default=True, nullable=False)
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'), nullable=False)
    source = db.relationship('Source', backref=db.backref('articles', lazy=True))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_published = db.Column(db.DateTime)
    __table_args__ = (
        db.UniqueConstraint('source_id', 'guid', name='uc_source_guid'),
    )
    @classmethod
    def insert_from_feed(cls, source_id, feed_articles):
        # statement that SQl uses to insert articles into database
        # create insert ignore statement so when uniqueness constraint fails (same source and unique id), ignores it
        stmt = Article.__table__.insert().prefix_with('IGNORE')
        articles = []
        for article in feed_articles:
            articles.append({
                'title': article['title'],
                'body': article['summary'],
                'link': article['link'],
                'guid': article['id'],
                'source_id': source_id,
                # convert to datetime obj from time.struct_time object bc date_published expects datetime
                'date_published': datetime.fromtimestamp(mktime(article['published'])),
            })
        db.engine.execute(stmt, articles)


# model for source
class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.Text, nullable=False)
    link = db.Column(db.Text, nullable=False)
    feed = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    @classmethod
    def insert_from_feed(cls, feed, feed_source):
        link = feed_source['link']
        title = feed_source['title']
        source = Source(feed=feed, link=link, title=title)
        # update the database
        db.session.add(source)
        db.session.commit()
        return source
