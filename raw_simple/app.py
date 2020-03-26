from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.mymongodb
tasks_collection = db.task
initial_tasks = [task for task in tasks_collection.find()]

if (len(initial_tasks)) == 0:
    tasks_collection.insert_many([{
        'id': 0,
        'title': 'Buy groceries',
        'description': 'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },{
        'id': 1,
        'title': 'Learn Python',
        'description': 'Need to find a good Python tutorial on the web',
        'done': False
    }])


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    all_tasks = tasks_collection.find()
    task_list = []
    for task in all_tasks:
        task_list.append(
            {'title': task['title'], 'description': task['description'], 'id': task['id']})

    return jsonify({'tasks': task_list})


@app.route('/api/create-task', methods=['GET'])
def create_task():
    tasks = tasks_collection.find()
    new_task = {"id": tasks.count(), "title": "Learn Mongo",
                "description": "Start with Flask + Mongo", "done": False}
    tasks_collection.insert_one(new_task)
    all_tasks = tasks_collection.find()
    task_list = []
    for task in all_tasks:
        task_list.append(
            {'title': task['title'], 'description': task['description'], 'id': task['id']})
    return jsonify({'tasks': task_list})


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    tasks = list(tasks_collection.find({'id': task_id}))
    if len(tasks) == 0:
        return jsonify({'task': None})
    tasks[0]["_id"] = str(tasks[0]["_id"])
    return jsonify({'task': tasks[0]})


@app.route('/', methods=['GET'])
def home():
    return jsonify({'msg': 'This is the Home'})


@app.route('/test', methods=['GET'])
def test():
    return jsonify({'msg': 'This is a Test'})


if __name__ == '__main__':
    app.run(debug=True)
