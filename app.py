from flask import Flask, render_template, request,url_for,redirect
from pymongo import MongoClient
from bson.objectid import ObjectId 
app = Flask(__name__)

#Database connection
client = MongoClient('localhost', 27017)
db = client.todo_database
todos = db.todos


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        todos.insert_one({'content': content})
        return redirect(url_for('index'))

    all_todos = todos.find()

    return render_template('index.html',todos = all_todos)

# @app.route('/<id>/edit', methods=['GET','POST'])
# def edit(id):
#     if request.meyhod == 'POST':


@app.route('/<id>/delete/',methods=['GET','POST'])
def delete(id):
      if request.method == 'POST':
        todos.delete_one({"_id":ObjectId(id)})
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)