from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))

    def __init__(self, title, body):
        self.title = title
        self.body = body

#def get_data(id):
#    return Blog.query.get(id)

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
        new_post = Blog.query.get(blogid)

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

