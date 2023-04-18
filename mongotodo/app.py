from flask import Flask, render_template, request, url_for, redirect

from flask import Flask
from pymongo import MongoClient

from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient("mongodb://127.0.0.1:27017")

db = client.flask_db
todos = db.todos

def redirect_url():    
    return request.args.get('next') or request.referrer or url_for('index')    

@app.route('/', methods=('GET', 'POST'))
def index():
    all_todos = todos.find()
    a = "active"
    return render_template('index.html', a=a, todos=all_todos)

@app.route("/action", methods=['POST'])
def post():    
    content = request.form['content']
    todos.insert_one({'content': content, "done": "no"})
    return redirect('/')

@app.route("/delete")    
def delete ():    
    key=request.values.get("_id")    
    todos.delete_one({"_id":ObjectId(key)})    
    return redirect("/")

@app.route("/done")    
def done ():    
    id=request.values.get("_id")    
    task=todos.find({"_id":ObjectId(id)})    
    if(task[0]["done"]=="yes"):    
        todos.update_one({"_id":ObjectId(id)}, {"$set": {"done":"no"}})    
    else:    
        todos.update_one({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})  
        db.todos.hideIndex({"_id": ObjectId(id)})
    return redirect("/")

@app.route("/update")    
def update ():    
    id=request.values.get("_id")    
    task=todos.find({"_id":ObjectId(id)})    
    return render_template('update.html', tasks=task)    

@app.route("/updatedata", methods=['POST'])    
def updatedata ():    
    content=request.values.get("content")      
    id=request.values.get("_id")    
    todos.update_one({"_id":ObjectId(id)}, {'$set':{ "content":content }})    
    return redirect("/")  

"""Although you can create the file by hand, you can also use the pip freeze command to 
generate the file based on the exact libraries installed in the activated environment:

With your chosen environment selected using the Python: Select Interpreter command, 
run the Terminal: Create New Terminal command (Ctrl+Shift+`)) to open a terminal with 
that environment activated.

In the terminal, run pip freeze > requirements.txt to create the requirements.txt 
file in your project folder."""