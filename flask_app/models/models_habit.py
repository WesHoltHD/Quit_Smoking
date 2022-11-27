from flask_app.models.models_user import User
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

#db reference
db = "smoke_quitter_final"

#Class - Reference
class Habit:
    def __init__(self, data):
        self.id = data['id']
        self.number = data['number']
        self.cost = data['cost']
        self.year = data['year']
        self.method = data['method']
        self.why = data['why']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.owner = None
        
    # Create Quitter
    @classmethod
    def create_habit(cls, data):
        query = """
                INSERT INTO habits (number, cost, year, method, why, user_id)
                VALUES ( %(number)s, %(cost)s, %(year)s, %(method)s, %(why)s, %(user_id)s)
                """
        return connectToMySQL(db).query_db(query, data)

#Getting All Quitters
    @classmethod
    def all_habits(cls):
        query='SELECT * FROM habits'
        results = connectToMySQL(db).query_db(query)
        habits =[]
        for habit in results:
            habits.append(cls(habit))
        return habits

#Getting One Quitter/User
    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM habits
                JOIN users on users.id = habits.user_id
                WHERE habits.id = %(id)s
                """
        results = connectToMySQL(db).query_db(query, data)
        habit = cls(results[0])
        owner_data ={
            'id' : results[0]['users.id'],
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'dob' : results[0]['dob'],
            'email' : results[0]['email'],
            'password' : results[0]['password'],
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at'],
        
        }
        habit.owner = User(owner_data)
        return habit
    
#Updating Quitter        
    @classmethod
    def update_habit(cls, data, habit_id):
        query = f"UPDATE habits SET cost = %(cost)s, year = %(year)s, why = %(why)s WHERE id= {habit_id}"
        return connectToMySQL(db).query_db(query, data)
    
#Delete Quitter   
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM habits WHERE id = %(id)s;"
        return connectToMySQL(db).query_db( query, data)

#Create Quitter Validator - For Min Values 
    @staticmethod
    def habit_validator(form_data):
        is_valid = True
        if len(form_data['number']) < 1:
            flash ('Number of cigarettes smoked must be greater than 0')
            is_valid = False
        if len(form_data['cost']) < 1:
            flash('Cost per pack of cigarettes must be greater than 1 dollar')
            is_valid = False
        if len(form_data['year']) < 1:
            flash('Year must be greater than 1')
            is_valid = False
        if len(form_data['method']) < 1:
            flash('1 Method Must Be Picked')
            is_valid = False
        if len(form_data['why']) < 8:
            flash ('Reason for quitting must be at least 8 characters')
            is_valid = False
        return is_valid
    
    @staticmethod
    def update_validator(form_data):
        is_valid = True
        if len(form_data['cost']) < 1:
            flash('Cost per pack of cigarettes must be greater than 1 dollar')
            is_valid = False
        if len(form_data['year']) < 1:
            flash('Year must be greater than 1')
            is_valid = False
        if len(form_data['why']) < 8:
            flash ('Reason for quitting must be at least 8 characters')
            is_valid = False
        return is_valid
    

#Getting All Quitters - To Show On Dashboard    
    @classmethod
    def get_all_habits( cls ):
        query = """
        SELECT * FROM habits
        JOIN users ON users.id = habits.user_id
        """
        results = connectToMySQL(db).query_db( query )
        all_habits = []
        for db_row in results:
            one_habit = cls(db_row)
            owner_info = {
                "id" : db_row["users.id"],
                "first_name" : db_row["first_name"],
                "last_name" : db_row["last_name"],
                "dob" : db_row["dob"],
                "email" : db_row["email"],
                "password" : db_row["password"],
                "created_at" : db_row["users.created_at"],
                "updated_at" : db_row["users.updated_at"]
            }
            one_habit.owner = User(owner_info)
            all_habits.append( one_habit )
        return all_habits

#Getting One Habit     same as one get one ; different function name
    @classmethod
    def get_one_habit( cls, data ):
        query = """
                SELECT * FROM habits 
                JOIN users ON users.id = habits.user_id
                WHERE habits.id = %(id)s
                """
        results = connectToMySQL(db).query_db( query, data ) 
        habit = cls(results[0])
        owner_info = {
            "id" : results[0]["users.id"],
            "first_name" : results[0]["first_name"],
            "last_name" : results[0]["last_name"],
            "dob" : results[0]["dob"],
            "email" : results[0]["email"],
            "password" : results[0]["password"],
            "created_at" : results[0]["users.created_at"],
            "updated_at" : results[0]["users.updated_at"]
        }
        habit.owner = User(owner_info)
        return habit
    
    @classmethod
    def delete_habit(cls, data):
        query = "DELETE FROM habits WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data) 
    
    