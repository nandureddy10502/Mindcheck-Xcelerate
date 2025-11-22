from flask import Flask, render_template, request, redirect, url_for
import datetime
import csv
import os
import time
from pyngrok import ngrok # <--- ADD THIS

# --- Configuration ---
# 1. Initialize the Flask application
app = Flask(__name__) 

# Define the file path for your data storage
DATA_FILE = 'checkins.csv'

# --- ROUTES ---

# Function to generate a tip based on the average score
def generate_ai_tip(average):
    # SIMULATE AI processing time for authenticity
    time.sleep(1) 

    # ... rest of the tip logic remains the same ...

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
    total_score = 0
    num_entries = 0
    average_mood = "N/A" # Default value

    try:
        if os.path.exists(DATA_FILE) and os.stat(DATA_FILE).st_size > 0:
            with open(DATA_FILE, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None) # Skip the header row
                
                # Iterate and calculate average while collecting data for the table
                for row in reader:
                    data.append(row)
                    # Row[1] is the Mood Score (which is a string, so we convert to int)
                    score = int(row[1]) 
                    total_score += score
                    num_entries += 1
                
                # Calculate the average if there is data
                if num_entries > 0:
                    # Round the average to two decimal places for neat display
                    average_mood = round(total_score / num_entries, 2)
        
    except Exception as e:
        print(f"Error reading or calculating data: {e}")
        
    # Pass BOTH the table data AND the calculated average to the template
    return render_template('history.html', checkins=data, average_mood=average_mood)


# 4. Clear History Handler: Handles requests to delete the data
@app.route('/clear_history', methods=['POST'])
def clear_history():
    print("ATTEMPTING TO CLEAR HISTORY...")
    try:
        # Check if the file exists before trying to delete it
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            print(f"SUCCESS: {DATA_FILE} has been deleted.")
        else:
            print("INFO: Data file not found, nothing to delete.")
            
    except Exception as e:
        print(f"ERROR: Could not clear history: {e}") 
        
    # Redirect the user back to the empty history page
    return redirect(url_for('history'))


# --- RUN APPLICATION ---
# --- RUN APPLICATION ---
if __name__ == '__main__':
    # 1. Start ngrok tunnel on port 5000
    # This will fail if your token wasn't correctly saved!
    public_url = ngrok.connect(5000).public_url
    print(f"\n ********************************************************")
    print(f" * MindCheck Public URL: {public_url}")
    print(f" * SUBMIT THIS LINK FOR JUDGING: {public_url}")
    print(f" ********************************************************\n")

    # 2. Run Flask server (Important: use_reloader=False prevents Ngrok from duplicating)
    app.run(port=5000, debug=True, use_reloader=False)