#!/usr/bin/env python

__author__ = "student"
__version__ = "1.0"
# June 26, 2017
# Flask Blog App re: LaunchCode LC-101
# Rubric: http://education.launchcode.org/web-fundamentals/assignments/build-a-blog/


from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:insecure@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'super_secret_key'


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_text = db.Column(db.String(1024))
    date = db.Column(db.DateTime)

    def __init__(self, blog_title, blog_text, date=None):
        self.blog_title = blog_title
        self.blog_text = blog_text
        if date is None:
            date = datetime.utcnow()
        self.date = date


@app.route('/blog', methods=['GET', 'POST'])
def index():
    blogs = BlogPost.query.all()

    if 'id' in request.args:
        blog_id = request.args['id']
        blog_post = BlogPost.query.get(blog_id)
        return render_template('post.html', blog=blog_post)

    return render_template('blog.html', blogs=blogs)


@app.route('/newpost', methods=['GET', 'POST'])
def add_blog():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_text = request.form['blog_text']

        title_error = ''
        text_error = ''

        if blog_title == '':
            title_error = "Please enter a title."
        if blog_text == '':
            text_error = "Please enter blog text."

        if not title_error and not text_error:

            new_blog = BlogPost(blog_title, blog_text)
            db.session.add(new_blog)
            db.session.commit()
            id_param = new_blog.id

            return redirect('/blog?id={0}'.format(id_param))

        else:
            return render_template('newpost.html', title_error=title_error, text_error=text_error,
                                   blog_text=blog_text, blog_title=blog_title)
    else:
        return render_template('newpost.html')


if __name__ == '__main__':
    app.run()
