from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import send_file
from flask import jsonify
from flask import session
import os
from datetime import datetime
from flask import redirect
import decimal


SESSION_TYPE = 'redis'
import mysql.connector
import model


SESSION_TYPE = 'redis'
app = Flask(__name__)
app.secret_key = "1234" 
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# Set the maximum size of the uploaded file to 16 MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Set the path to the uploads folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/js/<file>")
def jsfile(file):
    return send_file(file)


@app.route("/img/<file>")
def images(file):
    return send_file("./img/"+file)

@app.route("/css/<file>")
def cssread(file):  
    return send_file(file)
    
@app.route("/uploads/<file>")
def uploadsread(file):  
    return send_file("./uploads/"+file)


@app.route("/")
def firstpage(): 
    if(session.get("idu")==None):
        page="arxiki"
        mnu=""
        usr="" 
    else:
        page="arxiki"
        mnu="user"
    
    return render_template(page+".html", menu=mnu)

@app.route("/admin")
def goadmin(): 
    if(session.get("idu")==None):
        page="admin"
        mnu="admin"
        usr="" 
    else:
        page="404"
        mnu="user"
    
    return render_template(page+".html", menu=mnu)

@app.route("/adminCat")
def adminCat(): 
    if(session.get("idu")==None):
        page="adminCat"
        mnu="admin"
        usr="" 
    else:
        page="404"
        mnu="user"
    
    return render_template(page+".html", menu=mnu)

@app.route("/adminUsr")
def adminUsr(): 
    if(session.get("idu")==None):
        page="adminUsr"
        mnu="admin"
        usr="" 
    else:
        page="404"
        mnu="user"
    
    return render_template(page+".html", menu=mnu)

@app.route("/egrafi")
def egrafi():
    page="egrafi"
    mnu=""
    
    return render_template(page+".html", menu=mnu)


@app.route("/syndesi")
def syndesi():
    page="syndesi"
    mnu=""
    
    return render_template(page+".html", menu=mnu)  

@app.route("/syndesiA")
def syndesiA():
    page="syndesiA"
    mnu=""
    
    return render_template(page+".html", menu=mnu)   

@app.route("/mycontents", methods=['GET', 'POST'])
def mycontents():
    if(session.get("idu")==None):
        page="404"
        mnu=""
        usr="" 
    else:
        page="mycontent"
        mnu="user"
    
    return render_template(page+".html", menu=mnu) 
    
@app.route("/allcontents")
def allcontents():
    if(session.get("idu")==None):
        page="404"
        mnu=""
        usr="" 
    else:
        page="allcontents"
        mnu="user"
    
    return render_template(page+".html", menu=mnu) 

@app.route("/related")
def related():
    if(session.get("idu")==None):
        page="404"
        mnu=""
        usr="" 
    else:
        page="related"
        mnu="user"
    
    return render_template(page+".html", menu=mnu) 

@app.route("/gpt")
def gpt():
    if(session.get("idu")==None):
        page="404"
        mnu=""
        usr="" 
    else:
        page="gpt"
        mnu="user"
    
    return render_template(page+".html", menu=mnu) 
    
@app.route("/users")
def users():
    if(session.get("idu")==None):
        page="404"
        mnu=""
        usr="" 
    else:
        page="users"
        mnu="user"
    
    return render_template(page+".html", menu=mnu) 

@app.route("/notifications")
def notifications():
    if(session.get("idu")==None):
        page="404"
        mnu=""
        usr="" 
    else:
        page="notifications"
        mnu="user"
    
    return render_template(page+".html", menu=mnu) 

@app.route("/bookmarks")
def bookmarks():
    if(session.get("idu")==None):
        page="404"
        mnu=""
        usr="" 
    else:
        page="bookmarks"
        mnu="user"
    
    return render_template(page+".html", menu=mnu) 


@app.route("/uploadfile",  methods=['POST', 'GET'])
def uploadfile(): 
    
    if(session.get("idu")==None):
        return jsonify({"done": "false"}) 
    else:
        try:
            c=model.Content()
            p={}
            p["iduser"]=session.get("idu")
            p["filename"]=""
            p["title"]=request.form.get('title')
            p["id"]=0
            c.set(p)
            c.uploadfile(request.files["filename"])
            c.insertdb()
            return jsonify({"done": "true"}) 
        except:
            return jsonify({"done": "false"})
        
    
@app.route("/egrafi2",  methods=['POST', 'GET'])
def egrafi2():
    email=request.form.get('email')
    password=request.form.get('password')
    phone=request.form.get('phone')
    name=request.form.get('name')
    bio=request.form.get('bio')
    location=request.form.get('location')
    field=request.form.get('field')
    birth=request.form.get('birth')
    p={}
    p['email']=email
    p['password']=password
    p['phone']=phone
    p['name']=name
    p['bio']=bio
    p['location']=location
    p['field']=field
    p['birth']=birth
    
    print(p)
    u=model.User()
    u.set(p)
    try:
        u.insertdb()
        done="true"
    except:
        done="false"
        
    return jsonify({"done": done})



@app.route("/syndesi2", methods=['POST', 'GET'])
def syndesi2():
    if request.method == 'POST':
        e=str(request.form.get('email'))
        p=str(request.form.get('password'))
       
        try:
            u=model.User()
            u.setUserByUsrPss(e,p)
            session['idu']=u.id
            return jsonify({"done": "true"})
        except:
            session['idu']=None
            return jsonify({"done": "false"})
        
@app.route("/syndesi2A", methods=['POST', 'GET'])
def syndesi2A():
    if request.method == 'POST':
        e = str(request.form.get('email'))
        p = str(request.form.get('password'))

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset='utf8'
        )

        # Create cursor
        mycursor = mydb.cursor()
        sql = "select * from admin where email='"+e+"' and password='"+p+"'"
        try:
            mycursor.execute(sql)
            r = mycursor.fetchone()
            if r is not None:
                # Create a dictionary with user details
                user = {
                    'email': r[0],
                    'password': r[1],
                    'id': str(r[2])
                }
                return jsonify({'done': 'true', 'user': user})
            else:
                return jsonify({'done': 'false'})
        except:
            raise Exception("Not found")

    # If request method is GET, render the login form
    return render_template('admin.html')

@app.route("/logout")
def logout():
    session['idu']=None
    page="arxiki"
    mnu=""
    usr="" 
    return render_template(page+".html", menu=mnu)


@app.route("/mycontents2")
def mycontents2():
     c=model.Content()
     A=c.getUserAll(session['idu'])
     print(A)
     return jsonify(A)

# @app.route("/mycontents3")
# def mycontents3():
#      c=model.Content()
#      A=c.getAll()
#      print(A)
#      return jsonify(A)   

@app.route("/listusers")
def listusers():
     u=model.User()
     A=u.getAll()
     print(A)
     return jsonify(A) 
     

    
@app.route("/profileUpdate", methods=["POST"])
def profileUpdate():
        try:
            user_id = request.form.get("user_id")
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            bio = request.form.get("bio")
            phone = request.form.get("phone")
            location = request.form.get("location")
            field = request.form.get("field")
            
            # Connect to the database
            mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="usercontentdb",
                    port="3308",
                    charset='utf8')

            # Create cursor
            mycursor = mydb.cursor()

            # Update user profile in the database
            if password != "":
                sql2 = f"update users set email='{email}', name='{name}', password='{password}', location='{location}',  bio='{bio}', field='{field}', phone='{phone}' where id='{user_id}'"
            
            else:
                sql2 = f"update users set email='{email}', name='{name}', location='{location}',  bio='{bio}', field='{field}', phone='{phone}' where id='{user_id}'"
            mycursor.execute(sql2)
            mydb.commit()
            return "true" 
            
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return jsonify({"error": "An error occurred while updating your profile. Please try again later."}), 500
        
        
@app.route('/statusUpload', methods=['POST'])
def handle_status_upload():
    try:
        user_id = session.get("idu")
        title = request.form['title']
        public = str(request.form['public'])
        category = str(request.form['category'])
        file = request.files.get("file-upload")
        filename = ''
        filetype = ''
        if file is not None:
            # Generate a unique filename for the uploaded file
            filename = f"file_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}{os.path.splitext(file.filename)[1]}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Save the uploaded file to disk
            file.save(filepath)
            # Get the file type based on the file extension
            filetype = os.path.splitext(file.filename)[1][1:].lower()  # e.g. 'png', 'pdf', 'txt'
        
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset='utf8'
        )

        # Create cursor
        mycursor = mydb.cursor()

        if filename != "":
            # Update user profile in the database with file
            sql2="insert into content set filename='"+filename+"',"
            sql2=sql2+"title='"+title+"',"
            sql2=sql2+"public='"+str(public)+"',"
            sql2=sql2+"type='"+filetype+"',"
            sql2=sql2+"category='"+category+"',"
            sql2=sql2+"date=NOW(),"
            sql2=sql2+"iduser='"+user_id+"'"
        else:
            # Update user profile in the database without file
            sql2="insert into content set title='"+title+"',"
            sql2=sql2+"public='"+str(public)+"',"
            sql2=sql2+"category='"+category+"',"
            sql2=sql2+"date=NOW(),"
            sql2=sql2+"iduser='"+user_id+"'"
        mycursor.execute(sql2)
        mydb.commit()

        # Get the ID of the last inserted content
        content_id = mycursor.lastrowid

        # Get the ID of the category associated with the content
        sql3 = "SELECT id FROM categories WHERE name=%s"
        mycursor.execute(sql3, (category,))
        category_id = mycursor.fetchone()[0]

        # Insert a new row in categories_rel table
        sql4 = "INSERT INTO categories_rel (id_category, id_cont, date) VALUES (%s, %s, NOW())"
        values = (category_id, content_id)
        mycursor.execute(sql4, values)
        mydb.commit()

        return "true"
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": "An error occurred while updating your profile. Please try again later."}), 500





@app.route("/profilePhotoUpload",  methods=['POST', 'GET'])
def profilePhotoUpload(): 
    if(session.get("idu")==None):
        return jsonify({"done": "false"}) 
    else:
        try:
            user_id = session.get("idu")
            profilephoto = request.files.get("file1")
            
            # Generate a unique filename for the uploaded file
            filename = f"profilephoto_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.{profilephoto.filename.split('.')[-1]}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            profilephoto.save(filepath)
            
            
                        
            # Connect to the database
            mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="usercontentdb",
                    port="3308",
                    charset='utf8')

            # Create cursor
            mycursor = mydb.cursor()

            # Update user profile in the database
           
            sql2 = f"update users set profilephoto='{filename}' where id='{user_id}'"            
            mycursor.execute(sql2)
            mydb.commit()
            return "true" 
            
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return jsonify({"error": "An error occurred while updating your profile. Please try again later."}), 500



@app.route("/userdata")
def userdata():
    user_id = session.get("idu")
    if user_id:
            # Connect to the database
            mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="usercontentdb",
                    port="3308",
                    charset='utf8')
            mycursor=mydb.cursor()
            sql="select * from users where id="+str(user_id)
            try:
                mycursor.execute(sql)
                r=mycursor.fetchone()
                p={}
                p['email']=r[1]
                p['password']=r[3]
                p['phone']=r[2]
                p['name']=r[4]
                p['bio']=r[5]
                p['location']=r[6]
                p['field']=r[7]
                p['birth']=r[8]
                p['profilephoto']=r[9]
                p['id']=str(r[0])
                return p
            except:
                raise Exception("No found")
    else:
        return jsonify({"error": "User not found"}), 401
    
@app.route("/contentdata")
def contentdata():
    user_id = session.get("idu")
    if user_id:
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset='utf8')
        mycursor=mydb.cursor()
        sql="""SELECT c.id, c.iduser, c.filename, c.title, u.name, u.profilephoto, c.date, c.likes, c.saves, c.views
               FROM content c
               JOIN users u ON c.iduser = u.id"""
        try:
            mycursor.execute(sql)
            results = mycursor.fetchall()
            data = []
            for row in results:
                item = {}
                item['id_cont'] = str(row[0])
                item['iduser'] = str(row[1])
                item['filename'] = row[2]
                item['title'] = row[3]
                item['name'] = row[4]
                item['profilephoto'] = row[5]
                item['date'] = str(row[6])  # Convert date to string
                item['likes'] = str(row[7])
                item['saves'] = str(row[8])
                item['views'] = str(row[9])
                data.append(item)
            return jsonify(data)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return jsonify({"error": "An error occurred while fetching the content data."}), 500
    else:
        return jsonify({"error": "User not found"}), 401


@app.route("/bestposts")
def bestposts():
    user_id = session.get("idu")
    if not user_id:
        return jsonify({"error": "User not found"}), 401
    
    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="usercontentdb",
        port="3308",
        charset='utf8')
    mycursor = mydb.cursor()

    # Step 1: Get the ID of the current user.
    sql = """SELECT birth FROM users WHERE id = %s"""
    mycursor.execute(sql, (user_id,))
    result = mycursor.fetchone()
    if not result:
        return jsonify({"error": "User not found in the database"}), 401
    user_birth = result[0]
    
    
    # Step 2: Get the content relavance
    sql = """
        SELECT content.id, content.filename, content.title,
           SUM(CASE
               WHEN categories_rel.id_category IN (
                   SELECT cr.id_category
                   FROM categories_rel cr
                   WHERE cr.id_user = %s
               ) THEN 1
               ELSE 0
           END) AS content_rel
    FROM content
    INNER JOIN categories_rel ON content.id = categories_rel.id_cont
    GROUP BY content.id, content.filename, content.title
        """
    mycursor.execute(sql, (user_id,))
    content_rel = mycursor.fetchall()
    
    # Step 5: For each content, calculate the score using the formula and return the content sorted by score in descending order.
    sql = """
    SELECT c.id, c.iduser, c.filename, c.title, u.name, u.profilephoto, c.date, c.likes, c.saves, c.views,
        TIMESTAMPDIFF(YEAR, u.birth, %s) AS user_age,
        cl.category, cl.score AS likes_score, cs.score AS saves_score
    FROM content c
    JOIN users u ON c.iduser = u.id
    JOIN (
        SELECT category, SUM(likes) AS score
        FROM content
        GROUP BY category
    ) cl ON c.category = cl.category
    JOIN (
        SELECT category, SUM(saves) AS score
        FROM content
        GROUP BY category
    ) cs ON c.category = cs.category
"""
    mycursor.execute(sql, (user_birth,))
    results = mycursor.fetchall()
    data = []
    # Get column names
    columns = [desc[0] for desc in mycursor.description]
    
    # Step 6: Calculate the number of followers for each user
    followers_query = """
        SELECT idu2 AS user_id, COUNT(*) AS follower_count
        FROM user_rel
        WHERE type = 'following'
        GROUP BY idu2
    """
    mycursor.execute(followers_query)
    followers_results = mycursor.fetchall()
    followers_data = {row[0]: row[1] for row in followers_results}

    for row in results:
        rel = next((x for x in content_rel if x[0] == row[0]), None)
        if rel is None:
            continue
        item = {}

        # Convert the result row into a dictionary-like object
        row_dict = dict(zip(columns, row))

        item['id_cont'] = str(row_dict['id'])
        item['iduser'] = str(row_dict['iduser'])
        item['filename'] = row_dict['filename']
        item['title'] = row_dict['title']
        item['name'] = row_dict['name']
        item['profilephoto'] = row_dict['profilephoto']
        item['date'] = str(row_dict['date'])
        item['likes'] = str(row_dict['likes'])
        item['saves'] = str(row_dict['saves'])
        item['views'] = str(row_dict['views'])

        post_likes = int(row_dict['likes'])
        post_saves = int(row_dict['saves'])
        post_views = int(row_dict['views'])

        user_id = row_dict['iduser']
        users_post_followers = followers_data.get(user_id, 0)  # Get the follower count for the user

        content_category_likes = int(row_dict['likes_score']) * 3  # Multiply likes_score by the weight 
        content_category_saves = int(row_dict['saves_score']) * 6  # Multiply saves_score by the weight 

        content_rel_value = rel[0]
        content_score = (25 * content_rel_value +
                        content_category_likes +
                        content_category_saves +
                        (post_likes * 5 / users_post_followers) +
                        (post_saves * 10 / users_post_followers) +
                        (post_views * 1.2 / users_post_followers))

        item['score'] = content_score
        print(f"content_score: {content_score}")

        data.append(item)


        
    # Sort the content by score in descending order
    data = sorted(data, key=lambda k: k['score'], reverse=True)
    
    return jsonify(data)



@app.route("/contentdataProfile")
def contentdataProfile():
    user_id = session.get("idu")
    if user_id:
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset='utf8')
        mycursor=mydb.cursor()
        sql = """SELECT c.iduser, c.filename, c.title, u.name, u.profilephoto, c.date, c.id
                 FROM content c
                 JOIN users u ON c.iduser = u.id
                 WHERE c.iduser = %s"""
        try:
            mycursor.execute(sql, (user_id,))
            results = mycursor.fetchall()
            data = []
            for row in results:
                item = {}
                item['iduser'] = str(row[0])
                item['filename'] = row[1]
                item['title'] = row[2]
                item['name'] = row[3]
                item['profilephoto'] = row[4]
                item['date'] = str(row[5])  # Convert date to string
                item['id'] = str(row[6])  # Convert date to string
                data.append(item)
            return jsonify(data)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return jsonify({"error": "An error occurred while fetching the content data."}), 500
    else:
        return jsonify({"error": "User not found"}), 401
    
@app.route("/likedContent")
def likedContent():
    user_id = session.get("idu")
    if user_id:
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset='utf8')
        mycursor=mydb.cursor()
        sql = """SELECT c.id, c.iduser, c.filename, c.title, u.name, u.profilephoto, c.date, c.likes, c.saves
                 FROM content c
                 JOIN users u ON c.iduser = u.id
                 JOIN content_rel cr ON c.id = cr.id_cont
                 WHERE cr.id_user = %s AND cr.type = 'like'"""
        try:
            mycursor.execute(sql, (user_id,))
            results = mycursor.fetchall()
            data = []
            for row in results:
                item = {}
                item['id'] = str(row[0])
                item['iduser'] = str(row[1])
                item['filename'] = row[2]
                item['title'] = row[3]
                item['name'] = row[4]
                item['profilephoto'] = row[5]
                item['date'] = str(row[6])  # Convert date to string
                item['likes'] = row[7]
                item['saves'] = row[8]
                data.append(item)
            return jsonify(data)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return jsonify({"error": "An error occurred while fetching the content data."}), 500
    else:
        return jsonify({"error": "User not found"}), 401
    
@app.route("/savedContent")
def savedContent():
    user_id = session.get("idu")
    if user_id:
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset='utf8')
        mycursor=mydb.cursor()
        sql = """SELECT c.id, c.iduser, c.filename, c.title, u.name, u.profilephoto, c.date, c.likes, c.saves
                 FROM content c
                 JOIN users u ON c.iduser = u.id
                 JOIN content_rel cr ON c.id = cr.id_cont
                 WHERE cr.id_user = %s AND cr.type = 'save'"""
        try:
            mycursor.execute(sql, (user_id,))
            results = mycursor.fetchall()
            data = []
            for row in results:
                item = {}
                item['id'] = str(row[0])
                item['iduser'] = str(row[1])
                item['filename'] = row[2]
                item['title'] = row[3]
                item['name'] = row[4]
                item['profilephoto'] = row[5]
                item['date'] = str(row[6])  # Convert date to string
                item['likes'] = row[7]
                item['saves'] = row[8]
                data.append(item)
            return jsonify(data)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return jsonify({"error": "An error occurred while fetching the content data."}), 500
    else:
        return jsonify({"error": "User not found"}), 401

@app.route("/likedcontentdataProfile/<int:id>")
def likedcontentdataProfile(id):
    user_id = id
    if user_id:
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset='utf8')
        mycursor=mydb.cursor()
        sql = """SELECT c.id, c.iduser, c.filename, c.title, u.name, u.profilephoto, c.date, c.likes, c.saves
                 FROM content c
                 JOIN users u ON c.iduser = u.id
                 JOIN content_rel cr ON c.id = cr.id_cont
                 WHERE cr.id_user = %s AND cr.type = 'like'"""
        try:
            mycursor.execute(sql, (user_id,))
            results = mycursor.fetchall()
            data = []
            for row in results:
                item = {}
                item['id'] = str(row[0])
                item['iduser'] = str(row[1])
                item['filename'] = row[2]
                item['title'] = row[3]
                item['name'] = row[4]
                item['profilephoto'] = row[5]
                item['date'] = str(row[6])  # Convert date to string
                item['likes'] = row[7]
                item['saves'] = row[8]
                data.append(item)
            return jsonify(data)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return jsonify({"error": "An error occurred while fetching the content data."}), 500
    else:
        return jsonify({"error": "User not found"}), 401


@app.route('/profile/<int:user_id>')
def get_user_profile(user_id):
    # Connect to the database
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset='utf8')
    mycursor=mydb.cursor()

    sql2 = "SELECT * FROM users WHERE id=%s"
    try:
        mycursor.execute(sql2, (user_id,))
        results = mycursor.fetchall()
        if len(results) == 0:
            page="404"
            mnu=""
            usr="" 
            return render_template(page+".html", menu=mnu)
        user_data = {}
        for row in results:
            user_data['iduser'] = str(row[0])
            user_data['filename'] = row[1]
            user_data['title'] = row[2]
            user_data['name'] = row[3]
            user_data['profilephoto'] = row[4]
            user_data['date'] = str(row[5])  # Convert date to string
            page="profile"
            mnu="user"
        return render_template(page+".html", menu=mnu,user_data=user_data)
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return render_template('404.html')

@app.route("/profile1/<int:id>")
def profile(id):
    user_id = id
    if user_id:
            # Connect to the database
            mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="usercontentdb",
                    port="3308",
                    charset='utf8')
            mycursor=mydb.cursor()
            sql="select * from users where id="+str(user_id)
            try:
                mycursor.execute(sql)
                r=mycursor.fetchone()
                p={}
                p['email']=r[1]
                p['password']=r[3]
                p['phone']=r[2]
                p['name']=r[4]
                p['bio']=r[5]
                p['location']=r[6]
                p['field']=r[7]
                p['birth']=r[8]
                p['profilephoto']=r[9]
                p['id']=str(r[0])
                return p
            except:
                raise Exception("No found")
    else:
        return jsonify({"error": "User not found"}), 401
    
@app.route("/contentdataProfile1/<int:id>")
def contentdataProfile1(id):
    user_id = id
    if user_id:
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset='utf8')
        mycursor=mydb.cursor()
        sql = """SELECT c.iduser, c.filename, c.title, u.name, u.profilephoto, c.date
                 FROM content c
                 JOIN users u ON c.iduser = u.id
                 WHERE c.iduser = %s"""
        try:
            mycursor.execute(sql, (user_id,))
            results = mycursor.fetchall()
            data = []
            for row in results:
                item = {}
                item['iduser'] = str(row[0])
                item['filename'] = row[1]
                item['title'] = row[2]
                item['name'] = row[3]
                item['profilephoto'] = row[4]
                item['date'] = str(row[5])  # Convert date to string
                data.append(item)
            return jsonify(data)
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return jsonify({"error": "An error occurred while fetching the content data."}), 500
    else:
        return jsonify({"error": "User not found"}), 401


@app.route("/folow/<int:id>", methods=['POST'])
def follow(id):
    user_id = id
    if user_id:
            # Connect to the database
            mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="usercontentdb",
                    port="3308",
                    charset='utf8')
            mycursor=mydb.cursor()
            user_id1 = session.get("idu")
            tp = "following"
            sql2="insert into user_rel set idu1='"+ str(user_id1) +"',"
            sql2=sql2+"idu2='"+ str(user_id) +"',"
            sql2=sql2+"date1=NOW(),"
            sql2=sql2+"type='"+tp+"'"
            print("id1: ", user_id)
            print("id2: ", user_id1)
            try:
                mycursor.execute(sql2)
                mydb.commit()
                return "1"
            except:
                raise Exception("No found")
    else:
        return jsonify({"error": "User not found"}), 401

@app.route("/unfolow/<int:id>", methods=['POST'])
def unfollow(id):
    user_id = id
    if user_id:
            # Connect to the database
            mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="usercontentdb",
                    port="3308",
                    charset='utf8')
            mycursor=mydb.cursor()
            user_id1 = session.get("idu")
            tp = "following"
            sql2 = "DELETE FROM user_rel WHERE idu1='" + str(user_id1) + "' AND idu2='" + str(user_id) + "' AND type='" + tp + "'"
            try:
                mycursor.execute(sql2)
                mydb.commit()
                return "1"
            except:
                raise Exception("No found")
    else:
        return jsonify({"error": "User not found"}), 401

@app.route("/showfollow/<int:id>", methods=['GET'])
def showfollow(id):
    user_id = id
    if user_id:
        # Connect to the database
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usercontentdb",
                port="3308",
                charset='utf8')
        mycursor=mydb.cursor()
        user_id1 = session.get("idu")
        tp = "following"
        sql2 = "select * FROM user_rel WHERE idu1='" + str(user_id1) + "' AND idu2='" + str(user_id) + "' AND type='" + tp + "'"
        try:
            mycursor.execute(sql2)
            results = mycursor.fetchall()
            data = {}
            data['following'] = False
            if len(results) > 0:
                data['following'] = True
            return jsonify(data)
        except:
            raise Exception("No found")
    else:
        return jsonify({"error": "User not found"}), 401
    
@app.route("/countfollow/<int:id>", methods=['GET'])
def countfollow(id):
    user_id = id
    if user_id:
        # Connect to the database
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usercontentdb",
                port="3308",
                charset='utf8')
        mycursor=mydb.cursor()
        # Count followers
        sql1 = "SELECT COUNT(*) FROM user_rel WHERE idu2='" + str(user_id) + "' AND type='following'"
        mycursor.execute(sql1)
        followers = mycursor.fetchone()[0]
        # Count following
        sql2 = "SELECT COUNT(*) FROM user_rel WHERE idu1='" + str(user_id) + "' AND type='following'"
        mycursor.execute(sql2)
        following = mycursor.fetchone()[0]
        # Close database connection
        mydb.close()
        # Return results
        data = {"followers": followers, "following": following}
        return jsonify(data)
    else:
        return jsonify({"error": "User not found"}), 401
    
@app.route("/followersprofile", methods=['GET'])
def followersprofile():
    user_id = session.get("idu")
    if user_id:
        # Connect to the database
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usercontentdb",
                port="3308",
                charset='utf8')
        mycursor=mydb.cursor()
        # Count followers
        sql1 = "SELECT COUNT(*) FROM user_rel WHERE idu2='" + str(user_id) + "' AND type='following'"
        mycursor.execute(sql1)
        followers = mycursor.fetchone()[0]
        # Count following
        sql2 = "SELECT COUNT(*) FROM user_rel WHERE idu1='" + str(user_id) + "' AND type='following'"
        mycursor.execute(sql2)
        following = mycursor.fetchone()[0]
        # Close database connection
        mydb.close()
        # Return results
        data = {"followers": followers, "following": following}
        return jsonify(data)
    else:
        return jsonify({"error": "User not found"}), 401

@app.route("/like", methods=['POST'])
def like():
    user_id = session.get("idu")
    cont_id = request.form.get('id_cont')
    if user_id and cont_id:
        # Connect to the database
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usercontentdb",
                port="3308",
                charset='utf8')
        mycursor=mydb.cursor()
        
        # Update the likes count in the content table
        sql1 = "UPDATE content SET likes = likes + 1 WHERE id = %s"
        values1 = (cont_id,)
        try:
            mycursor.execute(sql1, values1)
            mydb.commit()
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return "false"
        
        # Add a record to the content_rel table
        sql2 = "INSERT INTO content_rel (id_cont, id_user, type, date1) VALUES (%s, %s, %s, NOW())"
        values2 = (cont_id, user_id, "like")
        try:
            mycursor.execute(sql2, values2)
            mydb.commit()
            return "true"
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return "false"
    else:
        return jsonify({"error": "User or content not found"}), 401
    
@app.route("/view", methods=['POST'])
def view():
    user_id = session.get("idu")
    cont_id = request.json.get('id_cont')  # get id_cont from JSON data in request
    if user_id and cont_id:
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset='utf8')
        mycursor = mydb.cursor()

        # Update the views count in the content table
        sql1 = "UPDATE content SET views = views + 1 WHERE id = %s"
        values1 = (cont_id,)
        try:
            mycursor.execute(sql1, values1)
            mydb.commit()
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return "false"

        # Add a record to the content_rel table
        sql2 = "INSERT INTO content_rel (id_cont, id_user, type, date1) VALUES (%s, %s, %s, NOW())"
        values2 = (cont_id, user_id, "view")
        try:
            mycursor.execute(sql2, values2)
            mydb.commit()
            return jsonify({"views": mycursor.rowcount})  # return number of rows affected by INSERT query
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return "false"
    else:
        return jsonify({"error": "User or content not found"}), 401

    
@app.route("/unlike", methods=['POST'])
def unlike():
    user_id = session.get("idu")
    cont_id = request.form.get('id_cont')
    if user_id and cont_id:
        # Connect to the database
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usercontentdb",
                port="3308",
                charset='utf8')
        mycursor=mydb.cursor()
        
        # Update the likes count in the content table
        sql1 = "UPDATE content SET likes = likes - 1 WHERE id = %s"
        values1 = (cont_id,)
        try:
            mycursor.execute(sql1, values1)
            mydb.commit()
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return "false"
        
        # Remove the record from the content_rel table
        sql2 = "DELETE FROM content_rel WHERE id_cont = %s AND id_user = %s AND type = 'like'"
        values2 = (cont_id, user_id)
        try:
            mycursor.execute(sql2, values2)
            mydb.commit()
            return "true"
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return "false"
    else:
        return jsonify({"error": "User or content not found"}), 401

    

@app.route("/showLike", methods=['GET'])
def showLike():
    user_id = session.get("idu")
    if user_id:
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset='utf8')
        mycursor=mydb.cursor()
        tp = "like"
        sql2 = "SELECT id_cont FROM content_rel WHERE id_user = %s AND type = %s"
        try:
            mycursor.execute(sql2, (user_id, tp))
            results = mycursor.fetchall()
            data = {}
            data['liked_posts'] = [row[0] for row in results]
            return jsonify(data)
        except:
            raise Exception("No found")
    else:
        return jsonify({"error": "User not found"}), 401
    
    
@app.route("/save", methods=['POST'])
def save():
    user_id = session.get("idu")
    cont_id = request.form.get('id_cont')
    if user_id and cont_id:
        # Connect to the database
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usercontentdb",
                port="3308",
                charset='utf8')
        mycursor=mydb.cursor()
        
        # Update the likes count in the content table
        sql1 = "UPDATE content SET saves = saves + 1 WHERE id = %s"
        values1 = (cont_id,)
        try:
            mycursor.execute(sql1, values1)
            mydb.commit()
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return "false"
        
        # Add a record to the content_rel table
        sql2 = "INSERT INTO content_rel (id_cont, id_user, type, date1) VALUES (%s, %s, %s, NOW())"
        values2 = (cont_id, user_id, "save")
        try:
            mycursor.execute(sql2, values2)
            mydb.commit()
            return "true"
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return "false"
    else:
        return jsonify({"error": "User or content not found"}), 401
    
    
@app.route("/unsave", methods=['POST'])
def unsave():
    user_id = session.get("idu")
    cont_id = request.form.get('id_cont')
    if user_id and cont_id:
        # Connect to the database
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usercontentdb",
                port="3308",
                charset='utf8')
        mycursor=mydb.cursor()
        
        # Update the likes count in the content table
        sql1 = "UPDATE content SET saves = saves - 1 WHERE id = %s"
        values1 = (cont_id,)
        try:
            mycursor.execute(sql1, values1)
            mydb.commit()
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return "false"
        
        # Remove the record from the content_rel table
        sql2 = "DELETE FROM content_rel WHERE id_cont = %s AND id_user = %s AND type = 'save'"
        values2 = (cont_id, user_id)
        try:
            mycursor.execute(sql2, values2)
            mydb.commit()
            return "true"
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return "false"
    else:
        return jsonify({"error": "User or content not found"}), 401
    
@app.route("/showSaved", methods=['GET'])
def showSaved():
    user_id = session.get("idu")
    if user_id:
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset='utf8')
        mycursor=mydb.cursor()
        tp = "save"
        sql2 = "SELECT id_cont FROM content_rel WHERE id_user = %s AND type = %s"
        try:
            mycursor.execute(sql2, (user_id, tp))
            results = mycursor.fetchall()
            data = {}
            data['saved_posts'] = [row[0] for row in results]
            return jsonify(data)
        except:
            raise Exception("No found")
    else:
        return jsonify({"error": "User not found"}), 401


# chat route fuunctions
# create chat
@app.route("/gotoChat/<int:user_id>", methods=["POST"])
def goto_chat(user_id):
    if not session.get("idu"):
        return jsonify({"error": "User not found"}), 401
    
    id1 = session.get("idu")
    id2 = user_id
    f = 0
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if id1 != id2:
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset='utf8')
        mycursor = mydb.cursor()

        sql0 = f"SELECT DISTINCT id_conv FROM conv_users WHERE id_user={id1}"
        mycursor.execute(sql0)
        results = mycursor.fetchall()

        for r in results:
            sql00 = f"SELECT * FROM conv_users WHERE id_conv={r[0]} AND id_user={id2}"
            mycursor.execute(sql00)
            q2 = mycursor.fetchall()
            if len(q2) > 0:
                f = r[0]
                break

        if f == 0:
            sql1 = f"INSERT INTO conversation SET date_start='{dt}', last_date='{dt}', user_start='{id1}'"
            mycursor.execute(sql1)
            mydb.commit()
            idc = mycursor.lastrowid

            sql2 = f"INSERT INTO conv_users SET id_user='{id2}', insert_date='{dt}', id_conv={idc}, active=0"
            mycursor.execute(sql2)

            sql2 = f"INSERT INTO conv_users SET id_user='{id1}', insert_date='{dt}', id_conv={idc}, active=1"
            mycursor.execute(sql2)

            mydb.commit()
            f = idc
            
    return redirect(url_for('users', chat_id=f))


#use chat 
@app.route('/get_convs', methods=['GET'])
def get_convs():
    user_id = session.get("idu")
    if not user_id:
        return jsonify({"error": "User not found"}), 401
        
    # Connect to the database
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset='utf8')
    cursor = mydb.cursor()
    cv = request.args.get('cv', default='')
    if cv != '':
        sql21 = "SELECT * FROM conversation WHERE id = %s"
        cursor.execute(sql21, (cv,))
        js1 = cursor.fetchone()
        if not js1:
            return jsonify({"error": "Conversation not found"}), 404
    else:
        sql21 = "SELECT * FROM conversation WHERE id IN (SELECT DISTINCT id_conv FROM conv_users WHERE id_user = %s) ORDER BY last_date DESC LIMIT 0, 1"
        cursor.execute(sql21, (user_id,))
        js1 = cursor.fetchone()
        if not js1:
            return jsonify({"error": "Conversation not found"}), 404
        cv = js1[0]

    sql23 = "SELECT * FROM conversation WHERE id <> %s AND id IN (SELECT DISTINCT id_conv FROM conv_users WHERE id_user = %s) ORDER BY last_date DESC"
    cursor.execute(sql23, (cv, user_id,))
    js3 = cursor.fetchall()

    convs = []
    for row in js3:
        conv = {}
        conv['id'] = row[0]
        conv['last_msg'] = row[1]
        conv['last_date'] = row[2].strftime("%Y-%m-%d %H:%M:%S")
        convs.append(conv)

    data = {}
    data['firstconv'] = {
        'id': js1[0],
        'last_msg': js1[1],
        'last_date': js1[2].strftime("%Y-%m-%d %H:%M:%S")
    }
    data['convs'] = convs

    return jsonify(data)

@app.route("/showConvUsers/<int:cv>", methods=['GET'])
def showConvUsers(cv):
    user_id = session.get("idu")
    if user_id:
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset='utf8')
        mycursor = mydb.cursor()
        
        sql = "SELECT * FROM conv_users INNER JOIN users ON users.id = conv_users.id_user WHERE id_user <> %s AND id_conv = %s"
        try:
            mycursor.execute(sql, (user_id, cv))
            results = mycursor.fetchall()
            print(results)  # print query results
            data = {}
            data['conv_users'] = []
            for row in results:
                user = {
                    'id': row[4],
                    'name': row[8],
                    'email': row[5],
                    'image': row[13]
                }
                data['conv_users'].append(user)
            return jsonify(data)
        except:   
            raise Exception("No data found")
            
    else:
        return jsonify({"error": "User not found"}), 401

  
@app.route("/showMessages/<int:cv>", methods=['GET'])
def showMessages(cv):
    user_id = session.get("idu")
    if user_id:
        # Connect to the database
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usercontentdb",
                port="3308",
                charset='utf8')
        mycursor=mydb.cursor()
        # sql22 = "SELECT *, %s - id_user as isnotme FROM messages WHERE id_conv = %s"

        sql22 = "SELECT *, id_user- %s as isnotme FROM messages WHERE id_conv = %s"
        try:
                mycursor.execute(sql22, (user_id, cv))
                results = mycursor.fetchall()
                data = {}
                data['messages'] = [{'id': row[0], 'id_user': row[1], 'text': row[2], 'id_conv': row[3], 'timestamp': row[4], 'isnotme': row[5]} for row in results]
                return jsonify(data)
        except:
                raise Exception("No found")
       
    else:
        return jsonify({"error": "User not found"}), 401
    
@app.route("/sendMessage", methods=['POST'])
def sendMessage():
    user_id = session.get("idu")
    if user_id:
        # Connect to the database
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usercontentdb",
                port="3308",
                charset='utf8')
        mycursor=mydb.cursor()
        
        data = request.get_json()
        cv = data.get('cv')
        msg = data.get('msg')
        
        sql203 = "INSERT INTO messages SET id_conv = %s, id_user = %s, message = %s, date_send = now(), isread = ''"
        try:
                mycursor.execute(sql203, (cv, user_id, msg))
                mydb.commit()
                return jsonify({"success": True}), 200
        except:
                mydb.rollback()
                raise Exception("No found")
    else:
        return jsonify({"error": "User not found"}), 401
    
#users search
@app.route("/searchuser")
def searchuser():
    user_id = session.get("idu")
    if user_id:
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset='utf8')
        mycursor = mydb.cursor()
        sql = "SELECT * FROM users"
        try:
            mycursor.execute(sql)
            r = mycursor.fetchall()
            if not r:
                return jsonify({"error": "No users found"}), 404
            else:
                user_list = []
                for row in r:
                    user = {}
                    user['id'] = str(row[0])
                    user['name'] = row[4]
                    user['profilephoto'] = row[9]
                    user_list.append(user)

                return jsonify(user_list), 200
        except:
            raise Exception("No found")
    else:
        return jsonify({"error": "User not found"}), 401


#admin actions
@app.route("/addcategory", methods=['POST'])
def addcategory():
    if request.method == 'POST':
        c = str(request.form.get('add_categ'))
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset='utf8'
        )
        # Create cursor
        mycursor = mydb.cursor()
        sql = "INSERT INTO categories SET name = %s"
        try:
            mycursor.execute(sql, (c,))
            mydb.commit()
            return jsonify({"done": True}), 200
        except:
            return jsonify({"done": False}), 500
    else:
        return jsonify({"error": "User not found"}), 401
    
#admin actions
#admin actions
@app.route("/addAdmin", methods=['POST'])
def addAdmin():
    if request.method == 'POST':
        e = str(request.form.get('email'))
        p = str(request.form.get('password'))
        
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset='utf8'
        )
        # Create cursor
        mycursor = mydb.cursor()        
        sql = "INSERT INTO admin (email, password) VALUES (%s, %s)"
        values = (e, p)
        print(sql)
        try:
            mycursor.execute(sql, values)
            
            mydb.commit()
            return jsonify({"done": True}), 200
        except:
            return jsonify({"done": False}), 500
    else:
        return jsonify({"error": "User not found"}), 401

# Get all categories
@app.route("/categoryContent", methods=['GET'])
def get_categories():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="usercontentdb",
        port="3308",
        charset='utf8'
    )

    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT id, name FROM categories"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return jsonify(result), 200

# Get all categories
@app.route("/usersContent", methods=['GET'])
def usersContent():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="usercontentdb",
        port="3308",
        charset='utf8'
    )

    mycursor = mydb.cursor(dictionary=True)
    sql = "SELECT id, name FROM users"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return jsonify(result), 200

# Delete a category by id
@app.route("/delCategory/<int:id>", methods=['GET'])
def delete_category(id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="usercontentdb",
        port="3308",
        charset='utf8'
    )

    mycursor = mydb.cursor()
    sql = "DELETE FROM categories WHERE id = %s"
    val = (id,)
    try:
        mycursor.execute(sql, val)
        mydb.commit()
        return jsonify("true"), 200
    except:
        return jsonify("false"), 500
    
# Delete a category by id
@app.route("/delUsr/<int:id>", methods=['GET'])
def delete_Usr(id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="usercontentdb",
        port="3308",
        charset='utf8'
    )

    mycursor = mydb.cursor()
    sql = "DELETE FROM users WHERE id = %s"
    val = (id,)
    try:
        mycursor.execute(sql, val)
        mydb.commit()
        return jsonify("true"), 200
    except:
        return jsonify("false"), 500
    

@app.route("/addCategory/<int:id>", methods=['GET'])
def addCategory(id):
    user_id = session.get("idu")

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="usercontentdb",
        port="3308",
        charset='utf8'
    )

    mycursor = mydb.cursor()
    sql = "INSERT INTO categories_rel (id_category, id_user, date) VALUES (%s, %s, NOW())"
    values = (id, user_id)

    try:
        mycursor.execute(sql, values)
        mydb.commit()
        return jsonify("true"), 200
    except mysql.connector.Error as err:
        print("SQL error: {}".format(err))
        return jsonify("false"), 500
    finally:
        mycursor.close()
        mydb.close()
        
        
@app.route("/removeCategory/<int:id>", methods=['GET'])
def removeCategory(id):
    user_id = session.get("idu")

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="usercontentdb",
        port="3308",
        charset='utf8'
    )

    mycursor = mydb.cursor()
    sql = "DELETE FROM categories_rel WHERE id_category=%s AND id_user=%s"
    values = (id, user_id)

    try:
        mycursor.execute(sql, values)
        mydb.commit()
        return jsonify("true"), 200
    except mysql.connector.Error as err:
        print("SQL error: {}".format(err))
        return jsonify("false"), 500
    finally:
        mycursor.close()
        mydb.close()

@app.route("/removeContent/<int:id>", methods=['GET'])
def removeContent(id):
    user_id = session.get("idu")

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="usercontentdb",
        port="3308",
        charset='utf8'
    )

    mycursor = mydb.cursor()
    sql = "DELETE FROM content WHERE id=%s AND iduser=%s"
    values = (id, user_id)

    try:
        mycursor.execute(sql, values)
        mydb.commit()
        return jsonify("true"), 200
    except mysql.connector.Error as err:
        print("SQL error: {}".format(err))
        return jsonify("false"), 500
    finally:
        mycursor.close()
        mydb.close()


@app.route("/categoryContent1", methods=['GET'])
def get_categories1():
    user_id = session.get("idu")

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="usercontentdb",
        port="3308",
        charset='utf8'
    )

    mycursor = mydb.cursor(dictionary=True)
    sql = """
        SELECT c.id, c.name
        FROM categories c
        LEFT JOIN categories_rel cr ON c.id = cr.id_category AND cr.id_user = %s
        WHERE cr.id_category IS NULL
    """
    mycursor.execute(sql, (user_id,))
    result = mycursor.fetchall()

    return jsonify(result), 200

@app.route("/categoryMyContent", methods=['GET'])
def get_my_categories():
    user_id = session.get("idu")

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="usercontentdb",
        port="3308",
        charset='utf8'
    )

    mycursor = mydb.cursor(dictionary=True)
    sql = """
        SELECT c.id, c.name
        FROM categories c
        INNER JOIN categories_rel cr ON c.id = cr.id_category
        WHERE cr.id_user = %s
    """
    mycursor.execute(sql, (user_id,))
    result = mycursor.fetchall()

    return jsonify(result), 200

@app.route("/followed_users", methods=["GET"])
def get_followed_users():
    user_id = session.get("idu")
    if user_id:
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset="utf8"
        )
        mycursor = mydb.cursor()
        sql = """
            SELECT u.id, u.name, u.profilephoto
            FROM users u
            INNER JOIN user_rel ur ON u.id = ur.idu2 AND ur.idu1 = %s
            WHERE ur.type = 'following'
        """
        try:
            mycursor.execute(sql, (user_id,))
            results = mycursor.fetchall()
            if not results:
                return jsonify({"error": "No followed users found"}), 404
            else:
                user_list = []
                for row in results:
                    user = {}
                    user["id"] = str(row[0])
                    user["name"] = row[1]
                    user["profilephoto"] = row[2]
                    user_list.append(user)
                return jsonify(user_list), 200
        except mysql.connector.Error as err:
            print("SQL error: {}".format(err))
            return jsonify({"error": "Internal Server Error"}), 500
        finally:
            mycursor.close()
            mydb.close()
    else:
        return jsonify({"error": "User not found"}), 401




@app.route("/userCategory/<int:id>", methods=['GET'])
def getUserCategory(id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="usercontentdb",
        port="3308",
        charset='utf8'
    )

    mycursor = mydb.cursor(dictionary=True)
    sql = """
        SELECT c.id, c.name
        FROM categories c
        INNER JOIN categories_rel cr ON c.id = cr.id_category
        WHERE cr.id_user = %s
    """
    mycursor.execute(sql, (id,))
    result = mycursor.fetchall()

    return jsonify(result), 200


@app.route("/userFriends/<int:id>", methods=['GET'])
def userFriends(id):
    user_id = id
    if user_id:
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usercontentdb",
            port="3308",
            charset="utf8"
        )
        mycursor = mydb.cursor()
        sql = """
            SELECT u.id, u.name, u.profilephoto
            FROM users u
            INNER JOIN user_rel ur ON u.id = ur.idu2 AND ur.idu1 = %s
            WHERE ur.type = 'following'
        """
        try:
            mycursor.execute(sql, (user_id,))
            results = mycursor.fetchall()
            
            user_list = []
            for row in results:
                    user = {}
                    user["id"] = str(row[0])
                    user["name"] = row[1]
                    user["profilephoto"] = row[2]
                    user_list.append(user)
            return jsonify(user_list), 200
        except mysql.connector.Error as err:
            print("SQL error: {}".format(err))
            return jsonify({"error": "Internal Server Error"}), 500
        finally:
            mycursor.close()
            mydb.close()
    else:
        return jsonify({"error": "User not found"}), 401

#api
app.run(debug=True,threaded=True, host='localhost', port="8081")