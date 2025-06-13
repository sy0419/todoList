from flask import Flask, jsonify, request

app = Flask(__name__)

todos = []

@app.route('/')
def home():
    return 'Hello, Flask! This is the home page.'

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    todo = {
        'id': len(todos) + 1,
        'title': data.get('title'),
        'is_completed': False
    }
    todos.append(todo)
    return jsonify(todo), 201

if __name__ == '__main__':
    app.run(debug=True)