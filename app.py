from flask import Flask, render_template, request, jsonify
from sql_interface import DataBaseInterface

app = Flask(__name__)
db = DataBaseInterface()

@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        if db.get_user(data['username'], data['password']):
            response = jsonify({"status": "success", "message": "Login successful"})
            response.status_code = 200
            return response, 200
        else:
            response = jsonify({"status": "error", "message": "Ошибка авторизации. Неправильные логин или пароль."})
            response.status_code = 401
            return response, 401
    return render_template('login.html')


@app.route('/contests')
def contests():
    contests = []
    for contest in db.get_all_contests():
        contests.append({
            'id': contest[0],
            'name': contest[1]})
    print(contests)
    return render_template('contests.html', contests=contests)


@app.route('/contest/<int:contest_id>')
def contest_details(contest_id):
    db_res = db.get_contest_by_id(contest_id)
    contest = {
        'id': db_res[0],
        'name': db_res[1],
        'description': db_res[2]
    }
    return render_template('contest_details.html', contest=contest)


@app.route('/contest/<int:contest_id>/problems')
def contest_problems(contest_id):
    exersises = []
    for ex in db.get_contest_exs(contest_id):
        exersises.append({
            'id': ex[0],
            'title': 'Задача ' + str(ex[1])
        })
    return render_template('contest_problems.html', contest_id=contest_id, problems=exersises)


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
