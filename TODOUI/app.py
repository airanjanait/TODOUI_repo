from flask import Flask,request,render_template,redirect,url_for
from flask_login import UserMixin,LoginManager,current_user,login_user,logout_user,login_required
from flask.sessions import SecureCookieSessionInterface
from function import Function
import base64 
from flask import g
import os

obj=Function()
app=Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = os.urandom(24)

registered_users=[]


class User(UserMixin):
    def __init__(self,id,Email,Password):
        self.id=id
        # print(id,"-------------------------")
        self.Email=Email
        # print(Email,"-------------------------")
        self.Password=Password
        # print(Password,"-------------------------")

@app.before_request
def before_request():
    g.user=current_user
    print(current_user,"---------------------")

@login_manager.user_loader
def load_user(user_id):
    # print(user_id,"!!!!!!!!!!!!!!!!!!!!!!!!!")
    try:
        with app.app_context():
            user = obj.user_id(user_id)
            print(user.Name,"==================")
            print(user.id,"user-id****************************")
            print(user.Email)
        if user: 
           return User((user.id,user.Email,user.Password))
    except:
        pass
        
    
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        Email=request.form.get("Email")
        print(Email)
        Password=request.form.get("Password")
        with app.app_context():
            user=obj.user_login(Email,Password)
        if user:
            print(user.Email,"#######################################")
            login_user(User(user.id,user.Email,user.Password))
            return render_template('login_done.html')
        else:
            return "Invalid username/password"
    return render_template('login.html')
   
        
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')
        
@app.route('/hello')
@login_required
def hello():
    return 'hello.html'

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@app.errorhandler(404)
def page_not_found(self):
    return redirect('/')
#_______________registration ____________________

@app.route("/",methods=['POST','GET'])
def registrationinfo():
    if request.method=="POST":
        Name=request.form.get("Name")
        Password=request.form.get("Password")
        pwd=base64.b64encode(Password.encode("utf-8"))
        print(pwd)
        Email=request.form.get("Email")
        data=obj.registration(Name,pwd,Email) 
        return render_template("home.html")
        
    return render_template("registration.html")

#___________________add task________________________

@app.route("/addtask",methods=['POST','GET'])
def addtasks():
    if request.method=="POST":
        TaskName=request.form.get("TaskName")
        StartDate=request.form.get("StartDate")
        StartTime=request.form.get("StartTime")
        DueDate=request.form.get("DueDate")
        data=obj.addtask(TaskName,StartDate,StartTime,DueDate)
    return render_template("addtask.html")

#__________________ fetch task detail ______________________

@app.route("/fetchtask",methods=['POST','GET'])
def fetchtaskdetailes():
    task_info=""
    if request.method=="POST":
        ID=request.form.get("ID")
        task_info=obj.fetchtask(ID)
        if "There is not any task on this ID" in task_info:
            return task_info
    return render_template("fetchtask.html",task_info=task_info)


#____________________delete task ____________________________

@app.route("/deletetask/<ID>")
def delete(ID):
    obj.deletetask(ID)
    return redirect ("/fetchtask")

#_________________fetch to update and to update________________

@app.route("/fetchtoupdate/<ID>")
def fetchtoupdate(ID):
    data=obj.fetchonetask(ID)
    return render_template("update.html",data=data)

@app.route("/updatetask",methods=['POST','GET'])
def update():
    data=""
    if request.method=="POST":
        ID=request.form.get("ID")
        TaskName=request.form.get("TaskName")
        StartDate=request.form.get("StartDate")
        StartTime=request.form.get("StartTime")
        DueDate=request.form.get("DueDate")
        obj.update_task(ID,TaskName,StartDate,StartTime,DueDate)
        return redirect("/fetchtask")
    
#__________________make history of tasks_______________________

@app.route("/maketaskhistory/<ID>")
def makehistoryoftask(ID):
    data=""
    data=obj.makehistory(ID)
    return data

#_____________________get history of task______________________

@app.route("/gettaskhistory",methods=['POST','GET'])
def gettaskhistory():
    data=""
    if request.form.get("date"):
        date=request.form.get("date")
        
        data=obj.gettaskhistory(date)
        if f"On {date} there is not any task assigned" in data:
            return data
    return render_template("gettaskhistory.html",data=data)

if __name__=="__main__":
    app.run(debug=True)