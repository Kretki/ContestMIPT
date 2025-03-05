import pandas as pd

class SqlExercisesInterface:
    __db : pd.DataFrame
    def __init__(self):
        self.__db = pd.read_csv('db.csv', sep=';')
        self.__db.set_index('id', drop=True, inplace=True)
    def save_db(self):
        self.__db.to_csv('db.csv', sep=';')
    def add(self, number : int, text : str, text_answers : str = "", 
                     value_answer : float = 0., unittest_answer : str = "", 
                     type : int = 0, contest_id : int = 0):
        # type = 0 -> задача с вариантами ответов, type = 1 -> задача на ввод значения, type = 2 -> задача на код
        self.__db.loc[len(self.__db)] = [number, text, text_answers, value_answer, unittest_answer, type, contest_id]
        self.save_db()
        return len(self.__db) - 1
    def delete(self, id : int):
        if id in self.__db.index:
            self.__db.drop([id], inplace=True)
            self.save_db()
    def change(self, id : int, number : int = -1, text : str = "", text_answers : str = "", 
                     value_answer : float = -1., unittest_answer : str = "", 
                     type : int = -1, contest_id : int = -1):
        if id in self.__db.index:
            row = self.__db.iloc[id].copy(deep=True)
            if number != -1: row['number'] = number
            if text != "": row['text'] = text
            if text_answers != "": row['text_answers'] = text_answers
            if value_answer != -1.: row['value_answer'] = value_answer
            if unittest_answer != "": row['unittest_answer'] = unittest_answer
            if type != -1: row['type'] = type
            if contest_id != -1: row['contest_id'] = contest_id
            self.__db.loc[id] = row
            self.save_db()
        else:
            raise KeyError('No such id in the db to change') 
    def get(self, id : int):
        if id in self.__db.index:
            return self.__db.iloc[id].copy(deep=True)
        else:
            raise KeyError('No such id in the db to get') 

if __name__ == '__main__':
    sql = SqlExercisesInterface()
    id = sql.add(1, 1, "Hello")
    sql.change(id, type=2)
    print(sql.get(id))
    sql.delete(id)