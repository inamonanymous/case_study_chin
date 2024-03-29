from flask import Flask, render_template, redirect, request, session, url_for, jsonify, flash
from model import db, Users, Reservations, Frontdesk, Holidays
import calendar
from datetime import datetime
from sqlalchemy import or_, desc
from sqlalchemy.orm import aliased
from flask_migrate import Migrate

app = Flask(__name__)
migrate = Migrate(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/db_event_management'
app.secret_key = 'putanginamochin'
app.config['TEMPLATES_AUTO_RELOAD'] = True

db.init_app(app)

@app.route('/logout')
def logout():
    if 'email' in session:
        session.clear()
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/change-password', methods=['POST'])
def change_password():
    if 'email' in session:
        current_user = Users.query.filter_by(email=session.get('email', "")).first()
        password, password2 = request.form['password'], request.form['password']
        if password != password2 and len(password2)>=8:
            return f"""
                <script>
                    alert("Please make sure the Passwords are matching and the characters is above 8 in length");
                    location.reload(true);
                </script>
                """
        current_user.pwd=password2
        db.session.commit()
        return f"""
                <script>
                    alert("Password Updated");
                    window.location.href='/dashboard';
                </script>
                """
    return redirect(url_for('index'))

@app.route('/edit-credentials', methods=['POST'])
def edit_credentials():
    if 'email' in session:
        current_user = Users.query.filter_by(email=session.get('email', "")).first()
        name, address, phone = request.form['name'], request.form['address'], request.form['phone']
        current_user.name=name
        current_user.address=address
        current_user.phone=phone
        db.session.commit()
        return f"""
                <script>
                    alert("Credentials Updated");
                    window.location.href='/dashboard';
                </script>
                """
    return redirect(url_for('index'))

@app.route('/delete_event/<int:id>', methods=['POST', 'GET'])
def delete_event(id):
    if 'email' in session:
        current_user = Users.query.filter_by(email=session.get('email', "")).first()
        if current_user.type=="admin":
            try:
                target_event = Reservations.query.filter(
                            (Reservations.id == id)).first()
                db.session.delete(target_event)
                db.session.commit()
                return redirect('/option/option4')
            except:
                print("Can't Delete Approved Event")
                return redirect('/option/option4')
        return redirect(url_for('dashboard'))
    return redirect(url_for('index'))

@app.route('/deny_event/<int:id>', methods=['POST', 'GET'])
def deny_event(id):
    if 'email' in session:
        current_user = Users.query.filter_by(email=session.get('email', "")).first()
        try:
            if current_user.type=="admin":
                target_event = Reservations.query.filter_by(id=id, status="pending").first()
                target_event.status = "denied"
                db.session.commit()
                return redirect('/option/option4')
        except:
            print("Can't Deny Approved Event")
            return redirect('/option/option4')
        return f"""
                        <script>
                            alert("Admin user can only do this task");
                            window.location.href='/dashboard';
                        </script>
                        """
    return redirect(url_for('index'))

@app.route('/approve_event/<int:id>', methods=['POST', 'GET'])
def approve_event(id):
    if 'email' in session:
        current_user = Users.query.filter_by(email=session.get('email', "")).first()
        try:
            if current_user.type=="admin":
                target_event = Reservations.query.filter_by(id=id, status="pending").first()
                target_event.status = "approved"
                db.session.commit()
                return redirect('/option/option4')
        except:
            return redirect('/option/option4')
        return f"""
                        <script>
                            alert("Admin user can only do this task");
                            window.location.href='/dashboard';
                        </script>
                        """
    return redirect(url_for('index'))

@app.route('/delete_holiday/<int:id>', methods=['POST', 'GET'])
def delete_holiday(id):
    if 'email' in session:
        current_user = Users.query.filter_by(email=session.get('email', "")).first()
        if current_user.type=="admin":
            target_holiday = Holidays.query.filter_by(id=id).first()
            db.session.delete(target_holiday)
            db.session.commit()
            return redirect('/option/option3')
        return f"""
                        <script>
                            alert("Admin user can only do this task");
                            window.location.href='/dashboard';
                        </script>
                        """
    return redirect(url_for('index'))

@app.route('/delete_staff/<int:id>', methods=['POST', 'GET'])
def delete_staff(id):
    if 'email' in session:
        current_user = Users.query.filter_by(email=session.get('email', "")).first()
        if current_user.type=="admin":
            target_user = Users.query.filter_by(id=id, type="staff").first()
            db.session.delete(target_user)
            db.session.commit()
            return redirect('/option/option2')
        return f"""
                        <script>
                            alert("Admin user can only do this task");
                            window.location.href='/dashboard';
                        </script>
                        """
    return redirect(url_for('index'))

@app.route('/unlock_staff/<int:id>', methods=['POST', 'GET'])
def unlock_staff(id):
    if 'email' in session:
        current_user = Users.query.filter_by(email=session.get('email', "")).first()
        if current_user.type=="admin":
            target_user = Users.query.filter_by(id=id, status="locked", type="staff").first()
            target_user.status="active"
            db.session.commit()
            return redirect('/option/option2')
        return f"""
                        <script>
                            alert("Admin user can only do this task");
                            window.location.href='/dashboard';
                        </script>
                        """
    return redirect(url_for('index'))

@app.route('/lock_staff/<int:id>', methods=['POST', 'GET'])
def lock_staff(id):
    if 'email' in session:
        current_user = Users.query.filter_by(email=session.get('email', "")).first()
        if current_user.type=="admin":
            target_user = Users.query.filter_by(id=id, status="active", type="staff").first()
            target_user.status="locked"
            db.session.commit()
            return redirect('/option/option2')
        return f"""
                        <script>
                            alert("Admin user can only do this task");
                            window.location.href='/dashboard';
                        </script>
                        """
    return redirect(url_for('index'))


@app.route('/save_holiday', methods=['POST', 'GET'])
def save_holiday():
    if 'email' in session:
        current_user = Users.query.filter_by(email=session.get('email', "")).first()
        if str(current_user.type)=="admin":
            date, reason = request.form['date'], request.form['reason']
            reservation_obj = Reservations.query.filter_by(rdate=date).first()
            holidays_obj = Holidays.query.filter_by(date=date).first()
            if reservation_obj or holidays_obj:
                return f"""
                    <script>
                        alert("Can't book on reserved/holiday date");
                    </script>
                    """
            holiday_entry = Holidays(
                date=date,
                reason=reason,
                bdate=datetime.now()
            )

            db.session.add(holiday_entry)
            db.session.commit()
            return redirect('/option/option3')
        print(current_user)
        print(current_user.status)
        return f"""
                        <script>
                            alert("User added! the password is automatically set to: password");
                            window.location.href='/dashboard';
                        </script>
                        """
    return redirect(url_for('index'))

@app.route('/save_user', methods=['POST', 'GET'])
def save_user():
    if 'email' in session:
        current_user = Users.query.filter_by(email=session.get('email', "")).first()
        if str(current_user.type) == 'admin':
            name, address, email_address, phone_no = request.form['name'], request.form['address'], request.form['email_address'], request.form['phone_no']
            check_user = Users.query.filter_by(email=email_address).first()
            if check_user:
                return f"""
                        <script>
                            alert("This email address already registered and cannot be added! Choose Different Email Address");
                            window.location.href='/dashboard';
                        </script>
                        """


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
        return f"""
                        <script>
                            alert("User added! the password is automatically set to: password");
                            window.location.href='/dashboard';
                        </script>
                        """
    return redirect(url_for('index'))

@app.route('/save_booking_event', methods=['POST','GET'])
def save_booking_event():
    if 'email' in session:
        title, address, phone_no, email_address, reservation_date, reservation_time, no_people = request.form['title'], request.form['address'], request.form['phone_no'], request.form['email_address'], request.form['reservation_date'], request.form['reservation_time'], request.form['no_people']
        if datetime.strptime(reservation_date, '%Y-%m-%d') < datetime.now():
            flash("Please reserve ahead of current time")
            return redirect('/option/option1')
        users_obj = Users.query.filter_by(email=session.get('email', "")).first()
        reservation_obj = Reservations.query.filter_by(rdate=reservation_date).first()
        holidays_obj = Holidays.query.filter_by(date=reservation_date).first()
        if reservation_obj or holidays_obj:
            return f"""
                    <script>
                        alert("Can't book on reserved/holiday date");
                    </script>
                    """

        reservation_entry = Reservations(
            uid=users_obj.id,
            ucount=no_people,
            rdate=reservation_date,
            status='pending',
            comments='',
            bdate=datetime.now(),
            caddress=address,
            cphone_no=phone_no,
            cemail_address=email_address,
            rtime=reservation_time,
            title=title
        )

        db.session.add(reservation_entry)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return redirect(url_for('index'))

@app.route('/get_calendar/<int:year>/<int:month>', methods=['GET'])
def get_calendar(year, month):
    if 'email' in session:
        try:
            # Perform any necessary logic to generate calendar data for the specified year and month
            calendar_data = generate_calendar(year, month)

            holidays_all_obj = Holidays.query.all()
            
            # Extract the relevant information from holidays_all_obj and reservation_all_obj
            holidays = [{"date": holiday.date, "reason": holiday.reason} for holiday in holidays_all_obj]


            user_alias = aliased(Users)
            reservations_with_names = db.session.query(Reservations, user_alias.name).join(user_alias, Reservations.uid == user_alias.id).filter(Reservations.status == "approved").all()
            # Now, you can create a list of reservations with user names
            reservations = [{"date": reservation.rdate, "title": reservation.title} for reservation, user_name in reservations_with_names]

            # Combine holidays and reservations into a dictionary
            reservations_and_holidays = {
                "holidays": holidays,
                "reservations": reservations
            }

            # Format the calendar data as a JSON object
            formatted_data = {
                'month_name': calendar.month_name[month],
                'calendar': calendar_data,
                'events': reservations_and_holidays  # Include the combined data
            }
            
            # Return the formatted data as JSON
            return jsonify(formatted_data)

        except Exception as e:
            # Handle any errors that may occur during data retrieval
            return jsonify({'error': str(e)}), 500
    return redirect(url_for('index'))

@app.route('/option/<option>')
def option(option):
    if 'email' in session:
        # Calculate the current year and month
        current_user = Users.query.filter_by(email=session.get('email', "")).first()
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month
        current_month_data = display_calendar(current_year, current_month)

        #return the users as list of objects
        users_all_obj = Users.query.order_by(Users.id.desc()).all()

        #return the holidays as list of objects
        holidays_all_obj = Holidays.query.order_by(Holidays.id.desc()).all()
        

        #return the events reserved as list of objects
        reservations_all_obj = Reservations.query.order_by(Reservations.id.desc()).all()
        events_and_user_combined = []
        for i in reservations_all_obj:
            user_obj = Users.query.filter_by(id=i.uid).first()
            if user_obj:
                combined_data = {
                'id': i.id,
                'name': user_obj.name,
                'email': user_obj.email,
                'phone': user_obj.phone,
                'rdate': datetime.strptime(i.rdate, '%Y-%m-%d').strftime('%B %d, %Y'),
                'bdate': datetime.strptime(i.bdate, '%Y-%m-%d %H:%M:%S.%f').strftime('%B %d, %Y, %I:%M:%S %p'),
                'rtime': datetime.strptime(i.rtime, '%H:%M').strftime('%I:%M %p'),
                'ucount': i.ucount,
                'status': i.status,
                'title': i.title
                 }
                events_and_user_combined.append(combined_data)

        return render_template('dashboard.html',
                              selected_option=option,
                              current_month_data=current_month_data,
                              users_all_obj=users_all_obj,
                              holidays_all_obj=holidays_all_obj,
                              reservations_all_obj=reservations_all_obj,
                              events_and_user_combined=events_and_user_combined,
                              current_user=current_user)
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'email' in session:
        
        return render_template('dashboard.html')
    return redirect(url_for('index'))

@app.route('/authenticate', methods=['POST', 'GET'])
def authenticate():
    try:
        email, password = request.form.get('email'), request.form.get('password')
        current_user = Users.query.filter_by(email=email).first()
        if current_user.type=="staff" and current_user.status=="locked":
            return f"""
                    <script>
                        alert("Can't Login, The account is LOCKED");
                    </script>
                    """
        
        if Users.login_is_true(email, password):
            session['email'] = email
            
            return redirect(url_for('dashboard'))
        return f"""
                    <script>
                        alert("Can't Login, Username and Password doesn't match");
                        window.location.href='/';
                    </script>
                    """
    except:
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