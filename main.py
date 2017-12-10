from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymsql://build-a-blog:delmar@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO '] = True
app.config['SESSION_TYPE'] = 'filesystem'
db =  SQLAlchemy(app)   

class Blog(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(120))
    body = db.Column(db.String(5000))
    
    def __init__(self,post_title,body):
        self.post_title = post_title
        self.body = body




@app.route("/", methods =['GET','POST'])
def display_main_page ():
    return render_template("index.html")    





@app.route('/newpost',methods =['GET','POST'])
def add_entry():
    if request.method == "GET":
        return render_template("newpost.html")
    else: 
        post_title = request.form['post_title']
        body= request.form['body']
        if "" in post_title or "" in body:
            return render_template("index.html")
            flash("Please enter your title or your post")
        elif request.method == 'POST': 
            new_blog = Blog(post_title, body)
            db.session.add(new_blog)
            db.session.commit()                 
            return render_template ("index.html", post_title=post_title,body =body)
    

@app.route('/display', methods =[ 'GET'])
def display_post(post_title, body):
  if request.method  == "POST": 
    blog_id= int(request.args.get('blog_id'))
    blog = Blog.query.filter_by(blog_id)

    return render_template ("display.html",post_title=post_title, body=body )

if __name__ == '__main__':
   app.run()
