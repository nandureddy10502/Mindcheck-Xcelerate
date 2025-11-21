from flask import Flask, render_template, request, redirect, url_for
import datetime
import csv
import os

# --- Configuration ---
# 1. Initialize the Flask application
app = Flask(__name__) 

# Define the file path for your data storage
DATA_FILE = 'checkins.csv'

# --- ROUTES ---

# 1. Home Page Route: Handles GET requests to the root URL (/)
@app.route('/')
def index():
    # Renders the check-in form.
    return render_template('index.html')


# 2. Form Submission Handler: Handles POST requests from the form
@app.route('/submit_checkin', methods=['POST'])
def submit_checkin():
    # Get data from the HTML form
    mood = request.form['mood_score']
    note = request.form['quick_note']
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # The data we want to save
    data = [timestamp, mood, note]

    # Append data to the CSV file
    try:
        # Check if file exists to decide if we need to write the header
        write_header = not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0
        
        with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write header only if the file is new/empty
            if write_header:
                writer.writerow(['Timestamp', 'Mood Score', 'Note'])

            writer.writerow(data)
            
        print(f"--- DATA SAVED: {timestamp}, Score {mood} ---") 

    except Exception as e:
        print(f"Error saving data: {e}") 

    # Redirect the user back to the home page after submission
    return redirect(url_for('index'))


# 3. History Page Route: Handles GET requests to /history
@app.route('/history')
def history():
    data = []
    try:
        # Check if the file exists and has content before trying to read it
        if os.path.exists(DATA_FILE) and os.stat(DATA_FILE).st_size > 0:
            with open(DATA_FILE, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                # Skip the header row
                next(reader, None) 
                # Convert reader object to a list
                data = list(reader) 
        
    except Exception as e:
        print(f"Error reading data: {e}")
        
    # Pass the list of data to the history.html template
    return render_template('history.html', checkins=data)


# --- RUN APPLICATION ---
if __name__ == '__main__':
    # 'debug=True' auto-reloads changes and shows errors in the browser
    app.run(debug=True)