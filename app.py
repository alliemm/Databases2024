#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors
import datetime
from functools import wraps
import random

#Initialize the app from Flask
app = Flask(__name__)
app.secret_key = 'my-secret_key'

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='project',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session['user_type'] != 'staff':
            flash('Please login as airline staff', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def customer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session['user_type'] != 'customer':
            flash('Please login as customer', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/customer')
def login_customer():
    return render_template('login_customer.html')

@app.route('/login/staff')
def login_staff():
    return render_template('login_staff.html')

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register/customer')
def register_customer():
    return render_template('register_customer.html')

@app.route('/register/staff')
def register_staff():
    return render_template('register_staff.html')

@app.route('/register/customer/auth', methods=['POST'])
def register_customer_auth():
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    building_number = request.form['building_number']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone_number = request.form['phone_number']
    passport_number = request.form['passport_number']
    passport_expiration = request.form['passport_expiration']
    passport_country = request.form['passport_country']
    date_of_birth = request.form['date_of_birth']

    cursor = conn.cursor()

    try:
        # Check if customer already exists
        query = 'SELECT * FROM customer WHERE email = %s'
        cursor.execute(query, (email,))
        data = cursor.fetchone()

        if data:
            flash('This email is already registered', 'error')
            return redirect(url_for('register_customer'))

        # Insert new customer
        ins = 'INSERT INTO customer VALUES(%s, %s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (email, name, password, building_number, street, city,
                             state, phone_number, passport_number, passport_expiration,
                             passport_country, date_of_birth))
        conn.commit()
        flash('Registration successful! Please login', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        flash('An error occurred during registration', 'error')
        return redirect(url_for('register_customer'))
    finally:
        cursor.close()

@app.route('/register/staff/auth', methods=['POST'])
def register_staff_auth():
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    airline_name = request.form['airline_name']
    phone_numbers = request.form.getlist('phone_numbers[]')
    emails = request.form.getlist('emails[]')

    cursor = conn.cursor()

    try:
        # First check if the airline exists
        airline_query = 'SELECT * FROM airline WHERE name = %s'
        cursor.execute(airline_query, (airline_name,))
        airline_data = cursor.fetchone()
        
        if not airline_data:
            flash('This airline does not exist in our system', 'error')
            return redirect(url_for('register_staff'))

        # Check if staff already exists
        query = 'SELECT * FROM airline_staff WHERE username = %s'
        cursor.execute(query, (username,))
        data = cursor.fetchone()

        if data:
            flash('This username is already taken', 'error')
            return redirect(url_for('register_staff'))

        # Insert new staff member
        ins = 'INSERT INTO airline_staff VALUES(%s, md5(%s), %s, %s, %s, %s)'
        cursor.execute(ins, (username, password, first_name, last_name,
                             date_of_birth, airline_name))
        
        # Insert phone numbers
        for phone_number in phone_numbers:
            if phone_number:  # Only insert non-empty phone numbers
                phone_ins = 'INSERT INTO staff_phone VALUES(%s, %s)'
                cursor.execute(phone_ins, (username, phone_number))
        
        # Insert email addresses
        for email in emails:
            if email:  # Only insert non-empty emails
                email_ins = 'INSERT INTO airline_email VALUES(%s, %s)'
                cursor.execute(email_ins, (username, email))
        
        conn.commit()
        flash('Staff registration successful! Please login', 'success')
        return redirect(url_for('login'))
    except Exception as e:
        flash('An error occurred during registration', 'error')
        return redirect(url_for('register_staff'))
    finally:
        cursor.close()

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['user_type'] == 'customer':
        cursor = conn.cursor()
        # Query all flights the customer has purchased tickets for
        query = '''
            SELECT f.*, t.ticket_ID
            FROM purchase p
            JOIN ticket t ON p.ticket_ID = t.ticket_ID
            JOIN flight f ON t.airline_name = f.airline_name AND t.flight_number = f.flight_number AND t.departure_datetime = f.departure_datetime
            WHERE p.email = %s
            ORDER BY f.departure_datetime DESC
        '''
        cursor.execute(query, (session['username'],))
        my_flights = cursor.fetchall()
        cursor.close()
        return render_template('customer_dashboard.html', my_flights=my_flights)
    else:
        cursor = conn.cursor()
        airline_name = session['airline_name']
        # Get flights for next 30 days
        today = datetime.datetime.now().date()
        end_date = today + datetime.timedelta(days=30)
        query = '''
            SELECT flight_number, departure_datetime, arrival_datetime, 
                   departure_airport_code, arrival_airport_code, status
            FROM flight 
            WHERE airline_name = %s 
            AND DATE(departure_datetime) BETWEEN %s AND %s
            ORDER BY departure_datetime ASC
        '''
        cursor.execute(query, (airline_name, today, end_date))
        flights = cursor.fetchall()
        cursor.close()
        return render_template('staff_dashboard.html', flights=flights)
@app.route('/cancel_trip')
@customer_required
def cancel_trip():
    ticket_id = request.args.get('ticket_id')
    return render_template('cancel_trip.html', ticket_id=ticket_id)
@app.route('/cancel_trip/confirm', methods=['POST'])
@customer_required
def confirm_cancel_trip():
    ticket_id = request.form['ticket_id']
    cursor = conn.cursor()
    try:
        # Deletes the purchase record
        delete_query = 'DELETE FROM purchase WHERE ticket_ID = %s AND email = %s'
        cursor.execute(delete_query, (ticket_id, session['username']))
        conn.commit()
        flash('Trip cancelled successfully', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error cancelling trip: {e}', 'success')
    finally:
        cursor.close()
    return redirect(url_for('dashboard'))
@app.route('/review_flight')
@customer_required
def review_flight():
    ticket_id = request.args.get('ticket_id')
    cursor = conn.cursor()
    try:
        query = '''
            SELECT t.ticket_ID, t.flight_number, t.airline_name, t.departure_datetime
            FROM ticket t
            JOIN purchase p ON t.ticket_ID = p.ticket_ID
            WHERE t.ticket_ID = %s AND p.email = %s
        '''
        cursor.execute(query, (ticket_id, session['username']))
        ticket = cursor.fetchone()
        if not ticket:
            flash("Ticket not found or unauthorized access", "error")
            return redirect(url_for('dashboard'))
        return render_template('review_flight.html', ticket=ticket)
    finally:
        cursor.close()
@app.route('/submit_review', methods=['POST'])
@customer_required
def submit_review():
    email = session['username']
    airline_name = request.form['airline_name']
    flight_number = request.form['flight_number']
    departure_datetime = request.form['departure_datetime']
    review = request.form['review']
    comment = request.form['comment']
    cursor = conn.cursor()
    try:
        insert_query = 'INSERT INTO review (email, airline_name, flight_number, departure_datetime, review, comment) VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.execute(insert_query, (email, airline_name, flight_number, departure_datetime, review, comment))
        conn.commit()
        flash('Thank you for your feedback!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error submitting review: {e}', 'error')
    finally:
        cursor.close()
    return redirect(url_for('dashboard'))
@app.route('/login/customer/auth', methods=['POST'])
def login_customer_auth():
    email = request.form['email']
    password = request.form['password']

    cursor = conn.cursor()
    try:
        # Check if the email exists first
        check_query = 'SELECT * FROM customer WHERE email = %s'
        cursor.execute(check_query, (email,))
        user_exists = cursor.fetchone()
        
        if not user_exists:
            flash('No customer account found with this email', 'error')
            return redirect(url_for('login_customer'))
        
        # Try password match with MD5 hashing
        query = 'SELECT * FROM customer WHERE email = %s AND password = md5(%s)'
        cursor.execute(query, (email, password))
        data = cursor.fetchone()
        
        if not data:
            flash('Incorrect password', 'error')
            return redirect(url_for('login_customer'))

        # If we get here, login was successful
        session['username'] = email
        session['user_type'] = 'customer'
        session['name'] = data['name']
        
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))
            
    except Exception as e:
        flash('An error occurred during login. Please try again.', 'error')
        return redirect(url_for('login_customer'))
    finally:
        cursor.close()

@app.route('/login/staff/auth', methods=['POST'])
def login_staff_auth():
    username = request.form['username']
    password = request.form['password']

    cursor = conn.cursor()
    try:
        # Check if the username exists first
        check_query = 'SELECT * FROM airline_staff WHERE username = %s'
        cursor.execute(check_query, (username,))
        user_exists = cursor.fetchone()
        
        if not user_exists:
            flash('No staff account found with this username', 'error')
            return redirect(url_for('login_staff'))
        
        # Try password match with MD5 hashing
        query = 'SELECT * FROM airline_staff WHERE username = %s AND password = md5(%s)'
        cursor.execute(query, (username, password))
        data = cursor.fetchone()
        
        if not data:
            flash('Incorrect password', 'error')
            return redirect(url_for('login_staff'))

        # If we get here, login was successful
        session['username'] = username
        session['user_type'] = 'staff'
        session['first_name'] = data['first_name']
        session['last_name'] = data['last_name']
        session['airline_name'] = data['airline_name']
        
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))
            
    except Exception as e:
        flash('An error occurred during login. Please try again.', 'error')
        return redirect(url_for('login_staff'))
    finally:
        cursor.close()

@app.route('/staff/view_reports')
@staff_required
def staff_view_reports():
    cursor = conn.cursor()
    airline_name = session['airline_name']
    query = '''
    SELECT f.flight_number, COUNT(p.ticket_ID) AS tickets_sold, 
               SUM(p.sold_price) AS total_revenue
        FROM flight f
        LEFT JOIN ticket t ON f.flight_number = t.flight_number AND f.airline_name = t.airline_name
        LEFT JOIN purchase p ON t.ticket_ID = p.ticket_ID
        WHERE f.airline_name = %s
        GROUP BY f.flight_number
    '''
    cursor.execute(query, (airline_name,))
    report_data = cursor.fetchall()
    cursor.close()
    return render_template('staff_view_reports.html', reports=report_data)
@app.route('/staff/view_reviews')
@staff_required
def staff_view_reviews():
    cursor = conn.cursor()
    airline_name = session['airline_name']
    query = '''
        SELECT flight_number, departure_datetime, 
               ROUND(AVG(review), 2) AS avg_review, COUNT(*) AS num_reviews
        FROM review
        WHERE airline_name = %s
        GROUP BY flight_number, departure_datetime
        ORDER BY departure_datetime DESC
    '''
    cursor.execute(query, (airline_name,))
    reviews_data = cursor.fetchall()
    cursor.close()
    return render_template('staff_view_reviews.html', reviews=reviews_data)

@app.route('/search_flights', methods=['GET', 'POST'])
def search_flights():
    if request.method == 'GET':
        return render_template('search_flights.html')
        
    source = request.form['source']
    destination = request.form['destination']
    departure_date = request.form['departure_date']
    trip_type = request.form['trip_type']
    return_date = request.form.get('return_date')

    cursor = conn.cursor()
    
    # Get current datetime for future flight validation
    current_datetime = datetime.datetime.now()
    
    # Search for outbound flights
    outbound_query = '''
    SELECT flight_number, airline_name, departure_datetime, arrival_datetime,
           departure_airport_code, arrival_airport_code, base_price, status, airplane_ID 
    FROM flight
    WHERE departure_airport_code = %s 
    AND arrival_airport_code = %s 
    AND DATE(departure_datetime) = %s
    '''
    cursor.execute(outbound_query, (source, destination, departure_date))
    outbound_flights = cursor.fetchall()

    # Convert datetime strings to datetime objects if needed
    for flight in outbound_flights:
        try:
            flight['departure_datetime'].strftime('%Y-%m-%d %H:%M:%S')
        except (AttributeError, TypeError):
            flight['departure_datetime'] = datetime.datetime.strptime(str(flight['departure_datetime']), '%Y-%m-%d %H:%M:%S')
            
        try:
            flight['arrival_datetime'].strftime('%Y-%m-%d %H:%M:%S')
        except (AttributeError, TypeError):
            flight['arrival_datetime'] = datetime.datetime.strptime(str(flight['arrival_datetime']), '%Y-%m-%d %H:%M:%S')

    # Search for return flights if round trip
    return_flights = []
    if trip_type == 'round_trip' and return_date:
        return_query = '''
        SELECT flight_number, airline_name, departure_datetime, arrival_datetime,
               departure_airport_code, arrival_airport_code, base_price, status, airplane_ID 
        FROM flight
        WHERE departure_airport_code = %s 
        AND arrival_airport_code = %s 
        AND DATE(arrival_datetime) = %s
        AND DATE(departure_datetime) >= DATE(%s)
        ORDER BY departure_datetime ASC
        '''
        cursor.execute(return_query, (destination, source, return_date, departure_date))
        return_flights = cursor.fetchall()
        
        # Convert datetime strings to datetime objects if needed
        for flight in return_flights:
            try:
                flight['departure_datetime'].strftime('%Y-%m-%d %H:%M:%S')
            except (AttributeError, TypeError):
                flight['departure_datetime'] = datetime.datetime.strptime(str(flight['departure_datetime']), '%Y-%m-%d %H:%M:%S')
                
            try:
                flight['arrival_datetime'].strftime('%Y-%m-%d %H:%M:%S')
            except (AttributeError, TypeError):
                flight['arrival_datetime'] = datetime.datetime.strptime(str(flight['arrival_datetime']), '%Y-%m-%d %H:%M:%S')

    cursor.close()

    return render_template('search_results.html', 
                         outbound_flights=outbound_flights,
                         return_flights=return_flights,
                         trip_type=trip_type)
@app.route('/staff/view_comments')
@staff_required
def view_comments():
    airline_name = session['airline_name']
    cursor = conn.cursor()
    try:
        query = '''
            SELECT flight_number, departure_datetime, review, comment
            FROM review
            WHERE airline_name = %s
            ORDER BY departure_datetime DESC
        '''
        cursor.execute(query, (airline_name,))
        comments = cursor.fetchall()
        return render_template('view_comments.html', rows=comments)
    finally:
        cursor.close()

@app.route('/add_airplane', methods=['GET', 'POST'])
@staff_required
def add_airplane():
    if request.method == 'POST':
        try:
            airline_name = session.get('airline_name')
            airplane_id = request.form['airplane_id']
            num_seats = request.form['num_seats']
            manufacturing_company = request.form['manufacturing_company']
            
            cursor = conn.cursor()
            try:
                # Check if airplane already exists
                query = 'SELECT * FROM airplane WHERE airline_name = %s AND airplane_ID = %s'
                cursor.execute(query, (airline_name, airplane_id))
                if cursor.fetchone():
                    flash('An airplane with this ID already exists', 'error')
                    return redirect(url_for('add_airplane'))
                    
                # Add new airplane
                query = 'INSERT INTO airplane (airline_name, airplane_ID, num_seats, manufacturing_company) VALUES(%s, %s, %s, %s)'
                cursor.execute(query, (airline_name, airplane_id, num_seats, manufacturing_company))
                conn.commit()
                flash('Airplane added successfully', 'success')
                return redirect(url_for('staff_view_flights'))
                
            except Exception as e:
                flash(f'Error adding airplane: {str(e)}', 'error')
                return redirect(url_for('add_airplane'))
            finally:
                cursor.close()
        except KeyError as e:
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('add_airplane'))
            
    # GET request - show the form
    return render_template('add_airplane.html')

@app.route('/staff/view_flights', methods=['GET', 'POST'])
@staff_required
def staff_view_flights():
    cursor = conn.cursor()
    airline_name = session['airline_name']
    
    # Get current date and default end date (30 days from now)
    today = datetime.datetime.now().date()
    default_end_date = today + datetime.timedelta(days=30)
    
    # Set default dates or get from form
    if request.method == 'POST':
        try:
            start_date = datetime.datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        except (ValueError, TypeError):
            # If dates are invalid, use defaults
            start_date = today
            end_date = default_end_date
    else:
        # For GET requests, show next 30 days by default
        start_date = today
        end_date = default_end_date
    
    # Base query
    query = '''
        SELECT flight_number, departure_datetime, arrival_datetime, 
               departure_airport_code, arrival_airport_code, status, 
               airplane_ID, base_price
        FROM flight 
        WHERE airline_name = %s 
        AND DATE(departure_datetime) BETWEEN %s AND %s
        AND (departure_airport_code = %s OR %s IS NULL)
        AND (arrival_airport_code = %s OR %s IS NULL)
        ORDER BY departure_datetime ASC
    '''

    # If no airport filter is selected, pass NULL
    source_airport = request.form.get('source_airport', '') if request.method == 'POST' else None
    destination_airport = request.form.get('destination_airport', '') if request.method == 'POST' else None

    # Execute query
    cursor.execute(query, (
        airline_name, 
        start_date, 
        end_date,
        source_airport or None,
        source_airport or None,
        destination_airport or None,
        destination_airport or None
    ))
    flights = cursor.fetchall()
    
    # Get all airports for the filter dropdowns
    query = 'SELECT DISTINCT code, city FROM airport ORDER BY code'
    cursor.execute(query)
    airports = cursor.fetchall()
    
    cursor.close()
    
    # Format dates for the form
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    return render_template('staff_view_flights.html', 
                         flights=flights, 
                         airports=airports,
                         start_date=start_date_str,
                         end_date=end_date_str,
                         source_airport=source_airport,
                         destination_airport=destination_airport)

@app.route('/staff/flight_customers/<flight_number>')
@staff_required
def staff_flight_customers(flight_number):
    cursor = conn.cursor()
    airline_name = session['airline_name']
    
    # Verify the flight belongs to the staff's airline
    query = 'SELECT * FROM flight WHERE airline_name = %s AND flight_number = %s'
    cursor.execute(query, (airline_name, flight_number))
    flight = cursor.fetchone()
    
    if not flight:
        flash('Flight not found or unauthorized', 'error')
        return redirect(url_for('staff_view_flights'))
    
    # Get customers on this flight
    query = '''
        SELECT c.name, c.email, t.ticket_ID, p.sold_price
        FROM ticket t
        JOIN purchase p ON t.ticket_ID = p.ticket_ID
        JOIN customer c ON p.email = c.email
        WHERE t.flight_number = %s AND t.airline_name = %s
    '''
    cursor.execute(query, (flight_number, airline_name))
    customers = cursor.fetchall()
    
    cursor.close()
    return render_template('staff_flight_customers.html', 
                         flight=flight, 
                         customers=customers)

@app.route('/staff/create_flight', methods=['GET', 'POST'])
@staff_required
def staff_create_flight():
    cursor = conn.cursor()
    airline_name = session['airline_name']

    if request.method == 'POST':
        try:
            # Get form data
            flight_number = request.form['flight_number']
            departure_airport = request.form['departure_airport']
            arrival_airport = request.form['arrival_airport']
            departure_datetime = request.form['departure_datetime']
            arrival_datetime = request.form['arrival_datetime']
            base_price = request.form['base_price']
            airplane_id = request.form['airplane_id']
            status = request.form['status']

            # Validate airports are different
            if departure_airport == arrival_airport:
                flash('Departure and arrival airports must be different', 'error')
                return redirect(url_for('staff_create_flight'))

            # Validate departure time is before arrival time
            departure_time = datetime.datetime.strptime(departure_datetime, '%Y-%m-%dT%H:%M')
            arrival_time = datetime.datetime.strptime(arrival_datetime, '%Y-%m-%dT%H:%M')
            if departure_time >= arrival_time:
                flash('Departure time must be before arrival time', 'error')
                return redirect(url_for('staff_create_flight'))

            # Check if flight number already exists for this airline
            query = 'SELECT * FROM flight WHERE airline_name = %s AND flight_number = %s'
            cursor.execute(query, (airline_name, flight_number))
            if cursor.fetchone():
                flash('A flight with this number already exists', 'error')
                return redirect(url_for('staff_create_flight'))

            # Check if airplane exists and belongs to the airline
            query = 'SELECT * FROM airplane WHERE airline_name = %s AND airplane_ID = %s'
            cursor.execute(query, (airline_name, airplane_id))
            if not cursor.fetchone():
                flash('Invalid airplane selection', 'error')
                return redirect(url_for('staff_create_flight'))

            # Check for airplane scheduling conflicts
            conflict_query = '''
                SELECT * FROM flight 
                WHERE airplane_ID = %s 
                AND (
                    (departure_datetime BETWEEN %s AND %s) OR
                    (arrival_datetime BETWEEN %s AND %s) OR
                    (%s BETWEEN departure_datetime AND arrival_datetime) OR
                    (%s BETWEEN departure_datetime AND arrival_datetime)
                )
            '''
            cursor.execute(conflict_query, (
                airplane_id,
                departure_datetime, arrival_datetime,
                departure_datetime, arrival_datetime,
                departure_datetime, arrival_datetime
            ))
            if cursor.fetchone():
                flash('This airplane is already scheduled for another flight during this time period', 'error')
                return redirect(url_for('staff_create_flight'))

            # Check if airports exist
            query = 'SELECT * FROM airport WHERE code = %s OR code = %s'
            cursor.execute(query, (departure_airport, arrival_airport))
            if len(cursor.fetchall()) != 2:
                flash('Invalid airport selection', 'error')
                return redirect(url_for('staff_create_flight'))

            # Insert new flight
            insert_query = '''
                INSERT INTO flight (airline_name, flight_number, departure_datetime, 
                                  arrival_datetime, departure_airport_code, 
                                  arrival_airport_code, base_price, status, airplane_ID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (airline_name, flight_number, departure_datetime,
                                        arrival_datetime, departure_airport, arrival_airport,
                                        base_price, status, airplane_id))
            conn.commit()
            flash('Flight created successfully', 'success')
            return redirect(url_for('staff_view_flights'))

        except Exception as e:
            flash('Error creating flight. Please try again.', 'error')
            return redirect(url_for('staff_create_flight'))

    # GET request - show the form
    try:
        # Get all airports
        query = 'SELECT code, city FROM airport'
        cursor.execute(query)
        airports = cursor.fetchall()

        # Get airline's airplanes
        query = 'SELECT airplane_ID, num_seats FROM airplane WHERE airline_name = %s'
        cursor.execute(query, (airline_name,))
        airplanes = cursor.fetchall()

        return render_template('create_flight.html', 
                             airports=airports,
                             airplanes=airplanes)
    except Exception as e:
        flash('Error loading form data: ' + str(e), 'error')
        return render_template('create_flight.html', 
                             airports=[], 
                             airplanes=[])
    finally:
        cursor.close()

@app.route('/staff/update_flight_status_page/<flight_number>')
@staff_required
def update_flight_status_page(flight_number):
    cursor = conn.cursor()
    airline_name = session['airline_name']
    
    # Verify the flight belongs to the staff's airline
    query = 'SELECT * FROM flight WHERE airline_name = %s AND flight_number = %s'
    cursor.execute(query, (airline_name, flight_number))
    flight = cursor.fetchone()
    
    if not flight:
        flash('Flight not found or unauthorized', 'error')
        return redirect(url_for('staff_view_flights'))
    
    cursor.close()
    return render_template('update_flight_status.html', flight=flight)

@app.route('/staff/update_flight_status', methods=['POST'])
@staff_required
def update_flight_status():
    try:
        flight_number = request.form['flight_number']
        new_status = request.form['status']
        airline_name = session['airline_name']
        
        cursor = conn.cursor()
        
        # Verify the flight belongs to the staff's airline
        query = 'SELECT * FROM flight WHERE airline_name = %s AND flight_number = %s'
        cursor.execute(query, (airline_name, flight_number))
        if not cursor.fetchone():
            flash('Flight not found or unauthorized', 'error')
            return redirect(url_for('staff_view_flights'))
        
        # Update the flight status
        query = 'UPDATE flight SET status = %s WHERE airline_name = %s AND flight_number = %s'
        cursor.execute(query, (new_status, airline_name, flight_number))
        conn.commit()
        
        flash(f'Flight status updated to {new_status}', 'success')
        return redirect(url_for('staff_view_flights'))
        
    except Exception as e:
        flash('Error updating flight status: ' + str(e), 'error')
        return redirect(url_for('staff_view_flights'))
    finally:
        cursor.close()

@app.route('/purchase_ticket', methods=['GET', 'POST'])
@customer_required
def purchase_ticket():
    if request.method == 'POST':
        flight_number = request.form['flight_number']
        airline_name = request.form['airline_name']
    else:
        flight_number = request.args.get('flight_number')
        airline_name = request.args.get('airline_name')
    
    cursor = conn.cursor()
    try:
        # Get flight details
        query = 'SELECT * FROM flight WHERE flight_number = %s AND airline_name = %s'
        cursor.execute(query, (flight_number, airline_name))
        flight = cursor.fetchone()
        
        if not flight:
            flash('Flight not found', 'error')
            return redirect(url_for('search_flights'))
            
        return render_template('purchase_ticket.html', flight=flight)
    finally:
        cursor.close()

def generate_ticket_id():
    return random.randint(1, 999999)

def calculate_ticket_price(base_price, total_seats, sold_tickets):
    capacity_percentage = (sold_tickets / total_seats) * 100
    if capacity_percentage >= 60:
        return base_price * 1.20  # Add 20% if 60% or more capacity is filled
    return base_price

@app.route('/process_purchase', methods=['POST'])
@customer_required
def process_purchase():
    flight_number = request.form['flight_number']
    airline_name = request.form['airline_name']
    card_number = request.form['card_number']
    card_name = request.form['card_name']
    expiry_date = request.form['expiry_date']
    card_type = request.form['card_type']
    
    cursor = conn.cursor()
    try:
        # Get flight details
        query = 'SELECT * FROM flight WHERE flight_number = %s AND airline_name = %s'
        cursor.execute(query, (flight_number, airline_name))
        flight = cursor.fetchone()
        
        if not flight:
            flash('Flight not found', 'error')
            return redirect(url_for('dashboard'))
            
        # Get airplane capacity
        query = 'SELECT num_seats FROM airplane WHERE airplane_ID = %s'
        cursor.execute(query, (flight['airplane_ID'],))
        airplane = cursor.fetchone()
        if not airplane:
            flash('Airplane information not found', 'error')
            return redirect(url_for('dashboard'))
        total_seats = airplane['num_seats']
        
        # Get number of tickets already sold for this flight
        query = 'SELECT COUNT(*) as sold FROM ticket WHERE flight_number = %s AND airline_name = %s'
        cursor.execute(query, (flight_number, airline_name))
        result = cursor.fetchone()
        sold_tickets = result['sold'] if result else 0
        
        if sold_tickets + 1 > total_seats:
            flash('No seats available', 'error')
            return redirect(url_for('dashboard'))
            
        # Calculate price based on capacity
        ticket_price = calculate_ticket_price(flight['base_price'], total_seats, sold_tickets)
        
        # Generate unique ticket ID
        while True:
            ticket_id = generate_ticket_id()
            # Check if this ID already exists
            query = 'SELECT ticket_ID FROM ticket WHERE ticket_ID = %s'
            cursor.execute(query, (ticket_id,))
            if not cursor.fetchone():
                break
                
        # Insert into ticket
        query = '''
            INSERT INTO ticket (ticket_ID, airline_name, flight_number, departure_datetime)
            VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(query, (
            ticket_id,
            airline_name,
            flight_number,
            flight['departure_datetime']
        ))
        
        # Insert into purchase
        query = '''
            INSERT INTO purchase (ticket_ID, email, card_type, card_number, card_name, card_expiry, purchase_datetime, sold_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(query, (
            ticket_id,
            session['username'],
            card_type,
            card_number,
            card_name,
            expiry_date,
            datetime.datetime.now(),
            ticket_price
        ))
        
        conn.commit()
        flash(f'Successfully purchased ticket at ${ticket_price:.2f}!', 'success')
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        conn.rollback()
        print(f"Error during purchase: {str(e)}")
        flash(f'An error occurred during purchase: {str(e)}', 'error')
        return redirect(url_for('dashboard'))
    finally:
        cursor.close()

@app.route('/add_airport', methods=['GET', 'POST'])
@staff_required
def add_airport():
    if request.method == 'POST':
        try:
            code = request.form['code']
            name = request.form['name']
            city = request.form['city']
            country = request.form['country']
            
            cursor = conn.cursor()
            try:
                # Check if airport already exists
                query = 'SELECT * FROM airport WHERE code = %s'
                cursor.execute(query, (code,))
                if cursor.fetchone():
                    flash('An airport with this code already exists', 'error')
                    return redirect(url_for('add_airport'))
                    
                # Add new airport
                query = 'INSERT INTO airport (code, name, city, country) VALUES(%s, %s, %s, %s)'
                cursor.execute(query, (code, name, city, country))
                conn.commit()
                flash('Airport added successfully', 'success')
                return redirect(url_for('staff_view_flights'))
                
            except Exception as e:
                flash(f'Error adding airport: {str(e)}', 'error')
                return redirect(url_for('add_airport'))
            finally:
                cursor.close()
        except KeyError as e:
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('add_airport'))
            
    # GET request - show the form
    return render_template('add_airport.html')

#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)

# This is a test comment