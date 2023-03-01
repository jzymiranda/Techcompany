from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from application import views


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mirandajing:@localhost:5432/demo'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    subtitle = db.Column(db.String)
    author = db.Column(db.String)
    content = db.Column(db.String)
    date_posted = db.Column('timestamp', db.DateTime, default=datetime.now())

@app.route('/')
def index():
    posts = BlogPost.query.all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = BlogPost.query.get(post_id)
    return render_template('post.html', post=post)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = BlogPost(title=title, subtitle=subtitle, author=author, content=content)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/news')
def news():
    url = ('https://newsapi.org/v2/everything?domains=techcrunch.com,thenextweb.com&apiKey=deb9f1b358564867965ed28ada681a2a')
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    return render_template('news.html', articles=articles)

app.add_url_rule('/faceapp', 'faceapp', views.faceapp, methods=['GET', 'POST'])





if __name__ == '__main__':
    app.run(debug=True)