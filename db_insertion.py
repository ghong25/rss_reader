"""
Inserts an RSS feed into the database
"""

from app import app, db
from models import Article, Source
from feed import Feed

articles = Article.query.all()

for article in articles:
    print(article.link)
