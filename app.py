from flask import Flask, request, render_template_string, redirect

app = Flask(__name__)

todos = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        if title:
            todos.append({
                'id': len(todos) + 1,
                'title': title,
                'is_completed': False
            })
        return redirect('/')  # POST 후 다시 홈으로 돌아가게 하기

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>할 일 목록</title>
    </head>
    <body>
        <h1>할 일 목록</h1>

        <ul>
        {% for todo in todos %}
            <li>{{ todo['title'] }} - 완료: {{ 'O' if todo['is_completed'] else 'X' }}</li>
        {% endfor %}
        </ul>

        <h2>할 일 추가하기</h2>
        <form method="POST">
            <input type="text" name="title" placeholder="할 일을 입력하세요" required>
            <button type="submit">추가</button>
        </form>
    </body>
    </html>
    '''
    return render_template_string(html, todos=todos)

if __name__ == '__main__':
    app.run(debug=True)
