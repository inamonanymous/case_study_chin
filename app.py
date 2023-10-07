from flask import Flask, render_template, redirect, request, session, url_for
from model import db, Users
import calendar

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/db_event_management'
app.secret_key = 'putanginamochin'
db.init_app(app)

def generate_calendar(year, month):
    cal = calendar.month(year, month)
    return cal

@app.route('/calendar')
def display_calendar():
    months = []
    
    # Generate calendars for January to December of a specific year (e.g., 2023)
    year = 2023
    for month in range(1, 13):
        cal = generate_calendar(year, month)
        months.append({'month_name': calendar.month_name[month], 'calendar': cal})

    return render_template('events-calendar.html', months=months)

@app.route('/option/<option>')
def option(option):
    if 'email' in session:
        return render_template('dashboard.html', selected_option=option)
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'email' in session:
        selected_option = request.args.get('option', 'option1')
        return render_template('dashboard.html', selected_option=selected_option)
    return redirect(url_for('index'))

@app.route('/authenticate', methods=['POST', 'GET'])
def authenticate():
    email, password = request.form.get('email'), request.form.get('password')
    if Users.login_is_true(email, password):
        session['email'] = email
        return redirect(url_for('dashboard'))
    return redirect(url_for('index'))

@app.route('/') 
def index():
    session.clear()
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)