from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:insecure@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'qwer654Beta##'


class BlogPost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_text = db.Column(db.String(1024))

    def __init__(self, blog_title, blog_text):
        self.blog_title = blog_title
        self.blog_text = blog_text


@app.route('/blog', methods=['GET', 'POST'])
def index():

    blogs = BlogPost.query.all()   

    return render_template('blog.html', blogs=blogs)


@app.route('/add', methods=['GET', 'POST'])
def add_blog():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_text = request.form['blog_text']

        title_error = ''
        text_error = ''

        if blog_title == "":
            title_error = "Please enter a title."
        if blog_text == "":
            text_error = "Please enter blog text."    
        
        if not title_error and not text_error:

            new_blog = BlogPost(blog_title, blog_text)
            db.session.add(new_blog)
            db.session.commit()
            return_block = "<h1>{0}</h1><p>{1}</p>".format(blog_title,blog_text)

            return return_block

        else:
            return render_template('add.html', 
            title_error=title_error,
            text_error=text_error, 
            blog_text=blog_text, 
            blog_title=blog_title)    

    else:
        return render_template('add.html')


if __name__ == '__main__':
    app.run()  