from flask_app.models.models_user import User
from flask_app.models.models_habit import Habit
from flask_app.config.mysqlconnection import connectToMySQL


#db reference
db = "Smoke_Quitter_Final"

#Class - Reference
class Day:
    def __init__(self, data):
        self.id = data['id']
        self.allowed = data['allowed']
        self.smoked = data['smoked']
        self.day_num = data['day_num']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.habit_id = data['habit_id']
        self.owner = None
        
    # Create Day
    @classmethod
    def create_day(cls, data):
        query = """
                INSERT INTO days (allowed, smoked, day_num, habit_id)
                VALUES ( %(allowed)s, %(smoked)s, %(day_num)s, %(habit_id)s)
                """
        return connectToMySQL(db).query_db(query, data)

#Getting All Days
    @classmethod
    def all_day(cls):
        query='''
        SELECT * FROM days
        '''
        results = connectToMySQL(db).query_db(query)
        days =[]
        for day in results:
            days.append(cls(day))
        return days


#Updating Day 
# ! does this need an f string?--- all are integers
    @classmethod
    def update_day(cls, data, day_id):
        query = f"UPDATE days SET allowed = %(allowed)s smoked = %(smoked)s, day_num = %(day_num)s WHERE id= {day_id}"
        return connectToMySQL(db).query_db(query, data)
    

#Getting All Quitters - To Show On Dashboard    
    @classmethod
    def get_all_days( cls, data ):
        query = """
        SELECT * FROM days
        JOIN habits ON habits.id = days.habit_id
        WHERE habits.user_id = %(id)s
        """
        results = connectToMySQL(db).query_db( query , data )
        all_days = []
        for db_row in results:
            one_day = cls(db_row)
            all_days.append( one_day )
        return all_days

#Getting One Day    same as one get one ; different function name
    @classmethod
    def get_one_day( cls, data ):
        query = """
                SELECT * FROM days 
                JOIN habits 
                ON habits.id = days.habit_id
                WHERE days.day_num = %(day_num)s
                AND days.habit_id = %(id)s
                """
        results = connectToMySQL(db).query_db( query, data )
        
        print(results[0])
        day = cls(results[0])       
        owner_info = {
                "user_id" : results[0]["user_id"],
                "id" : results[0]["habits.id"],
                "number" : results[0]["number"],
                "cost" : results[0]["cost"],
                "year" : results[0]["year"],
                "method" : results[0]["method"],
                "why" : results[0]["why"],
                "created_at" : results[0]["habits.created_at"],
                "updated_at" : results[0]["habits.updated_at"]
        }
        day.owner = Habit(owner_info)
        return day
    
    @classmethod
    def days_smoked( cls, data):
        query = '''
        UPDATE days SET smoked = smoked + %(smoked)s
        WHERE days.day_num = %(day_num)s
        AND days.habit_id = %(habit_num)s 
        '''
        return connectToMySQL(db).query_db( query, data )