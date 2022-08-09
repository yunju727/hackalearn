from flask import Flask, request, render_template, session, redirect, url_for
import os
import pymysql

app = Flask(__name__)
app.secret_key = os.urandom(24)

users = {
    'guest': 'guest',
    'user': 'user1234',
    'admin': '1'
}

@app.route('/')
def index():
    # html file은 templates 폴더에 위치해야 함
    return render_template('index.html', username=session.get("id"))

@app.route('/login')
def login():
    if "id" in session:
        return render_template("login.html",username=session.get("id"), login = True)
    else:
        return render_template("login.html", login = False)

@app.route('/signin', methods = ["get"])
def signin():
    userid = request.args.get('id')
    passwd = request.args.get('pw')
    
    if passwd == users[userid]:
        session["id"] = userid
        return redirect(url_for("index"))
    else:
        return redirect(url_for("login"))

@app.route('/logout')
def logout():
    session.pop("id")
    return redirect(url_for("login"))

@app.route('/question')
def question():
    db = pymysql.connect(host='us-cdbr-east-06.cleardb.net', port=3306, user='bbc263342cae56', passwd='33c946ea', db='heroku_0a4b1cb2682c753', charset='utf8')
    tag = db.cursor()
    sql = "select * from tag"
    tag.execute(sql)
    result = tag.fetchall()
    db.close()
    return render_template('question.html', tag=result, username=session.get("id"))

@app.route('/answer')
def answer():
    db = pymysql.connect(host='us-cdbr-east-06.cleardb.net', port=3306, user='bbc263342cae56', passwd='33c946ea', db='heroku_0a4b1cb2682c753', charset='utf8')
    article = db.cursor()
    article.execute("select * from articles")
    articles = article.fetchall()
    articles = list(articles)
    db.close()
    return render_template('answer.html', article=articles, username=session.get("id"))

@app.route('/user')
def user():
    return render_template('user.html', username=session.get("id"))

@app.route('/write')
def write():
    return render_template('write.html', username=session.get("id"))

@app.route('/post', methods = ["get", "post"])
def post():
    id = session.get("id")
    if id == None:
        return render_template('errorwrite.html')
    tag = str(request.args.get('tag'))
    title = str(request.args.get('title'))
    content = str(request.args.get('content'))
    db = pymysql.connect(host='us-cdbr-east-06.cleardb.net', port=3306, user='bbc263342cae56', passwd='33c946ea', db='heroku_0a4b1cb2682c753', charset='utf8')
    article = db.cursor()
    article.execute("INSERT INTO articles VALUES(%s, %s, %s, %s, %s)", [None, id, title, content, tag])
    db.commit();
    return redirect(url_for('answer'))
    
@app.route('/detail/<int:post>')
def detail(post):
    idx = int(post)
    db = pymysql.connect(host='us-cdbr-east-06.cleardb.net', port=3306, user='bbc263342cae56', passwd='33c946ea', db='heroku_0a4b1cb2682c753', charset='utf8')
    article = db.cursor()
    sql="select * from articles where MYKEY = %d" %(idx)
    article.execute(sql)
    result = article.fetchall()
    # print(result)
    id = result[0][1]
    tag = result[0][4]
    title = result[0][2]
    content = result[0][3]
    db.close()
    return render_template('detail.html', id=id, tag=tag, title=title, content=content, username=session.get("id"))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080")
