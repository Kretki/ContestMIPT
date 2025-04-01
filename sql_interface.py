import sqlite3

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
            password TEXT
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()

        query = f'''
        CREATE TABLE IF NOT EXISTS {"GlobalUserStatistics"} (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            right_answer INT,
            wrong_answer INT,
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
            ex_id INT
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()

        query = f'''
        CREATE TABLE IF NOT EXISTS {"Exersises"} (
            ex_id INTEGER PRIMARY KEY AUTOINCREMENT,
            contest_id INT,
            ex_number INT,
            ex_desc TEXT, 
            ex_type INT,
            right_answers INT,
            wrong_answers INT,
            answer_text TEXT
        )
        '''
        self.cursor.execute(query)
        self.conn.commit()

        query = f'''
        CREATE TABLE IF NOT EXISTS {"Tests"} (
            unittest_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ex_id INT,
            test_code TEXT
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

    def add_user(self, nickname, login, password):
        query = "INSERT INTO User (nickname, login, password) VALUES (?, ?, ?)"
        self.cursor.execute(query, (nickname, login, password))
        self.conn.commit()
    
    def add_test(self, ex_id, test_code):
        query = "INSERT INTO Tests (ex_id, test_code) VALUES (?, ?)"
        self.cursor.execute(query, (ex_id, test_code))
        self.conn.commit()
    
    def add_contest_ex(self, contest_id, ex_number, ex_desc, ex_type, right_answers, wrong_answers, answer_text):
        query = "INSERT INTO Exersises (contest_id, ex_number, ex_desc, ex_type, right_answers, wrong_answers, answer_text) VALUES (?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, (contest_id, ex_number, ex_desc, ex_type, right_answers, wrong_answers, answer_text))
        self.conn.commit()
        query = "SELECT last_insert_rowid() FROM Exersises"
        self.cursor.execute(query, ())
        query = "INSERT INTO ContestExs (contest_id, ex_id) VALUES (?, ?)"
        self.cursor.execute(query, (contest_id, self.cursor.lastrowid))
        self.conn.commit()

    def add_contest(self, contest_name, contest_desc):
        query = '''INSERT INTO Contest (contest_name, contest_desc) VALUES (?, ?)'''
        self.cursor.execute(query, (contest_name, contest_desc))
        self.conn.commit()
    
    def add_admin(self, nickname, login, password):
        query = "INSERT INTO Administrator (nickname, login, password) VALUES (?, ?, ?)"
        self.cursor.execute(query, (nickname, login, password))
        self.conn.commit()
    
    def get_user(self, username, password):
        query = "SELECT * FROM User WHERE login =? AND password =?"
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone()
    
    def get_admin(self, username, password):
        query = "SELECT * FROM Administrator WHERE login =? AND password =?"
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone()
    
    def get_contest_exs(self, contest_id):
        query = "SELECT ex_id, ex_number FROM Exersises WHERE contest_id =?"
        self.cursor.execute(query, (contest_id,))
        return self.cursor.fetchall()
    
    def get_tests(self, ex_id):
        query = "SELECT * FROM Tests WHERE ex_id =?"
        self.cursor.execute(query, (ex_id,))
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
    
    def update_global_stats(self, user_id, ex_id, right_answer, wrong_answer):
        query = '''INSERT INTO GlobalUserStatistics (right_answer, wrong_answer, user_id, ex_id) VALUES (?,?,?,?) 
        ON CONFLICT (user_id, ex_id) 
        DO UPDATE SET right_answer =?, wrong_answer =?'''
        self.cursor.execute(query, (right_answer, wrong_answer, user_id, ex_id, right_answer, wrong_answer))

    def update_contest(self, contest_id, contest_name, contest_desc):
        query = "UPDATE Contest SET contest_name =?, contest_desc =? WHERE contest_id =?"
        self.cursor.execute(query, (contest_name, contest_desc, contest_id))
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

    def delete_ex(self, ex_id):
        query = "DELETE FROM Exersises WHERE contest_id =?"
        self.cursor.execute(query, (ex_id,))
        self.conn.commit()
    
    def delete_test(self, unittest_id):
        query = "DELETE FROM Tests WHERE unittest_id =?"
        self.cursor.execute(query, (unittest_id,))
        self.conn.commit()

    def delete_contest_ex(self, contest_id, ex_id):
        query = "DELETE FROM ContestExs WHERE contest_id =? AND ex_id =?"
        self.cursor.execute(query, (contest_id, ex_id))
        self.conn.commit()

if __name__ == "__main__":  
    db = DataBaseInterface()
    db.add_user("User", "user", "password")
    db.add_admin("Admin", "admin", "password")
    db.add_contest("Контест 1", "Это пробный контест под номером 1 для проверки системы")
    db.add_contest_ex(1, 1, "Напишите программу для вычисления: 3x + 2 = 5", 2, "", "", "")
    db.add_contest_ex(1, 2, "Напишите программу для вычисления: 2x - 5 = 10", 2, "", "", "")
    db.add_contest_ex(1, 3, "Напишите программу для вычисления: 5x - 1 = 10", 2, "", "", "")
    db.add_contest("Контест 2", "Это пробный контест под номером 2 для проверки системы")
    db.add_contest_ex(2, 1, "Напишите программу для вычисления: 33x + 2 = 5", 2, "", "", "")
    db.add_contest_ex(2, 2, "Напишите программу для вычисления: 12x - 5 = 10", 2, "", "", "")
    db.add_contest_ex(2, 3, "Напишите программу для вычисления: 52x - 1 = 10", 2, "", "", "")