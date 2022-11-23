from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models.models_user import User
from flask_app.models.models_habit import Habit
from flask_app.models.models_day import Day

from flask_app.config.mysqlconnection import connectToMySQL

import math

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect("/")
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_one(user_data)
    all = Habit.get_all_habits()
    days = Day.get_all_days(user_data)

    return render_template('dashboard.html', user = user, all = all, days = days)

# Adding a Quitter
@app.route('/new')
def add_habit():
    return render_template('/new_quitter.html')



#Update Habit
@app.route('/edit/<int:habit_id>')
def edit_habit(habit_id):
    data = {
        'id' : habit_id
    }
    habit = Habit.get_one(data)
    return render_template('edit.html', habit = habit)

# Update Habit - Update Post Method
@app.route('/update_habit/<int:habit_id>', methods=['POST'])
def update_habit(habit_id):
    valid = Habit.update_validator(request.form)
    print(valid)
    if valid:
        Habit.update_habit(request.form, habit_id)
        return redirect('/dashboard')
    return redirect(f'/edit/{habit_id}')


#Delete Quitter
@app.route('/delete/<int:habit_id>')
def delete(habit_id):
    data = {
        'id' : habit_id
    }
    Habit.delete(data)
    return redirect ('/dashboard')

#View Quitter
@app.route('/view/<int:habit_id>')
def view_habit(habit_id):
    data = {
        'id' : habit_id
    }
    habit = Habit.get_one(data)
    return render_template ('view.html', habit = habit)

# @app.route('/habit/<int:habit_id>/day/28')
# def back(habit_id,):
#     data = {
#         'id' : habit_id,
#     }
#     habits = Habit.get_one(data)
#     return render_template ('week.html', habits = habits)


@app.route('/inspire')
def register_inspire():
    return render_template('/inspire.html')

@app.route('/risks')
def risks():
    return render_template('/risks.html')


# # !misc quieres for days 
@app.route('/habit/<int:habit_id>/day/<int:day_num>')
def week(habit_id, day_num):
    data = {
        'id' : habit_id,
        'day_num' : day_num
    }
    habits = Habit.get_one(data)
    day = Day.get_one_day(data)
    return render_template ('week.html', day = day , habits = habits)



# ! misc quieres for weeks in accordian
@app.route('/habit/<int:habit_id>/day/<int:week_num>')
def cur_smoke(habit_id, week_num):
    data = {
        'id' : habit_id,
        'start_num' : (week_num * 7) - 6,
        'end_num' : (week_num * 7)
    }
    # habits = Habit.get_one(data)
    week = Day.get_one_week(data)
    return render_template ('week1.html', week = week, week_num = week_num)


@app.route('/benefits')
def quitting_benefits():
    return render_template('/benefits.html')



# # ! stays here
@app.route('/create_habit', methods = ['POST'])
def allowance():
    data = {
        'number' : request.form['number'],
        'cost' : request.form['cost'],
        'year' : request.form['year'],
        'method' : request.form['method'],
        'why' : request.form['why'],
        'user_id' :session['user_id'],
    }
    valid = Habit.habit_validator(data)
    if valid:   
        allowance_num = int(request.form['number'])
        habit_id=Habit.create_habit(data)
        for x in range (0,28):
            if request.form['method'] == "Cold Turkey":
                allowed = 0
            elif x <= 6:
                allowed = math.floor(allowance_num * .75)
            elif x <= 13:
                allowed = math.floor(allowance_num * .50)
            elif x <= 20:
                allowed = math.floor(allowance_num * .25)
            elif x <= 27:
                allowed = math.floor(allowance_num * .00)
            day_num = x + 1
            data = {
                'habit_id' : habit_id,
                'allowed' : allowed,
                'smoked' : 0,
                'day_num' : day_num
            }
            Day.create_day(data)  
        return redirect ('/dashboard')
    return redirect ('/new')

# # ! stays here
@app.route('/smoked', methods = ['POST'])
def smoked():
    Day.days_smoked(request.form)
    return redirect (request.referrer)

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect("/")
    user_data = {
        'id' : session['user_id']
    }
    user = User.get_one(user_data)
    days = Day.get_all_days(user_data)
    return render_template('history.html', days = days, user = user)

