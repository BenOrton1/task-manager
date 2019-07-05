import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)


@app.route('/')
@app.route('/gettasks')
def gettasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())
    
@app.route('/addtask')
def addtask():
    _categories = mongo.db.categories.find()
    category_list = [category for category in _categories]
    return render_template('addtasks.html', categories = category_list)
    
@app.route('/inserttask', methods=['GET', 'POST'])
def inserttask():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('gettasks'))
    
@app.route('/edittask/<task_id>')
def edittask(task_id):
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_catagories = mongo.db.categories.find()
    return render_template('edittask.html', task = the_task, categories= all_catagories)
 
@app.route('/updatetask/<task_id>', methods=['GET', 'POST'])
def updatetask(task_id):
    tasks = mongo.db.tasks
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'task_name':request.form.get('task_name'),
        'category_name':request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent':request.form.get('is_urgent')
    })
    return redirect(url_for('gettasks'))
    
@app.route('/deletetask/<task_id>')
def deletetask(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('gettasks'))
    
    
@app.route('/getcategories')
def getcategories():
    return render_template('categories.html',
    categories=mongo.db.categories.find())


@app.route('/editcategory/<category_id>')
def editcategory(category_id):
    return render_template('editcategory.html',
                           category=mongo.db.categories.find_one(
                           {'_id': ObjectId(category_id)}))


@app.route('/updatecategory/<category_id>', methods=['GET', 'POST'])
def updatecategory(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get['category_name']})
    return redirect(url_for('getcategories'))

@app.route('/deletecategory/<category_id>', methods=['GET', 'POST'])
def deletecategory(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('getcategories'))

@app.route('/insertcategory',  methods=['GET', 'POST'])
def insertcategory():
    categories = mongo.db.categories
    category_doc = {'category_name': request.form.get['category_name']}
    categories.insert_one(category_doc)
    return redirect(url_for('getcategories'))

@app.route('/addcategory')
def addcategory():
    return render_template('addcategory.html')

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)