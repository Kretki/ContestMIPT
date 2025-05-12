import sqlite3
import json

class DataBaseInterface:
    def __init__(self, db_name="er-database.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL;")  # Ensures better write concurrency
        self.cursor = self.conn.cursor()

        query = f'''
        CREATE TABLE IF NOT EXISTS {"User"} (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT,
            login TEXT,
            password TEXT,
            active_contest_id INT
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()

        query = f'''
        CREATE TABLE IF NOT EXISTS {"GlobalUserStatistics"} (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            active_contest_id INT,
            answer INT,
            user_id INT,
            ex_id INT
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()

        query = f'''
        CREATE TABLE IF NOT EXISTS {"Contest"} (
            contest_id INTEGER PRIMARY KEY AUTOINCREMENT,
            contest_name TEXT,
            contest_desc TEXT
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()

        query = f'''
        CREATE TABLE IF NOT EXISTS {"ContestExs"} (
            UniqueID INTEGER PRIMARY KEY AUTOINCREMENT,
            contest_id INT,
            ex_id INT,
            ex_type INT
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()

        query = f'''
        CREATE TABLE IF NOT EXISTS {"BasicExersises"} (
            ex_id INTEGER PRIMARY KEY AUTOINCREMENT,
            contest_id INT,
            ex_number INT,
            ex_title TEXT, 
            ex_desc TEXT
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()

        query = f'''
        CREATE TABLE IF NOT EXISTS {"CodeExersises"} (
            ex_id INTEGER PRIMARY KEY AUTOINCREMENT,
            contest_id INT,
            ex_number INT,
            ex_title TEXT, 
            ex_time TEXT,
            ex_memory TEXT,
            ex_input TEXT,
            ex_output TEXT,
            ex_description TEXT,
            ex_input_description TEXT,
            ex_output_description TEXT
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()

        query = f'''
        CREATE TABLE IF NOT EXISTS {"Tests"} (
            unittest_id INTEGER PRIMARY KEY AUTOINCREMENT,
            UniqueID INT,
            input TEXT,
            test_code TEXT,
            output TEXT
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()

        query = f'''
        CREATE TABLE IF NOT EXISTS {"Administrator"} (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT,
            login TEXT,
            password TEXT
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()
        
        query = f'''
        CREATE TABLE IF NOT EXISTS {"BasicExAnswers"} (
            basic_ex_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ex_id INT,
            text TEXT,
            correct INT
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()

    def add_user(self, nickname, login, password):
        query = "SELECT * FROM User WHERE login =?"
        self.cursor.execute(query, (login,))
        if self.cursor.fetchone():
            return False
        query = "INSERT INTO User (nickname, login, password, active_contest_id) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (nickname, login, password, -1))
        self.conn.commit()
        return True
    
    def get_user_active_contest(self, user_id):
        query = "SELECT active_contest_id FROM User WHERE user_id =?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()
    
    def set_user_active_contest(self, user_id, contest_id):
        query = "UPDATE User SET active_contest_id=? WHERE user_id=?"
        self.cursor.execute(query, (contest_id, user_id))
        self.conn.commit()
    
    def add_test(self, UniqueID, input, test_code, output):
        query = "INSERT INTO Tests (UniqueID, input, test_code, output) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (UniqueID, input, test_code, output))
        self.conn.commit()

    def add_contest_basic_ex(self, contest_id, ex_number, ex_title, ex_desc, ex_options, ex_right_answer):
        query = "INSERT INTO BasicExersises (contest_id, ex_number, ex_title, ex_desc) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (contest_id, ex_number, ex_title, ex_desc))
        self.conn.commit()
        query = "SELECT last_insert_rowid() FROM BasicExersises"
        self.cursor.execute(query, ())
        query = "INSERT INTO ContestExs (contest_id, ex_id, ex_type) VALUES (?, ?, ?)"
        ex_id = self.cursor.lastrowid
        self.cursor.execute(query, (contest_id, ex_id, 1))
        self.conn.commit()
        for i in range(len(ex_options)):
            correct = 0
            if i == ex_right_answer:
                correct = 1
            query = "INSERT INTO BasicExAnswers (ex_id, text, correct) VALUES (?,?,?)"
            self.cursor.execute(query, (ex_id, ex_options[i], correct))
            self.conn.commit()
    
    def add_contest_code_ex(self, contest_id, ex_number, ex_title, ex_time, ex_memory, ex_input, ex_output, ex_description, ex_input_description, ex_output_description):
        query = "INSERT INTO CodeExersises (contest_id, ex_number, ex_title, ex_time, ex_memory, ex_input, ex_output, ex_description, ex_input_description, ex_output_description) VALUES (?,?,?,?,?,?,?,?,?,?)"
        self.cursor.execute(query, (contest_id, ex_number, ex_title, ex_time, ex_memory, ex_input, ex_output, ex_description, ex_input_description, ex_output_description))
        self.conn.commit()
        query = "SELECT last_insert_rowid() FROM CodeExersises"
        self.cursor.execute(query, ())
        query = "INSERT INTO ContestExs (contest_id, ex_id, ex_type) VALUES (?, ?, ?)"
        uniqueId = self.cursor.lastrowid
        self.cursor.execute(query, (contest_id, uniqueId, 2))
        self.conn.commit()
        return uniqueId

    def add_contest(self, contest_name, contest_desc):
        query = '''INSERT INTO Contest (contest_name, contest_desc) VALUES (?, ?)'''
        self.cursor.execute(query, (contest_name, contest_desc))
        self.conn.commit()
    
    def add_admin(self, nickname, login, password):
        query = "INSERT INTO Administrator (nickname, login, password) VALUES (?, ?, ?)"
        self.cursor.execute(query, (nickname, login, password))
        self.conn.commit()
    
    def add_test(self, UniqueID, input, test_code, output):
        query = "INSERT INTO Tests (UniqueID, input, test_code, output) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (UniqueID, input, test_code, output))
        self.conn.commit()
    
    def get_user(self, username, password):
        query = "SELECT * FROM User WHERE login =? AND password =?"
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone()
    
    def get_admin(self, username, password):
        query = "SELECT * FROM Administrator WHERE login =? AND password =?"
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone()
    
    def get_user_stats(self, user_id):
        query = "SELECT * FROM GlobalUserStatistics"
        self.cursor.execute(query)
        all_exs = self.cursor.fetchall()
        contests = []
        scores = []
        users = []
        places = []
        for (_, contest_id, correct, _, ex_id) in all_exs:
            if self.get_contest_by_id(contest_id)[1] not in contests:
                query = "SELECT COUNT(*) FROM ContestExs WHERE contest_id=?"
                self.cursor.execute(query, (contest_id,))
                count_all_exs = self.cursor.fetchone()[0]
                query = "SELECT SUM(answer) FROM GlobalUserStatistics WHERE active_contest_id=? AND user_id=?"
                self.cursor.execute(query, (contest_id, user_id))
                count_all_correct = self.cursor.fetchone()[0]
                query = "SELECT COUNT(*) FROM (SELECT user_id FROM GlobalUserStatistics WHERE active_contest_id=? GROUP BY user_id)"
                self.cursor.execute(query, (contest_id,))
                count_users = self.cursor.fetchone()[0]
                query = '''
                    SELECT ROW_NUMBER() OVER(ORDER BY score DESC) 
                    FROM 
                    (
                        SELECT user_id, SUM(answer) AS score 
                        FROM GlobalUserStatistics 
                        WHERE active_contest_id=? 
                        GROUP BY user_id 
                    ) WHERE user_id=?
                    
                '''
                self.cursor.execute(query, (contest_id, user_id))
                places_users = self.cursor.fetchone()[0]
                contests.append(self.get_contest_by_id(contest_id)[1])
                scores.append(f"{count_all_correct}/{count_all_exs}")
                users.append(count_users)
                places.append(places_users)
        return contests, scores, users, places
    
    def get_contest_exs(self, contest_id):
        query = "SELECT UniqueID, contest_id, ex_id, ex_type FROM ContestExs WHERE contest_id =?"
        self.cursor.execute(query, (contest_id,))
        exList = self.cursor.fetchall()
        resList = []
        for item in exList:
            if item[3] == 1:
                query = "SELECT ex_id, ex_number, ex_title FROM BasicExersises WHERE ex_id =?"
                self.cursor.execute(query, (item[2],))
                res = self.cursor.fetchone()
                resList.append((item[0], ". ".join(str(x) for x in res[1:])))
            elif item[3] == 2:
                query = "SELECT ex_id, ex_number, ex_title FROM CodeExersises WHERE ex_id =?"
                self.cursor.execute(query, (item[2],))
                res = self.cursor.fetchone()
                resList.append((item[0], ". ".join(str(x) for x in res[1:])))
        return resList

    def get_ex_text(self, contest_id, unique_id):
        query = "SELECT ex_id, ex_type FROM ContestExs WHERE contest_id =? AND UniqueID =?"
        self.cursor.execute(query, (contest_id, unique_id,))
        exParams = self.cursor.fetchall()[0]
        if exParams[1] == 1:
            query = "SELECT ex_number, ex_title, ex_desc FROM BasicExersises WHERE ex_id =?"
            self.cursor.execute(query, (exParams[0],))
            exText = self.cursor.fetchall()[0]
            query = "SELECT text, correct FROM BasicExAnswers WHERE ex_id=?"
            self.cursor.execute(query, (exParams[0],))
            exOptions = self.cursor.fetchall()
            options = []
            right_answer = 0
            for i in range(len(exOptions)):
                options.append(exOptions[i][0])
                if exOptions[i][1]:
                    right_answer = i
            res = list((exParams[1],) + exText + tuple([options]) + tuple([right_answer]) + (exParams[0],))
            res[1] = str(res[1])
            return res
        else:
            query = "SELECT ex_number, ex_title, ex_time, ex_memory, ex_input, ex_output, ex_description, ex_input_description, ex_output_description FROM CodeExersises WHERE ex_id =?"
            self.cursor.execute(query, (exParams[0],))
            res = list((exParams[1],) + self.cursor.fetchall()[0] + (exParams[0],))
            res[1] = str(res[1])
            return res
    
    def get_tests(self, UniqueID):
        query = "SELECT input, test_code, output FROM Tests WHERE UniqueID =?"
        self.cursor.execute(query, (UniqueID,))
        return self.cursor.fetchall()
    
    def get_contest_by_id(self, contest_id):
        query = "SELECT * FROM Contest WHERE contest_id =?"
        self.cursor.execute(query, (contest_id,))
        return self.cursor.fetchone()
    
    def get_contest_by_name(self, contest_name):
        query = "SELECT * FROM Contest WHERE contest_name =?"
        self.cursor.execute(query, (contest_name,))
        return self.cursor.fetchone()
    
    def get_all_contests(self):
        query = "SELECT contest_id, contest_name FROM Contest"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_global_stats(self, user_id):
        query = "SELECT * FROM GlobalUserStatistics WHERE user_id =?"
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()
    
    def start_contest_stats(self, user_id):
        active_contest_id = self.get_user_active_contest(user_id)[0]
        query = "DELETE FROM GlobalUserStatistics WHERE active_contest_id =? AND user_id=?"
        self.cursor.execute(query, (active_contest_id, user_id,))
        self.conn.commit()
    
    def get_stats_contest_ex(self, user_id, ex_id):
        active_contest_id = self.get_user_active_contest(user_id)[0]
        query = "SELECT answer FROM GlobalUserStatistics WHERE user_id=? AND active_contest_id=? AND ex_id=?"
        self.cursor.execute(query, (user_id, active_contest_id, ex_id))
        return len(self.cursor.fetchall()) == 0
        
    def update_global_stats(self, user_id, ex_id, answer):
        active_contest_id = self.get_user_active_contest(user_id)[0]
        query = "DELETE FROM GlobalUserStatistics WHERE active_contest_id =? AND user_id=? AND ex_id=?"
        self.cursor.execute(query, (active_contest_id, user_id, ex_id,))
        self.conn.commit()
        query = "INSERT INTO GlobalUserStatistics (user_id, active_contest_id, answer, ex_id) VALUES (?,?,?,?)"
        self.cursor.execute(query, (user_id, active_contest_id, answer, ex_id))
        self.conn.commit()

    def update_contest(self, contest_id, contest_name, contest_desc):
        query = "UPDATE Contest SET contest_name =?, contest_desc =? WHERE contest_id =?"
        self.cursor.execute(query, (contest_name, contest_desc, contest_id))
        self.conn.commit()

    def update_contest_basic_ex(self, ex_id, ex_title, ex_desc, ex_options, ex_right_answer):
        query = "UPDATE BasicExersises SET ex_title=?, ex_desc=? WHERE ex_id=?"
        self.cursor.execute(query, (ex_title, ex_desc, ex_id))
        self.conn.commit()
        query = "DELETE FROM BasicExAnswers WHERE ex_id =?"
        self.cursor.execute(query, (ex_id,))
        self.conn.commit()
        for i in range(len(ex_options)):
            correct = 0
            if i == ex_right_answer:
                correct = 1
            query = "INSERT INTO BasicExAnswers (ex_id, text, correct) VALUES (?,?,?)"
            self.cursor.execute(query, (ex_id, ex_options[i], correct))
            self.conn.commit()
    
    def update_contest_code_ex(self, ex_id, ex_title, ex_time, ex_memory, ex_input, ex_output, ex_description, ex_input_description, ex_output_description):
        query = "UPDATE CodeExersises SET ex_title=?, ex_time=?, ex_memory=?, ex_input=?, ex_output=?, ex_description=?, ex_input_description=?, ex_output_description=? WHERE ex_id=?"
        self.cursor.execute(query, (ex_title, ex_time, ex_memory, ex_input, ex_output, ex_description, ex_input_description, ex_output_description, ex_id))
        self.conn.commit()

    def delete_user(self, user_id):
        query = "DELETE FROM User WHERE user_id =?"
        self.cursor.execute(query, (user_id,))
        self.conn.commit()
        query = "DELETE FROM GlobalUserStatistics WHERE user_id =?"
        self.cursor.execute(query, (user_id,))
        self.conn.commit()

    def delete_admin(self, admin_id):
        query = "DELETE FROM Administrator WHERE admin_id =?"
        self.cursor.execute(query, (admin_id,))
        self.conn.commit()
    
    def delete_test(self, unittest_id):
        query = "DELETE FROM Tests WHERE unittest_id =?"
        self.cursor.execute(query, (unittest_id,))
        self.conn.commit()

    def delete_contest_ex(self, contest_id, ex_id):
        query = "DELETE FROM ContestExs WHERE contest_id =? AND ex_id =?"
        self.cursor.execute(query, (contest_id, ex_id))
        self.conn.commit()
    
    def delete_contest(self, contest_id):
        query = "DELETE FROM Contest WHERE contest_id =?"
        self.cursor.execute(query, (contest_id,))
        self.conn.commit()
        query = "DELETE FROM ContestExs WHERE contest_id =?"
        self.cursor.execute(query, (contest_id,))
        self.conn.commit()
        query = "SELECT ex_id FROM BasicExersises WHERE contest_id =?"
        self.cursor.execute(query, (contest_id,))
        exes = self.cursor.fetchall()
        for ex_id in exes:
            query = "DELETE FROM BasicExAnswers WHERE ex_id =?"
            self.cursor.execute(query, (ex_id,))
            self.conn.commit()
        query = "DELETE FROM BasicExersises WHERE contest_id =?"
        self.cursor.execute(query, (contest_id,))
        self.conn.commit()
        query = "DELETE FROM CodeExersises WHERE contest_id =?"
        self.cursor.execute(query, (contest_id,))
        self.conn.commit()

def basic_behaviour():
    db = DataBaseInterface()
    db.add_user("User", "user", "1234")
    db.add_admin("Admin", "admin", "1234")
    db.add_contest("Контест 1", "Это пробный контест под номером 1 для проверки системы")
    db.add_contest_basic_ex(1, 1, 'Палитра', 'Какой цвет получится при смешении синего и жёлтого?', ['Зелёный', 'Фиолетовый', 'Оранжевый', 'Красный'], 0)
    uniqueId = db.add_contest_code_ex(1, 2, 'A+B', '2 секунды', '64 Мб', 'стандартный ввод или input.txt', 'стандартный вывод или output.txt', 'Даны два числа <strong>A</strong> и <strong>B</strong>. Вам нужно вычислить их сумму <strong>A + B</strong>.', 'Первая строка входа содержит числа <strong>A</strong> и <strong>B</strong> (-2 * 10⁹ ≤ A, B ≤ 2 * 10⁹), разделенные пробелом.', 'В единственной строке выхода выведите сумму чисел <strong>A + B</strong>.')
    db.add_test(uniqueId,'2 2', 'print(a+b)', '4')
    db.add_test(uniqueId,'57 43', 'print(a+b)', '100')
    db.add_test(uniqueId,'123456789 673243342', 'print(a+b)', '796700131')
    # db.add_contest_ex(1, 1, "Напишите программу для вычисления: 3x + 2 = 5", 2, "", "", "")
    # db.add_contest_ex(1, 2, "Напишите программу для вычисления: 2x - 5 = 10", 2, "", "", "")
    # db.add_contest_ex(1, 3, "Напишите программу для вычисления: 5x - 1 = 10", 2, "", "", "")
    db.add_contest("Контест 2", "Это пробный контест под номером 2 для проверки системы")
    db.add_contest_basic_ex(2, 1, 'Палитра', 'Какой цвет получится при смешении синего и жёлтого?', ['Зелёный', 'Фиолетовый', 'Оранжевый', 'Красный'], 0)
    uniqueId = db.add_contest_code_ex(2, 2, 'A+C', '2 секунды', '64 Мб', 'стандартный ввод или input.txt', 'стандартный вывод или output.txt', 'Даны два числа <strong>A</strong> и <strong>B</strong>. Вам нужно вычислить их сумму <strong>A + B</strong>.', 'Первая строка входа содержит числа <strong>A</strong> и <strong>B</strong> (-2 * 10⁹ ≤ A, B ≤ 2 * 10⁹), разделенные пробелом.', 'В единственной строке выхода выведите сумму чисел <strong>A + B</strong>.')
    db.add_test(uniqueId,'2 2', 'print(a+b)', '4')
    db.add_test(uniqueId,'57 43', 'print(a+b)', '100')
    db.add_test(uniqueId,'123456789 673243342', 'print(a+b)', '796700131')
    # db.add_contest_ex(2, 1, "Напишите программу для вычисления: 33x + 2 = 5", 2, "", "", "")
    # db.add_contest_ex(2, 2, "Напишите программу для вычисления: 12x - 5 = 10", 2, "", "", "")
    # db.add_contest_ex(2, 3, "Напишите программу для вычисления: 52x - 1 = 10", 2, "", "", "")

if __name__ == "__main__":  
    basic_behaviour()
    # db = DataBaseInterface()