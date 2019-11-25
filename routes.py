from flask import render_template, redirect, request, url_for
from app import app, db
from models import Article, Source
from feed import Feed
from sqlalchemy import Table

# home page, displays unread articles
@app.route('/', methods=['GET'])
def index():
    query = Article.query
    # display only unread articles and sort by descending publication date
    query = query.filter(Article.unread == True)
    query = query.order_by(Article.date_published.desc())

    sources = Source.query
    page = request.args.get('page', 1, type=int)

    articles = query.paginate(page, 10, False)
    return render_template('home.html', articles=articles.items)#, sources=sources.items)

# different page numbers of the database query
@app.route('/<int:page_num>')
def index_num(page_num):
    articles = Article.query.paginate(per_page=20, page=page_num, error_out=True)
    # will have to fix this stuff below, but good enough for now
    return render_template('base.html', articles=articles)  


# flags articles as read and redirecting to url of particular article
@app.route('/read/<int:article_id>', methods=['GET'])
def read_article_get(article_id):
    article = Article.query.get(article_id)
    article.unread = True
    db.session.commit()
    return redirect("http://outline.com/" + str(article.link))

# list feeds subscribed to and gives form to add new sources
@app.route('/sources', methods=['GET'])
def sources_get():
    query = Source.query
    query = query.order_by(Source.title)
    sources = query.all()
    return render_template('sources.html', sources=sources)

# where the form posts to
@app.route('/sources', methods=['POST'])
def sources_post():
    feed_url = request.form['feed']
    # create new Feed object from feed_url
    try:
        feed_obj = Feed(feed_url)
        source = Source.insert_from_feed(feed_url, feed_obj.get_source())
        # retrieve articles from the rss feed added by the form
        feed_articles = feed_obj.get_articles()
        Article.insert_from_feed(source.id, feed_articles)
    except:
        print("Invalid Feed")
    return redirect('/sources')

# delete sources from db
@app.route('/sources/<int:source_id>', methods=['DELETE'])
def sources_remove(source_id):
    source = Source.query.filter(id=source_id)
    db.session.delete(source)
    return "Source deleted."