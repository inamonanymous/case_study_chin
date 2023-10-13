from flask import Flask, render_template, redirect, request, session, url_for, jsonify
from model import db, Users, Reservations, Frontdesk, Holidays
import calendar
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/db_event_management'
app.secret_key = 'putanginamochin'
app.config['TEMPLATES_AUTO_RELOAD'] = True

db.init_app(app)

@app.route('/save_holiday', methods=['POST', 'GET'])
def save_holiday():
    date, reason = request.form['date'], request.form['reason']
    reservation_obj = Reservations.query.filter_by(bdate=date).first()
    holidays_obj = Holidays.query.filter_by(date=date).first()
    if reservation_obj or holidays_obj:
        return "cannot add, date is reservation or holidays"
    holiday_entry = Holidays(
        date=date,
        reason=reason,
        bdate=datetime.now()
    )

    db.session.add(holiday_entry)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/save_user', methods=['POST', 'GET'])
def save_user():
    if 'email' in session:
        current_user = Users.query.filter_by(email=session.get('email', "")).first()
        if current_user.type == 'admin':
            name, address, email_address, phone_no = request.form['name'], request.form['address'], request.form['email_address'], request.form['phone_no']
            user_entry = Users(
                name=name,
                pwd='password',
                address=address,
                phone=phone_no,
                email=email_address,
                type='staff',
                status='active',
                bdate='not set'
            )
            db.session.add(user_entry)
            db.session.commit()
        return redirect(url_for('dashboard'))
    return redirect(url_for('index'))

@app.route('/save_booking_event', methods=['POST','GET'])
def save_booking_event():

    name, address, phone_no, email_address, reservation_date, reservation_time, no_people = request.form['name'], request.form['address'], request.form['phone_no'], request.form['email_address'], request.form['reservation_date'], request.form['reservation_time'], request.form['no_people']

    users_obj = Users.query.filter_by(id=name).first()

    holidays_all_obj = Holidays.query.filter_by(date=reservation_date).first()
    if holidays_all_obj:
        return "cant book any event on holidays"

    reservation_entry = Reservations(
        uid=users_obj.id,
        ucount=no_people,
        rdate=reservation_date,
        status='PENDING',
        comments='',
        bdate=datetime.now()
    )
    db.session.add(reservation_entry)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/get_calendar/<int:year>/<int:month>', methods=['GET'])
def get_calendar(year, month):
    try:
        # Perform any necessary logic to generate calendar data for the specified year and month
        calendar_data = generate_calendar(year, month)

        # Format the calendar data as a JSON object
        formatted_data = {
            'month_name': calendar.month_name[month],
            'calendar': calendar_data
        }

        # Return the formatted data as JSON
        return jsonify(formatted_data)

    except Exception as e:
        # Handle any errors that may occur during data retrieval
        return jsonify({'error': str(e)}), 500 

@app.route('/option/<option>')
def option(option):
    if 'email' in session:
        # Calculate the current year and month
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month
        current_month_data = display_calendar(current_year, current_month)

        #return the users as list of objects
        users_all_obj = Users.query.all()

        #return the holidays as list of objects
        holidays_all_obj = Holidays.query.all()
        

        #return the events reserved as list of objects
        reservations_all_obj = Reservations.query.all()
        events_and_user_combined = []
        for i in reservations_all_obj:
            user_obj = Users.query.filter_by(id=i.uid).first()
            if user_obj:
                combined_data = {
                'name': user_obj.name,
                'email': user_obj.email,
                'phone': user_obj.phone,
                'rdate': i.rdate,
                'bdate': i.bdate,
                'ucount': i.ucount,
                'status': i.status
                 }
                events_and_user_combined.append(combined_data)

        return render_template('dashboard.html',
                              selected_option=option,
                              current_month_data=current_month_data,
                              users_all_obj=users_all_obj,
                              holidays_all_obj=holidays_all_obj,
                              reservations_all_obj=reservations_all_obj,
                              events_and_user_combined=events_and_user_combined)
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'email' in session:
        
        return render_template('dashboard.html')
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

def generate_calendar(year, month):
    cal = calendar.month(year, month)
    return cal

def display_calendar(year, month):
    cal = generate_calendar(year, month)
    return {'month_name': calendar.month_name[month], 'calendar': cal}


if __name__ == "__main__":
    app.run(debug=True, port="5001")