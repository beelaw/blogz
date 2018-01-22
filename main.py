from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    __tablename__ = 'blog'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/newpost', methods=['POST', 'GET'])
def index():


    error_text = ''

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        
        if title == '' or body == '':
            error_text = "Please fill out all forms"
            return render_template('newpost.html', title_ph = title, body_ph = body, error_text = error_text)

        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()

        blogs = Blog.query.all()

        blogid = 0
        for i in blogs:
            blogid += 1
        new_post = Blog.query.get(blogid) #find length of list instead

        return render_template('postblog.html', blogs=blogs, post=new_post)
    else:
        return render_template('newpost.html')

    blogs = Blog.query.all()

    return render_template('blog.html', blogs=blogs)

@app.route('/blog')
@app.route('/blog/<bid>', methods=['GET'])
def blog():
    blogs = Blog.query.all()
    blogid=request.args.get('bid')
    if blogid:
        blogid=request.args.get('bid')
        new_post = Blog.query.get(blogid)
        return render_template('postblog.html', blogs=blogs, post=new_post)

    else:
        return render_template('blog.html', blogs=blogs)



#@app.route('/postblog/', methods=['GET'])
#@app.route('/postblog/<idef>/', methods=['GET'])
#def post():
    #postid = str(request.args.get('idef', idef))
    #postid = 'meh'
    
#    for i in blogs.length()
#    blogs = Blog.query.all()

#    return render_template('blog.html', blogs= blogs)


if __name__ == '__main__':
    app.run()

