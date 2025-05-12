from flask import Flask, render_template, request, jsonify, url_for
import flask
from sql_interface import DataBaseInterface
from unittest import test
import json

app = Flask(__name__)
app.secret_key ="super secret key"
db = DataBaseInterface()


@app.route('/')
def welcome():
    if 'user_data' in flask.session:
        flask.session.pop('user_data', None)

    if 'admin_id' in flask.session:
        flask.session.pop('admin_id', None)


    return render_template('welcome.html')


@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        data = request.json
        db_response = db.get_user(data['username'], data['password'])
        if db_response:
            response = jsonify({"status": "success", "message": "Успешный вход"})
            response.status_code = 200
            flask.session['user_data'] =db_response
            return response, 200
        else:
            response = jsonify({"status": "error", "message": "Ошибка авторизации. Неправильные логин или пароль."})
            response.status_code = 401
            return response, 401
    return render_template('login_user.html')

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        data = request.json
        db_response = db.get_admin(data['username'], data['password'])
        if db_response:
            response = jsonify({"status": "success", "message": "Успешный вход"})
            response.status_code = 200
            flask.session['admin_id'] = db_response[0]
            return response, 200
        else:
            response = jsonify({"status": "error", "message": "Ошибка авторизации. Неправильные логин или пароль."})
            response.status_code = 401
            return response, 401

    return render_template('login_admin.html')

@app.route('/user_profile')
def user_profile():
    if 'user_data' not in flask.session:
        return flask.redirect(url_for('login_user'))

    #todo: Добавить динамическое отображение результатов контестов

    user_data = flask.session['user_data']
    return render_template('user_profile.html', user_nickname=user_data[1],user_login=user_data[2])




@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        data = request.json
        if db.add_user(data['nickname'], data['username'], data['password']):
            response = jsonify({"status": "success", "message": "Успешная регистрация"})
            response.status_code = 200
            db_response = db.get_user(data['username'], data['password'])
            flask.session['user_data'] =db_response
            return response, 200
        else:
            response = jsonify({"status": "error", "message": "Ошибка регстрации. Пользователь с таким логином уже существует."})
            response.status_code = 402
            return response, 402
    return render_template('registration.html')

@app.route('/contests')
def contests():
    if 'user_data' not in flask.session:
        return flask.redirect(url_for('login_user'))
    active_contest = int(db.get_user_active_contest(flask.session['user_data'][0])[0])
    if active_contest != -1:
        return flask.redirect(f'/contest/{active_contest}/problems')

    contests = []
    for contest in db.get_all_contests():
        contests.append({
            'id': contest[0],
            'name': contest[1]})
    return render_template('contests.html', contests=contests)

@app.route('/contests_admin', methods=['GET', 'POST'])
def contests_admin():
    if 'admin_id' not in flask.session:
        return flask.redirect(url_for('login_admin'))

    if request.method == 'POST':
        data = request.json
        if data['type']=='delete':
            db.delete_contest(data['id'])
            response = jsonify({"status": "success", "message": "Удаление прошло успешно"})
            response.status_code = 200
            return response, 200

        if data['type']=='add':
            print('add')
            db.add_contest(data['name'],data['description'])
            response = jsonify({"status": "success", "message": "Добавление произошло успешно"})
            response.status_code = 200
            return response, 200

        response = jsonify({"status": "error", "message": "Ошибка"})
        response.status_code = 402
        return response, 402


    contests = []
    for contest in db.get_all_contests():
        contests.append({
            'id': contest[0],
            'name': contest[1]})
    return render_template('contests_admin.html', contests=contests)


@app.route('/contest/<int:contest_id>', methods=['GET', 'POST'])
def contest_details(contest_id):
    if request.method == 'POST':
        active_contest = db.get_user_active_contest(int(flask.session['user_data'][0]))[0]
        if active_contest != -1:
            response = jsonify({"status": "error", "message": f"Ошибка, вы уже проходите контест {active_contest}"})
            response.status_code = 402
            return response, 402
        data = request.get_json() or {}
        redirect_url = data.get('redirect_url') or url_for('contest_problems', contest_id=contest_id)
        contest_id = int(redirect_url.split('/')[2])
        db.set_user_active_contest(contest_id, int(flask.session['user_data'][0]))
        return jsonify({'redirect_url': url_for('contest_problems', contest_id=contest_id)}), 200
    
    else:
        if 'user_data' not in flask.session:
            return flask.redirect(url_for('login_user'))

        db_res = db.get_contest_by_id(contest_id)
        contest = {
            'id': db_res[0],
            'name': db_res[1],
            'description': db_res[2]
        }
        return render_template('contest_details.html', contest=contest)

@app.route('/contest_admin/<int:contest_id>', methods=['GET', 'POST'])
def contest_details_admin(contest_id):
    if 'admin_id' not in flask.session:
        return flask.redirect(url_for('login_admin'))

    if request.method == 'POST':
        data = request.json

        db.update_contest(contest_id,data['name'],data['description'])
        response = jsonify({"status": "success", "message": "Данные обновлены"})
        response.status_code = 200
        return response, 200


    db_res = db.get_contest_by_id(contest_id)
    contest = {
        'id': db_res[0],
        'name': db_res[1],
        'description': db_res[2]
    }
    return render_template('contest_details_admin.html', contest=contest)


@app.route('/contest/<int:contest_id>/problems', methods=['GET', 'POST'])
def contest_problems(contest_id):
    if 'user_data' not in flask.session:
        return flask.redirect(url_for('login_user'))

    if request.method == 'POST':
        # print(request.get_json()['contest_id'])
        db.set_user_active_contest(int(flask.session['user_data'][0]), -1)
        # todo: Дописать окончательные расчёты и возможно исправить скрипт
        response = jsonify({"status": "error", "message": "Ошибка"})
        response.status_code = 402
        return response, 402

    exersises = []
    for ex in db.get_contest_exs(contest_id):
        exersises.append({
            'id': ex[0],
            'title': ex[1]
        })
    return render_template('contest_problems.html', contest_id=contest_id, problems=exersises)

@app.route('/contest_admin/<int:contest_id>/problems', methods=['GET', 'POST'])
def contest_problems_admin(contest_id):
    if 'admin_id' not in flask.session:
        return flask.redirect(url_for('login_admin'))

    if request.method == 'POST':
        data = request.json
        
        if data['type']=='add':
            if data['problem_type']=='question':
                db.add_contest_basic_ex(contest_id,
                                        len(db.get_contest_exs(contest_id))+1,
                                        'Название',
                                        'Описание',
                                        json.dumps(['Вариант1'], ensure_ascii=False).encode('utf8'),
                                        0)

                response = jsonify({"status": "success", "message": "Успешное добавление"})
                response.status_code = 200
                return response, 200
            else:
                db.add_contest_code_ex(contest_id,
                                       len(db.get_contest_exs(contest_id))+1,
                                       'Название',
                                       'Время',
                                       'Память',
                                       'Входные данные',
                                       'Выходные данные',
                                       'Описание',
                                       'Описание входных данных',
                                       'Описание выходных данных')

                response = jsonify({"status": "success", "message": "Успешное добавление"})
                response.status_code = 200
                return response, 200

    exersises = []
    for ex in db.get_contest_exs(contest_id):
        exersises.append({
            'id': ex[0],
            'title': ex[1]
        })
    return render_template('contest_problems_admin.html', contest_id=contest_id, problems=exersises)


@app.route('/contest/<int:contest_id>/problem/<int:problem_id>', methods=['GET', 'POST'])
def contest_problem(contest_id, problem_id):
    if 'user_data' not in flask.session:
        return flask.redirect(url_for('login_user'))


    ex_params = db.get_ex_text(contest_id, problem_id)
    if ex_params[0] == 1:
        problem_type = 'question'
        # todo: Относится к нижнему. Если есть ответ, то user_answ = индексу ответа
        problem = {
            'id': ex_params[1],
            'title': '. '.join(ex_params[1:3]),
            'description': ex_params[3],
            'options': ex_params[4],
            'correct': ex_params[5],
            'user_answ': -1
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
            right_answer, wrong_answer, _ = db.get_global_stats(int(flask.session['user_data'][0]))
            if is_correct:
                right_answer += 1
            else:
                wrong_answer += 1
            db.update_global_stats(int(flask.session['user_data'][0]), right_answer, wrong_answer)
            # todo: Добавить сохранение ответов. Чтобы пользователь не мог дважды ответить на вопрос

            # selected = int(request.form.get('option', -1))
            # if selected == problem['correct']:
            #     result = 'Правильно'
            # else:
            #     result = 'Неправильно'
        else:
            compiler = request.json['compiler'].lower()
            code = request.json['code']
            all_tests = db.get_tests(problem_id)
            input = [all_tests[i][0] for i in range(len(all_tests))]
            output = [all_tests[i][2] for i in range(len(all_tests))]
            res = test(code, compiler, input, output, float(ex_params[3].split(' ')[0]))
            right_answer, wrong_answer, _ = db.get_global_stats(int(flask.session['user_data'][0]))
            if res == "OK":
                response = jsonify({"status": "success", "message": "Задание решено верно"})
                right_answer += 1
                db.update_global_stats(int(flask.session['user_data'][0]), right_answer, wrong_answer)
                response.status_code = 200
                return response, 200
            else:
                response = jsonify({"status": "error", "message": "Ошибка при проходе тестирования"})
                wrong_answer += 1
                db.update_global_stats(int(flask.session['user_data'][0]), right_answer, wrong_answer)
                response.status_code = 300
                return response, 300

    #Вычисление предыдущего и прошлого задания для кнопки перехода
    prev_problem_id = None
    next_problem_id = None

    db_exs=db.get_contest_exs(contest_id)
    for i, ex in enumerate(db_exs):
        if ex[0]==problem_id:
            if i!=0:
                prev_problem_id=db_exs[i-1][0]

            if i!=len(db_exs)-1:
                next_problem_id=db_exs[i+1][0]
            break


    return render_template('contest_problem.html',
                           contest_id=contest_id,
                           problem=problem,
                           selected=selected,
                           is_correct=is_correct,
                           problem_type=problem_type, 
                           result=result,
                           prev_problem_id=prev_problem_id,
                           next_problem_id=next_problem_id
                           )

@app.route('/contest_admin/<int:contest_id>/problem/<int:problem_id>', methods=['GET', 'POST'])
def contest_problem_admin(contest_id, problem_id):
    if 'admin_id' not in flask.session:
        return flask.redirect(url_for('login_admin'))

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
        data = request.json
        if ex_params[0] == 1:
            if data['problem_type']=='question':
                print(ex_params[-1])
                db.update_contest_basic_ex(ex_params[-1], '.'.join(data['name'].split('.')[1:]), data['description'], data['items'], data['index'], 0, 0)
                response = jsonify({"status": "success", "message": "Успешное добавление"})
                response.status_code = 200
                return response, 200

            # selected = int(request.form.get('option', -1))
            # is_correct = (selected == problem['correct'])
            # selected = int(request.form.get('option', -1))
            # if selected == problem['correct']:
            #     result = 'Правильно'
            # else:
            #     result = 'Неправильно'
        else:
            print(data)
            db.update_contest_code_ex(ex_params[-1], data['title'], data['time'], data['memory'], data['input'], data['output'], data['desc'], data['input_desc'], data['output_desc'], 0, 0)
            for i in range(len(data['unittest'])):
                db.add_test(problem_id, data['unittest'][i]['input'], "", data['unittest'][i]['output'])
            response = jsonify({"status": "success", "message": "Успешное добавление"})
            response.status_code = 200
            return response, 200
    else:
        return render_template('contest_problem_admin.html',
                           contest_id=contest_id,
                           problem=problem,
                           selected=selected,
                           is_correct=is_correct,
                           problem_type=problem_type,
                           result=result)


if __name__ == '__main__':
    app.run(debug=True)
