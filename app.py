from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

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
@app.route("/admin-login")
def admin_login():
    if request.method == 'POST':
        # Here you can handle the login logic
        username = request.form['username']
        password = request.form['password']
        # For example, check if the username and password are correct
        if username == 'admin' and password == 'password':  # replace with actual login logic
            return redirect(url_for('dashboard'))  # Redirect to another page if login is successful
        else:
            return "Invalid username/password combination"

    return render_template('admin_login.html') 

# Initialize the seating chart (O = available, X = reserved)
rows = 10
seats_per_row = 5
seating_chart = [['O' for _ in range(seats_per_row)] for _ in range(rows)]

# Create app route for reserve to avoid crashes for now.
@app.route("/reserve")
def reserve_seat():
    global seating_chart
    message = None

    if request.method == 'POST':
        # Get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        row = int(request.form['row'])
        seat = int(request.form['seat'])

        # Reserve seat if available
        if seating_chart[row][seat] == 'O':
            seating_chart[row][seat] = 'X'
            message = f"Seat {seat} in row {row} reserved for {first_name} {last_name}."
        else:
            message = f"Seat {seat} in row {row} is already reserved."

    return render_template('reserve_seat.html', seating_chart=seating_chart, rows=len(seating_chart), message=message, seats_per_row=seats_per_row)

# Run the Flask app
if __name__ == "__main__":
    initialize_database()
    app.run(debug=True, host="0.0.0.0", port=5001)
