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
    return "Admin Login Page"

# Create app route for reserve to avoid crashes for now.
@app.route("/reserve")
def reserve_seat():
    return "Reservation Page"

# Run the Flask app
if __name__ == "__main__":
    initialize_database()
    app.run(debug=True, host="0.0.0.0", port=5000)
