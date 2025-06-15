from flask import Flask, request, render_template_string, redirect
import calendar
from datetime import datetime

app = Flask(__name__)

todos = []

year = 2025
month = 6
cal = calendar.Calendar(firstweekday=6)
month_days = cal.monthdayscalendar(year, month)

@app.route('/', methods=['GET', 'POST'])
def home():
    editing_id = request.args.get('edit', type=int)
    
    today = datetime.today()
    
    year = request.args.get('year', default=today.year, type=int)
    month = request.args.get('month', default=today.month, type=int)
    
    def prev_month(y, m):
        if m == 1:
            return y - 1, 12
        else:
            return y, m - 1

    def next_month(y, m):
        if m == 12:
            return y + 1, 1
        else:
            return y, m + 1

    prev_year, prev_month = prev_month(year, month)
    next_year, next_month = next_month(year, month)

    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)

    if request.method == 'POST':
        title = request.form.get('title')
        date = request.form.get('date')

        if editing_id:
            # 수정하는 경우
            for todo in todos:
                if todo['id'] == editing_id:
                    todo['title'] = title
                    todo['date'] = date
                    break
        else:
            # 새 할 일 추가
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
        <style>
            table {
                width: 100%;
                border-collapse: separate;
                border-spacing: 15px; /* 셀 간격 */
            }
            h1 {
                font-size: 40px;
                text-align: center;
                margin-bottom: 20px;
            }
            td {
                width: 100px;
                height: 100px;
                vertical-align: top;
                border: 1px solid #ccc;
                padding: 5px;
                font-size: 18px;  
            }
            td span {
                display: block;
                font-weight: bold;
                font-size: 18px;
                margin-bottom: 5px;
            }
            .saturday {
                background-color: #d0eaff; /* 연한 파랑 */
            }
            .sunday {
                background-color: #ffd6d6; /* 연한 빨강 */
            }
            body {
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px 0;
            }
        </style>
    </head>
    <body>
        <h1>Calendar</h1>
        <style>
            .nav-button {
                font-size: 18px;
                padding: 5px 10px;
            }
            .month-title {
                font-size: 24px;
                margin: 0 15px;
            }
        </style>
        <div style="margin-bottom: 20px; text-align: center;">
            <button class="nav-button" onclick="location.href='/?year={{ prev_year }}&month={{ prev_month }}'">&lt; 이전</button>
            <strong class="month-title">{{ year }}년 {{ month }}월</strong>
            <button class="nav-button" onclick="location.href='/?year={{ next_year }}&month={{ next_month }}'">다음 &gt;</button>
        </div>
        <table>
        <tr>
            <th>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th>토</th>
        </tr>
        {% for week in month_days %}
        <tr>
            {% for day in week %}
            {% set weekday = loop.index0 %}
                <td>
                    {% if day == 0 %}
                        &nbsp;
                    {% else %}
                        {% set date_str = '{}-{:02d}-{:02d}'.format(year, month, day) %}
                        <span 
                            {% if weekday == 6 %}
                                style="color: blue;"
                            {% elif weekday == 0 %}
                                style="color: red;"
                            {% endif %}
                        >
                            {{ day }}
                        </span>
                        {% for todo in todos %}
                            {% if todo.date == date_str %}
                                <div style="color: {% if todo.is_completed %}#bbb{% else %}black{% endif %};">
                                    {{ todo.title }}
                                </div>
                            {% endif %}
                        {% endfor %}
                    {% endif %}
                </td>
            {% endfor %}
        </tr>
        {% endfor %}
        </table>

        <h2>할 일 목록</h2>
        <ul>
        {% for todo in todos %}
            <li>
                {% if editing_id == todo['id'] %}
                    <form method="POST" action="/?edit={{ todo['id'] }}" style="display:inline;">
                        <input type="text" name="title" value="{{ todo['title'] }}">
                        <input type="date" name="date" value="{{ todo['date'] }}">
                        <button type="submit">저장</button>
                    </form>
                {% else %}
                    <span style="color: {% if todo.is_completed %}#bbb{% else %}black{% endif %};">
                        {{ todo['title'] }} ({{ todo['date'] }})
                    </span>
                    <form method="POST" action="{{ url_for('complete_todo', todo_id=todo['id']) }}" style="display:inline;">
                        <input type="checkbox" name="is_completed" onchange="this.form.submit()" {% if todo['is_completed'] %}checked{% endif %}>
                    </form>
                    <form method="GET" action="/" style="display:inline;">
                        <input type="hidden" name="edit" value="{{ todo['id'] }}">
                        <button type="submit">수정</button>
                    </form>
                {% endif %}
                <form method="POST" action="{{ url_for('delete_todo', todo_id=todo['id']) }}" style="display:inline;">
                    <button type="submit" onclick="return confirm('정말 삭제할까요?');">삭제</button>
                </form>
            </li>
        {% endfor %}
        </ul>

        <h3>할 일 추가하기</h3>
        <form method="POST">
            <input type="text" name="title" placeholder="할 일을 입력하세요" required>
            <input type="date" name="date" placeholder="날짜를 입력하세요" required>
            <button type="submit">추가</button>
        </form>
    </body>
    </html>
    '''

    return render_template_string(
        html, todos=todos, month_days=month_days, year=year, month=month,
        editing_id=editing_id, prev_year=prev_year, prev_month=prev_month,
        next_year=next_year, next_month=next_month
    )

@app.route('/complete/<int:todo_id>', methods=['POST'])
def complete_todo(todo_id):
    value = request.form.get('is_completed')
    for todo in todos:
        if todo['id'] == todo_id:
            if value == 'on':
                todo['is_completed'] = True
                break
            else:
                todo['is_completed'] = False
                break
    return redirect('/')

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)