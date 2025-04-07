from flask import Flask, render_template, request, jsonify
from sql_interface import DataBaseInterface
from unittest import test 

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
            response = jsonify({"status": "success", "message": "Успешный вход"})
            response.status_code = 200
            return response, 200
        else:
            response = jsonify({"status": "error", "message": "Ошибка авторизации. Неправильные логин или пароль."})
            response.status_code = 401
            return response, 401
    return render_template('login.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        data = request.json
        if db.add_user(data['nickname'], data['username'], data['password']):
            response = jsonify({"status": "success", "message": "Успешная регистрация"})
            response.status_code = 200
            return response, 200
        else:
            response = jsonify({"status": "error", "message": "Ошибка регстрации. Пользователь уже существует."})
            response.status_code = 402
            return response, 402
    return render_template('registration.html')

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
            'title': ex[1]
        })
    return render_template('contest_problems.html', contest_id=contest_id, problems=exersises)


@app.route('/contest/<int:contest_id>/problem/<int:problem_id>', methods=['GET', 'POST'])
def contest_problem(contest_id, problem_id):
    ex_params = db.get_ex_text(contest_id, problem_id)
    if ex_params[0] == 1:
        problem_type = 'question'
        problem = {
            'id': ex_params[1],
            'title': '. '.join(ex_params[1:3]),
            'description': ex_params[3],
            'options': ex_params[4],
            'correct': ex_params[5]
        }
    else:
        tests = db.get_tests(problem_id)[:3]
        problem_type = 'code'
        problem = {
            'id':  ex_params[1],
            'title': '. '.join(ex_params[1:3]),
            'time': ex_params[3],
            'memory': ex_params[4],
            'input': ex_params[5],
            'output': ex_params[6],
            'description': ex_params[7],
            'input_description': ex_params[8],
            'output_description': ex_params[9],
            'examples': [{'input': tests[i][0], 'output': tests[i][2]} for i in range(len(tests))],
            'compilers': ['Python']
        }

    selected = None
    is_correct = None

    result = None
    if request.method == 'POST':
        if ex_params[0] == 1:
            selected = int(request.form.get('option', -1))
            is_correct = (selected == problem['correct'])
            # selected = int(request.form.get('option', -1))
            # if selected == problem['correct']:
            #     result = 'Правильно'
            # else:
            #     result = 'Неправильно'
        else:
            compiler = request.form.get('compiler')
            code = request.json['code']
            print(code)
            all_tests = db.get_tests(problem_id)
            input = [all_tests[i][0] for i in range(len(all_tests))]
            output = [all_tests[i][2] for i in range(len(all_tests))]
            if test(code, compiler, input, output, float(ex_params[3].split(' ')[0])) == "OK":
                response = jsonify({"status": "success", "message": "Задание решено верно"})
                response.status_code = 200
                return response, 200
            else:
                response = jsonify({"status": "error", "message": "Ошибка при проходе тестирования"})
                response.status_code = 300
                return response, 300

    return render_template('contest_problem.html',
                           contest_id=contest_id,
                           problem=problem,
                           selected=selected,
                           is_correct=is_correct,
                           problem_type=problem_type, 
                           result=result)


if __name__ == '__main__':
    app.run(debug=True)
