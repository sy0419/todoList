from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

todos = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        date = request.form.get('date')
        if title:
            todos.append({
                'id': len(todos) + 1,
                'title': title,
                'is_completed': False,
                'date': date
            })
        return redirect('/')

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>TO-DO_LIST</title>
    </head>
    <body>
        <h1>할 일 목록</h1>

        <ul>
        {% for todo in todos %}
            <li>
                {{ todo['title'] }} ({{ todo['date'] }})  - 완료: {{ 'O' if todo['is_completed'] else 'X' }}
                {% if not todo['is_completed'] %}
                    <form action="{{ url_for('complete_todo', todo_id=todo['id']) }}" method="post" style="display:inline;">
                        <button type="submit">완료</button>
                    </form>
                {% endif %}
            </li>
        {% endfor %}
        </ul>

        <h2>할 일 추가하기</h2>
        <form method="POST">
            <input type="text" name="title" placeholder="할 일을 입력하세요" required>
            <input type="date" name="date" placeholder="날짜를 입력하세요" required>
            <button type="submit">추가</button>
        </form>
    </body>
    </html>
    '''
    return render_template_string(html, todos=todos)

@app.route('/complete/<int:todo_id>', methods=['POST'])
def complete_todo(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            todo['is_completed'] = True
            break
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)