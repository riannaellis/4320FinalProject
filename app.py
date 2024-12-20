from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRECT_KEY"] = 'your secret key'
app.secret_key = 'your secret key'

# Create def to initialize the database
def initialize_database():
    connection = sqlite3.connect("database/reservations.db")
    with open("database/schema.sql", "r") as schema_file:
        connection.executescript(schema_file.read())
    connection.close()
    print("Database initialized successfully.")

# Create app route for index page (main page)
@app.route("/", methods=["GET", "POST"])
def index():

    # Create if statement to handle menu options
    if request.method == "POST":
        menu_option = request.form.get("menu-option")
        
        # Redirect to admin login
        if menu_option == "admin":
            return redirect(url_for("admin_login"))  
        
        # Redirect to reservation page
        elif menu_option == "reserve":
            return redirect(url_for("reserve_seat"))  
        
    # Render the main menu page
    return render_template("index.html")

# Create app route for admin-login to avoid crashes for now.
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']

        #Get admin credentials from database
        mydb = sqlite3.connect("database/reservations.db")
        mydb.row_factory = sqlite3.Row
        cursor = mydb.cursor()

        try:
            query = "SELECT * FROM admins WHERE username = ? AND password = ?;"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                return redirect(url_for('admin_dashboard'))
            else:
                flash(f"Username and/or password incorrect. Please try again.")
        except:
            flash(f"An error ocurred. Please try again.")

    return render_template('admin_login.html') 

'''
Function to generate cost matrix for flights
Input: none
Output: Returns a 12 x 4 matrix of prices
'''
def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix

# Create app route for admin dashboard
@app.route("/admin-dashboard")
def admin_dashboard():
    # Seat configuration
    rows = 12
    seats_per_row = 4
    
    # Initialize seating chart 
    seating_chart = [['O' for _ in range(seats_per_row)] for _ in range(rows)]
    
    # Get reserved seats from the database
    mydb = sqlite3.connect("database/reservations.db")
    mydb.row_factory = sqlite3.Row
    cursor = mydb.cursor()
    query = "SELECT seatRow, seatColumn FROM reservations;"
    cursor.execute(query)
    reserved_seats = cursor.fetchall()
    
    # Mark reserved seats as 'X'
    for seat in reserved_seats:
        seat_row = seat['seatRow']
        seat_column = seat['seatColumn']
        seating_chart[seat_row][seat_column] = 'X'

    # calculate total sales using the cost matrix
    cost_matrix = get_cost_matrix()  # Get the cost matrix
    total_sales = 0

    # calculate the total sales based on seat prices
    for seat in reserved_seats:
        seat_row = seat['seatRow']
        seat_column = seat['seatColumn']
        seat_price = cost_matrix[seat_row][seat_column]  # Get price from cost matrix
        total_sales += seat_price  # Add to total sales

    # Render the admin dashboard with seating chart and total sales
    return render_template(
        "admin_dashboard.html",
        seating_chart=seating_chart,
        rows=rows,
        seats_per_row=seats_per_row,
        total_sales=total_sales
    )


# Create app route for reserve
@app.route("/reserve", methods=["GET", "POST"])
def reserve_seat():

    #Initialize seating chart
    rows = 12
    seats_per_row = 4
    seating_chart = [['O' for _ in range(seats_per_row)] for _ in range(rows)]
   
    #Get seating chart data from database
    mydb = sqlite3.connect("database/reservations.db")
    mydb.row_factory = sqlite3.Row
    cursor = mydb.cursor()
    query = "SELECT seatRow, seatColumn FROM reservations;"
    cursor.execute(query)
    reserved_seats = [dict(row) for row in cursor.fetchall()]

    #Replace reserved seats with X
    for seat in reserved_seats:
        seat_row = seat['seatRow']
        seat_column = seat['seatColumn']
        seating_chart[seat_row][seat_column] = "X"

    if request.method == 'POST':
        # Get form data
        firstName = request.form['name']
        lastName = request.form['last_name']
        passengerName = firstName + lastName
        seatRow = int(request.form['row'])
        seatColumn = int(request.form['seat'])
        eTicketNumber = get_eTicketNumber(firstName)

        # Reserve seat if available
        if seating_chart[seatRow][seatColumn] == 'O':
            query = 'INSERT INTO reservations (passengerName, seatRow, seatColumn, eTicketNumber) VALUES (?, ?, ?, ?);'
            cursor.execute(query, (passengerName, seatRow, seatColumn, eTicketNumber))
            mydb.commit()
            flash(f"Congratuations {firstName} {lastName}! Row: {seatRow}, Seat: {seatColumn} is now reserved for you. Enjoy your trip!\nYour eticket number is: {eTicketNumber}")
        else:
            flash(f"Row: {seatRow}, Seat: {seatColumn} is already assigned. Choose again.")

        return redirect(url_for('reserve_seat'))

    return render_template('reserve_seat.html', seating_chart=seating_chart, rows=len(seating_chart), seats_per_row=seats_per_row)

#Function to get the eTicketNumber
def get_eTicketNumber(passengerName):
    course = "INFOTC4320"
    eTicketNumber = ""

    length_course = len(course)
    length_name = len(passengerName)

    min_length = 0
    if length_course >= length_name:
        min_length = length_name
    else:
        min_length = length_course
    
    for i in range(min_length):
        eTicketNumber += "".join(passengerName[i] + course[i])
    
    eTicketNumber += passengerName[min_length:] + course[min_length:]

    return eTicketNumber


# Run the Flask app
if __name__ == "__main__":
    initialize_database()
    app.run(debug=True, host="0.0.0.0", port=5004)
