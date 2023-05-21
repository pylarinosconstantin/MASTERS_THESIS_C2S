import json
import mysql.connector
import random as rd
import datetime
import os
from werkzeug.utils import secure_filename
from flask import request
from flask import session
import base64
from PIL import Image


mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="usercontentdb",
        port="3308",
        charset='utf8')

mycursor=mydb.cursor()

class User:
    def __init__(self):
        self.email=""
        self.password=""
        self.phone=""
        self.name=""
        self.bio=""
        self.location=""
        self.field=""
        self.birth=""
        self.profilephoto=""
        self.backgroundphoto=""
        self.id=""
    
    def set(self,T):
        try:
            self.email=T["email"]
        except:
            pass
        try:    
            self.password=T["password"]
        except:
            pass
        try: 
            self.phone=T["phone"]
        except:
            pass
        try: 
            self.name=T["name"]
        except:
            pass
        try: 
            self.bio=T["bio"]
        except:
            pass
        try: 
            self.location=T["location"]
        except:
            pass
        try: 
            self.field=T["field"]
        except:
            pass
        try: 
            self.birth=T["birth"]
        except:
            pass
        try: 
            self.profilephoto=T["profilephoto"]
        except:
            pass
        try: 
            self.backgroundphoto=T["backgroundphoto"]
        except:
            pass
        try: 
            self.id=T["id"]
        except:
            pass
    
    
    
    
    def insertdb(self):
        global mydb
        mycursor = mydb.cursor()

        sql = "insert into users set email='"+self.email+"',"
        sql = sql+" password='"+self.password+"', "
        sql = sql+" phone='"+self.phone+"', "
        sql = sql+" name='"+self.name+"', "
        sql = sql+" bio='"+self.bio+"', "
        sql = sql+" location='"+self.location+"', "
        sql = sql+" field='"+self.field+"', "
        sql = sql+" birth='"+self.birth+"' "

        try:
            mycursor.execute(sql)
            mydb.commit()
            self.id = mycursor.lastrowid
        except Exception as e:
            print(e)  # print the error message
            raise Exception("Insert error")
    
    
    def deletedb(self):
        global mydb
        mycursor=mydb.cursor()
          
        mycursor.execute("delete from users where id="+str(self.id))
        self.id=0  

    def getAll(self):
        global mydb
        mycursor=mydb.cursor()
        sql="select * from users"
        mycursor.execute(sql)
        res=mycursor.fetchall()
        P=[]
        for r in res:
                p={}
                p['email']=r[1]
                p['password']=r[3]
                p['phone']=r[2]
                p['name']=r[4]
                p['bio']=r[5]
                p['location']=r[6]
                p['field']=r[7]
                p['birth']=r[8]
                p['id']=str(r[0])
                P.append(p)
                
        return (json.dumps(P))
    
    def get_user_info(self):
        return self.user_info

    def setUserById(self,id1):
        global mydb
        mycursor=mydb.cursor()
        sql="select * from users where id="+str(id1)
        print("id received: ", id1)
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
            p['id']=str(r[0])
            self.user_info=p
            return p
        except:
            raise Exception("No found")

    def setUserByUsrPss(self,e,p):
        global mydb
        mycursor=mydb.cursor()
        sql="select * from users where email='"+e+"' and password='"+p+"'"
        try:
            mycursor.execute(sql)
            r=mycursor.fetchone()
            p={}
            p['email']=r[1]
            p['password']=r[3]
            p['phone']=r[2]
            p['id']=str(r[0])
            self.set(p)
        except:
            raise Exception("No found")
        
    def setAdminByUsrPss(self,e,p):
        global mydb
        mycursor=mydb.cursor()
        sql="select * from admin where email='"+e+"' and password='"+p+"'"
        try:
            mycursor.execute(sql)
            r=mycursor.fetchone()
            p={}
            p['email']=r[0]
            p['password']=r[1]
            p['id']=str(r[2])
            self.set(p)
        except:
            raise Exception("No found")      
    
    
    def printuser(self):
        print("email:"+self.email+" password:"+self.password+" phone:"+self.phone)
        
    def getJSON(self):
        x={}
        x["id"]=self.id
        x["email"]=self.email
        x["password"]=self.password
        x["phone"]=self.phone
        return json.dumps(x)
    

    def updateProfile(self, app, request):
        user_id = request.json.get("user_id")
        # check if user_id is not None
        if user_id is None:
            raise Exception("User not logged in")
        self.name = request.json.get("name")
        self.password = request.json.get("password")
        self.bio = request.json.get("bio")
        self.location = request.json.get("location")
        self.field = request.json.get("field")
        self.birth = request.json.get("birth")
        # handle profile photo
        if request.json.get('profile_photo'):
            profile_photo = request.json.get('profile_photo')
            # decode the base64 encoded image data
            image_data = base64.b64decode(profile_photo)
            # write the image data to a file
            with open(os.path.join(app.config['uploads'], 'profile_photo.jpg'), 'wb') as f:
                f.write(image_data)
            self.profile_photo = 'profile_photo.jpg'
        # handle background photo
        if request.json.get('background_photo'):
            background_photo = request.json.get('background_photo')
            # decode the base64 encoded image data
            image_data = base64.b64decode(background_photo)
            # write the image data to a file
            with open(os.path.join(app.config['uploads'], 'background_photo.jpg'), 'wb') as f:
                f.write(image_data)
            self.background_photo = 'background_photo.jpg'
        # update the user's information in the database
        sql = f"UPDATE users SET name = '{self.name}', password = '{self.password}', bio = '{self.bio}', location = '{self.location}', field = '{self.field}', birth = '{self.birth}', profile_photo = '{self.profile_photo}', background_photo = '{self.background_photo}' WHERE id = {user_id}"
        mycursor.execute(sql)
        mydb.commit()


    
    


class Content:
     
    def __init__(self):
        self.filename=""
        self.title=""
        self.user=User()
        self.id=0     

    def set(self,T):
        self.filename=T["filename"]
        self.title=T["title"]
        self.id=T["id"]
        self.user.setUserById(T["iduser"])
      
    def uploadfile(self,fn):
        try:
            y=str(datetime.datetime.now().year)
            m=str(datetime.datetime.now().month)
            d=str(datetime.datetime.now().day)
            h=str(datetime.datetime.now().hour)
            mn=str(datetime.datetime.now().minute)
            ff=os.path.splitext(fn.filename)
            
            newfn=y+m+d+h+mn+str(rd.randint(10000,99999))+str(rd.randint(10000,99999))+ff[1]
            
            self.filename=newfn
            
            fn.save("uploads/"+newfn)
        except:
            raise Exception("No Upload")
      
    def insertdb(self):
        global mydb
        mycursor=mydb.cursor()
        try:
            sql="insert into content set filename='"+self.filename+"',"
            sql=sql+"title='"+self.title+"',"
            sql=sql+"iduser='"+str(self.user.id)+"'"
            mycursor.execute(sql)
            mydb.commit()
            self.id=mycursor.lastrowid  
        except:
            raise Exception("No insert content")
      
    
    def updatedb(self):
        global mydb
        mycursor=mydb.cursor()
        try:
            sql="update content set filename='"+self.filename+"',"
            sql=sql+"title='"+self.title+"',"
            sql=sql+"iduser='"+str(self.user.id)+"'"
            sql=sql+" where id="+str(self.id)
            mycursor.execute(sql)
            mydb.commit()
                  
        except:
            raise Exception("No Update content")

    def deletedb(self):
        global mydb
        mycursor=mydb.cursor()
        try:
            sql="delete from content where id="+str(self.id)
            mycursor.execute(sql)
            mydb.commit()
            
        except:
            raise Exception("No delete content")      

      
    def getAll(self):
        global mydb
        mycursor=mydb.cursor()
        
        sql="select * from content"
        mycursor.execute(sql)
        res=mycursor.fetchall()
        P=[]
        for r in res:
                p={}
                u=User()
                u.setUserById(r[3])
                p['id']=str(r[0])
                p['filename']=r[1]
                p['title']=r[2]
                p['iduser']=r[3]
                p['email']=u.email
                P.append(p)
        
        return (json.dumps(P))
      
    def getUserAll(self, iduser):
            global mydb
            mycursor=mydb.cursor()
            
            sql="select * from content where iduser="+str(iduser)
            mycursor.execute(sql)
            res=mycursor.fetchall()
            P=[]
            for r in res:
                    p={}
                    p['id']=str(r[0])
                    p['filename']=r[1]
                    p['title']=r[2]
                    p['iduser']=r[3]
                    P.append(p)
        
            return (json.dumps(P))


    def setContentByIdl(self, id):
            global mydb
            mycursor=mydb.cursor()
            try:
                sql="select * from content where id="+str(id)
                mycursor.execute(sql)
                r=mycursor.fetchone()
               
                p={}
                p['id']=str(r[0])
                p['filename']=r[1]
                p['title']=r[2]
                p['iduser']=r[3]
                self.set(p)
            except:
                raise Exception("No found content") 

     
    
    def getJSON(self):
        x={}
        x["id"]=self.id
        x["filename"]=self.filename
        x["title"]=self.title
        x["iduser"]=self.user.id
        return json.dumps(x)
