from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Здесь должна быть логика проверки логина и пароля
        return render_template('contests.html', contests=[
            {'id': 1, 'name': 'Contest 1'},
            {'id': 2, 'name': 'Contest 2'},
            {'id': 3, 'name': 'Contest 3'}
        ])
    return render_template('login.html')


@app.route('/contests')
def contests():
    contests = [
        {'id': 1, 'name': 'Contest 1'},
        {'id': 2, 'name': 'Contest 2'},
        {'id': 3, 'name': 'Contest 3'}
    ]
    return render_template('contests.html', contests=contests)


@app.route('/contest/<int:contest_id>')
def contest_details(contest_id):
    contest = {
        'id': contest_id,
        'name': f'Contest {contest_id}',
        'description': f'Описание контеста {contest_id}. Здесь можно разместить информацию о правилах и времени проведения.'
    }
    return render_template('contest_details.html', contest=contest)


@app.route('/contest/<int:contest_id>/problems')
def contest_problems(contest_id):
    problems = [
        {'id': 1, 'title': 'Задача 1'},
        {'id': 2, 'title': 'Задача 2'},
        {'id': 3, 'title': 'Задача 3'}
    ]
    return render_template('contest_problems.html', contest_id=contest_id, problems=problems)


@app.route('/contest/<int:contest_id>/problem/<int:problem_id>', methods=['GET', 'POST'])
def contest_problem(contest_id, problem_id):
    # Если id задачи чётный – это задача с вариантами ответа (MCQ),
    # если нечётный – задача с написанием кода.
    if problem_id % 2 == 0:
        problem_type = 'mcq'
        problem = {
            'id': problem_id,
            'question': 'Какой цвет получится при смешении синего и жёлтого?',
            'options': ['Зелёный', 'Фиолетовый', 'Оранжевый', 'Красный'],
            'correct': 0  # индекс правильного ответа (Зелёный)
        }
    else:
        problem_type = 'code'
        problem = {
            'id': problem_id,
            'description': 'Напишите функцию, которая возвращает сумму двух чисел.',
            'compilers': ['Python', 'Java', 'C++']
        }

    result = None
    if request.method == 'POST':
        if problem_type == 'mcq':
            selected = int(request.form.get('option', -1))
            if selected == problem['correct']:
                result = 'correct'
            else:
                result = 'incorrect'
        else:
            code = request.form.get('code')
            compiler = request.form.get('compiler')
            # Здесь можно добавить логику компиляции и проверки кода.
            result = f'Код отправлен на проверку с использованием {compiler}.'

    return render_template('contest_problem.html',
                           contest_id=contest_id,
                           problem=problem,
                           problem_type=problem_type,
                           result=result)


if __name__ == '__main__':
    app.run(debug=True)
