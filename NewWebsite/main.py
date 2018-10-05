
from flask import Flask, render_template, request
import pymysql


app = Flask(__name__)
@app.route('/')
def home():
    name = "Harry"

    return render_template('index.html', name_template=name)

@app.route('/about')
def bootstrap():
    return render_template('about.html')

@app.route('/blog')
def blog():
    connection = pymysql.connect(host='localhost', user='root', password='', db='american')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM `posts`")
        all1 = cursor.fetchall()
        print(all1)
        # return str(all1[0][2])
        return render_template('blog.html', var1=all1)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('text')
    connection = pymysql.connect(host='localhost', user='root', password='', db='american')
    with connection.cursor() as cursor:
        # cursor.execute("SELECT * FROM `posts` WHERE title like '%" + query + "%'")
        cursor.execute("SELECT * FROM `posts` WHERE title like '%" + query + "%' OR sno like '%" + query +
                       "%' OR post like '%" + query + "%' OR tags like '%" + query + "%'")
        results = cursor.fetchall()
        if len(results)>0:
            # return results[0][2] # We can display the output in search.html by using any template
            return render_template('search.html', data=results)
        else:
            return "no results found"


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method=='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        subject = request.form.get('subject')
        message = request.form.get('message')
        connection = pymysql.connect(host='localhost', user='root', password='', db='american')
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO `contact` (`name`, `email`, `mobile`, `sub`, `message`) VALUES (%s,%s,%s,%s,%s)",(name,email,mobile,subject,message))
            connection.commit()

    return render_template('contact.html')



app.run(debug=True)