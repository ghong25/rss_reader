from flask import render_template, redirect, request, flash
from app import app, db
from models import Article, Source
from feed import Feed

# home page, displays unread articles
@app.route('/', methods=['GET'])
def index():
    query = Article.query
    # display only unread articles and sort by descending publication date
    query = query.filter(Article.unread == True)
    articles = query.order_by(Article.date_published.desc())

    sources = Source.query
    page = request.args.get('page', 1, type=int)

    return render_template('home.html', articles=articles, sources=sources)

# different page numbers of the database query
@app.route('/<int:page_num>')
def index_num(page_num):
    articles = Article.query.paginate(per_page=20, page=page_num)
    # will have to fix this stuff below, but good enough for now
    return render_template('home.html', articles=articles)

# returns articles from a particular source
@app.route('/sort/<int:source_id>', methods=['GET'])
def source_filter(source_id):
    query = Article.query
    query = query.filter(Article.source_id == source_id)
    query = query.filter(Article.unread == True)
    query = query.order_by(Article.date_published.desc())
    articles = query.all()

    sources = Source.query
    return render_template('sort.html', articles=articles, sources=sources)

# flags articles as read and redirecting to url of particular article
@app.route('/read/<int:article_id>', methods=['GET'])
def read_article_get(article_id):
    article = Article.query.get(article_id)
    article.unread = False
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
        flash("Invalid Feed")
    return redirect('/sources')

# display sources to potentially remove
@app.route('/delete', methods=['GET'])
def display_source():
    query = Source.query
    query = query.order_by(Source.title)
    sources = query.all()
    return render_template('remove_source.html', sources=sources)

# Delete Article
@app.route('/delete_source/<int:id>', methods=['POST'])
def delete_source(id):
    # trying to avoid foreign key constraint?
    db.session.query(Article).filter(Article.source_id == id).delete()
    db.session.commit()

    db.session.query(Source).filter(Source.id == id).delete()
    db.session.commit()
    flash('Source Deleted', 'success')
    return redirect('/sources')
