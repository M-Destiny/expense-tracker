# from flask import Flask, render_template, request, redirect, url_for, session, flash
# from extensions import db
# from werkzeug.security import generate_password_hash, check_password_hash
# import matplotlib.pyplot as plt
# from configparser import ConfigParser
# import os

# app = Flask(__name__)
# print("Flask app initialized")  # Debug line

# app.secret_key = 'secret_key_here'

# # PostgreSQL config
# app.config[
#     'SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:npg_5y2glfHIUvhR@ep-autumn-union-a4m50mi4-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)

# from models import User, Expense


# # @app.route('/')
# # def home():
# #     return redirect(url_for('login'))


# # @app.route('/signup', methods=['GET', 'POST'])
# # def signup():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']

# #         existing_user = User.query.filter_by(username=username).first()
# #         if existing_user:
# #             flash('User already exists')
# #             return render_template('signup.html')

# #         hashed_pw = generate_password_hash(password)
# #         new_user = User(username=username, password=hashed_pw)
# #         db.session.add(new_user)
# #         db.session.commit()
# #         flash('Signup successful, please login')
# #         return redirect(url_for('login'))
# #     return render_template('signup.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         existing_user = User.query.filter_by(username=email).first()
#         if existing_user:
#             flash('User already exists')
#             return render_template('signup.html')

#         hashed_pw = generate_password_hash(password)
#         new_user = User(username=email, password=hashed_pw)
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Signup successful, please login')
#         return redirect(url_for('login'))
#     return render_template('signup.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['email']
#         password = request.form['password']

#         user = User.query.filter_by(username=username).first()
#         if user and check_password_hash(user.password, password):
#             session['user_id'] = user.id
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Invalid credentials or user not found')
#             return redirect(url_for('signup'))
#     return render_template('login.html')


# @app.route('/dashboard')
# def dashboard():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
#     return render_template('dashboard.html')


# @app.route('/add-expense', methods=['POST'])
# def add_expense():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))

#     category = request.form['category']
#     amount = float(request.form['amount'])
#     user_id = session['user_id']
#     new_exp = Expense(user_id=user_id, category=category, amount=amount)
#     db.session.add(new_exp)
#     db.session.commit()
#     return redirect(url_for('dashboard'))


# @app.route('/view-expense')
# def view_expense():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))

#     user_id = session['user_id']
#     expenses = Expense.query.filter_by(user_id=user_id).all()

#     data = {}
#     for e in expenses:
#         data[e.category] = data.get(e.category, 0) + e.amount

#     categories = list(data.keys())
#     values = list(data.values())

#     plt.clf()
#     plt.pie(values, labels=categories, autopct='%1.1f%%')
#     plt.savefig('static/pie_chart.png')

#     plt.clf()
#     plt.bar(categories, values)
#     plt.savefig('static/bar_chart.png')

#     return render_template('expense_popup.html')


# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return redirect(url_for('login'))


# if __name__ == '__main__':
#     print("Starting app...")  # Debug
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-GUI support

import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for, session, flash
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Expense
import matplotlib.pyplot as plt
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key_here'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:npg_5y2glfHIUvhR@ep-autumn-union-a4m50mi4-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(username=email).first()
        if existing_user:
            flash('User already exists', 'error')
            return render_template('signup.html')

        hashed_pw = generate_password_hash(password)
        new_user = User(username=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(username=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'error')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).all()

    total_spent = sum(e.amount for e in expenses)
    monthly_budget = 10000.0  # Example fixed value
    remaining_budget = monthly_budget - total_spent

    return render_template('index.html', expenses=expenses, total_spent=total_spent, monthly_budget=monthly_budget, remaining_budget=remaining_budget)
# @app.route('/expenses')
# def expenses():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).all()

    total_spent = sum(e.amount for e in expenses)
    monthly_budget = 10000.0  # Example fixed value
    remaining_budget = monthly_budget - total_spent

    # Prepare data for the charts
    data = {}
    for e in expenses:
        data[e.category] = data.get(e.category, 0) + e.amount

    categories = list(data.keys())
    values = list(data.values())

    os.makedirs("static/images", exist_ok=True)

    # Generate Pie Chart
    plt.clf()
    plt.pie(values, labels=categories, autopct='%1.1f%%')
    plt.savefig('static/images/pie_chart.png')

    # Generate Bar Chart
    plt.clf()
    plt.bar(categories, values)
    plt.savefig('static/images/bar_graph.png')

    return render_template('ExpenseInsights.html', 
                           expenses=expenses, 
                           total_spent=total_spent, 
                           monthly_budget=monthly_budget, 
                           remaining_budget=remaining_budget)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    # Retrieve total spent, monthly budget, and remaining budget
    total_spent = sum(expense.amount for expense in Expense.query.filter_by(user_id=user_id).all())
    user = User.query.get(user_id)
    monthly_budget = user.monthly_budget if user.monthly_budget else 0
    remaining_budget = monthly_budget - total_spent

    expenses = Expense.query.filter_by(user_id=user_id).all()

    return render_template('index.html', total_spent=total_spent, remaining_budget=remaining_budget, monthly_budget=monthly_budget, expenses=expenses)

@app.route('/expenses')
def expenses():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).all()

    total_spent = sum(e.amount for e in expenses)
    monthly_budget = 10000.0  # Example fixed value
    remaining_budget = monthly_budget - total_spent

    # Prepare data for the charts
    data = {}
    for e in expenses:
        data[e.category] = data.get(e.category, 0) + e.amount

    categories = list(data.keys())
    values = list(data.values())

    os.makedirs("static/images", exist_ok=True)

    # Generate Pie Chart
    plt.clf()
    plt.pie(values, labels=categories, autopct='%1.1f%%')
    plt.savefig('static/images/pie_chart.png')

    # Generate Bar Chart
    plt.clf()
    plt.bar(categories, values)
    plt.savefig('static/images/bar_graph.png')

    return render_template('ExpenseInsights.html', 
                           expenses=expenses, 
                           total_spent=total_spent, 
                           monthly_budget=monthly_budget, 
                           remaining_budget=remaining_budget)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    description = request.form['description']
    category = request.form['category']
    amount = float(request.form['amount'])
    date = request.form['date']

    new_exp = Expense(user_id=session['user_id'], category=category, amount=amount, date=date, description=description)
    db.session.add(new_exp)
    db.session.commit()
    return redirect(url_for('dashboard'))
# @app.route('/set_budget', methods=['POST'])
# def set_budget():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    new_budget = float(request.form['monthly_budget'])
    
    # Assuming you have a column in the User model to store the budget
    user = User.query.get(user_id)
    user.monthly_budget = new_budget
    db.session.commit()

    flash('Monthly budget updated successfully!', 'success')
    return redirect(url_for('dashboard'))
@app.route('/set_budget', methods=['POST'])
def set_budget():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    monthly_budget = request.form['monthly_budget']

    # Update the budget in the database (assuming a 'User' model has a 'monthly_budget' field)
    user = User.query.get(user_id)
    user.monthly_budget = float(monthly_budget)
    db.session.commit()

    # Redirect to the homepage after updating the budget
    return redirect(url_for('index'))  # Ensure 'index' route is defined as shown above

    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    monthly_budget = request.form['monthly_budget']

    # Update the budget in the database (assuming a 'User' model has a 'budget' field)
    user = User.query.get(user_id)
    user.monthly_budget = monthly_budget
    db.session.commit()

    # After updating, you may want to redirect to the same page or a different page
    return redirect(url_for('index'))  # Redirect to the home page or wherever you want

@app.route('/delete_expense/<int:expense_id>')
def delete_expense(expense_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    exp = Expense.query.get(expense_id)
    if exp and exp.user_id == session['user_id']:
        db.session.delete(exp)
        db.session.commit()
    return redirect(url_for('dashboard'))

# @app.route('/insights')
# def insights():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))

#     user_id = session['user_id']
#     expenses = Expense.query.filter_by(user_id=user_id).all()
#     data = {}
#     for e in expenses:
#         data[e.category] = data.get(e.category, 0) + e.amount

#     categories = list(data.keys())
#     values = list(data.values())

#     os.makedirs("static/images", exist_ok=True)

#     # Pie Chart
#     plt.clf()
#     plt.pie(values, labels=categories, autopct='%1.1f%%')
#     plt.savefig('static/images/pie_chart.png')

#     # Bar Chart
#     plt.clf()
#     plt.bar(categories, values)
#     plt.savefig('static/images/bar_graph.png')

#     return render_template('ExpenseInsights.html')
# @app.route('/insights')
# def insights():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))

#     print("Inside /insights route")  # Debug print

#     user_id = session['user_id']
#     expenses = Expense.query.filter_by(user_id=user_id).all()
#     data = {}
#     for e in expenses:
#         data[e.category] = data.get(e.category, 0) + e.amount

#     categories = list(data.keys())
#     values = list(data.values())

#     os.makedirs("static/images", exist_ok=True)

#     # Pie Chart
#     plt.clf()
#     plt.pie(values, labels=categories, autopct='%1.1f%%')
#     plt.savefig('static/images/pie_chart.png')

#     # Bar Chart
#     plt.clf()
#     plt.bar(categories, values)
#     plt.savefig('static/images/bar_graph.png')

#     print("Charts generated and saved.")  # Debug print

#     return render_template('ExpenseInsights.html')

@app.route('/insights', methods=['GET'])
def insights():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    print("Inside /insights route")  # Debugging print

    user_id = session['user_id']
    search_date = request.args.get('search_date')  # Get the search date from the URL
    print(f"Searching for date: {search_date}")  # Debugging print

    # If a search date is provided, filter the expenses by the date
    if search_date:
        expenses = Expense.query.filter_by(user_id=user_id, date=search_date).all()
    else:
        expenses = Expense.query.filter_by(user_id=user_id).all()

    # Aggregate expenses by category for chart data
    data = {}
    for e in expenses:
        data[e.category] = data.get(e.category, 0) + e.amount

    categories = list(data.keys())
    values = list(data.values())

    # Generate and save the charts
    os.makedirs("static/images", exist_ok=True)

    # Pie Chart
    plt.clf()
    plt.pie(values, labels=categories, autopct='%1.1f%%')
    plt.savefig('static/images/pie_chart.png')

    # Bar Chart
    plt.clf()
    plt.bar(categories, values)
    plt.savefig('static/images/bar_graph.png')

    print("Charts generated and saved.")  # Debugging print

    return render_template('ExpenseInsights.html', expenses=expenses)



@app.route('/search_expenses')
def search_expenses():
    search_date = request.args.get('search_date')
    if not search_date:
        return redirect('/')  # or wherever your home is

    expenses = Expense.query.filter_by(date=search_date).all()
    
    return render_template('index.html', expenses=expenses)  # Use your actual template name

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)