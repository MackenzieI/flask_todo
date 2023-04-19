from flask import Flask, render_template, request, url_for, redirect

from flask import Flask
from pymongo import MongoClient

from bson.objectid import ObjectId

# Init the Flask app
app = Flask(__name__)
client = MongoClient("mongodb://127.0.0.1:27017")

# Create the database
db = client.flask_db
todos = db.todos

def redirect_url():
    # Redirects the webpage to index
    return request.args.get('next') or request.referrer or url_for('index')    

@app.route('/', methods=('GET', 'POST'))
def index():
    # Find and render the index with the active todo tasks
    all_todos = todos.find()
    a = "active"
    return render_template('index.html', a=a, todos=all_todos)

@app.route("/action", methods=['POST'])
def post():
    # Submit a task with the form. Tasks are initialized as not done
    content = request.form['content']
    todos.insert_one({'content': content, "done": "no"})
    return redirect('/')

@app.route("/delete")    
def delete ():   
    # Delete an id then redirect to route 
    key=request.values.get("_id")    
    todos.delete_one({"_id":ObjectId(key)})    
    return redirect("/")

@app.route("/done")    
def done ():    
    # Get and find an ID. If a task is set as done, set it as not done
    # Otherwise, update the task as done and hide the index. Redirect
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
    # Get the task id and redirect to update.html
    id=request.values.get("_id")    
    task=todos.find({"_id":ObjectId(id)})    
    return render_template('update.html', tasks=task)    

@app.route("/updatedata", methods=['POST'])    
def updatedata ():    
    # Update the task with its new content. Redirect to root
    content=request.values.get("content")      
    id=request.values.get("_id")    
    todos.update_one({"_id":ObjectId(id)}, {'$set':{ "content":content }})    
    return redirect("/")  
