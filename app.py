from flask import Flask, render_template, request,url_for,redirect
from pymongo import MongoClient
from bson.objectid import ObjectId 
app = Flask(__name__)

#Database connection
client = MongoClient('localhost', 27017)
db = client.todo_database
todos = db.todos


@app.route('/', methods=['GET','POST'])
@app.route('/<todo_id>', methods=['GET','POST'])
def index(todo_id=None):
    if request.method == 'POST':
        content = request.form['content']
        if todo_id is None:
            todos.insert_one({'content': content})
        else:
            todo = todos.find_one({"_id":ObjectId(todo_id)})
            if todo:
                content = request.form['content']
                db.todos.update_one({"_id": ObjectId(todo_id)},
                                    {"$set":{'content': content}})        
                                    

                return redirect(url_for('index'))
    
    todo = None
    if todo_id is not None:
        todo = todos.find_one({"_id":ObjectId(todo_id)})
    all_todos = todos.find()

    return render_template('index.html',todos = all_todos,todo = todo)



@app.route('/<id>/delete/',methods=['GET','POST'])
def delete(id):
      if request.method == 'POST':
        todos.delete_one({"_id":ObjectId(id)})
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)