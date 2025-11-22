from flask import Flask, render_template, request, redirect, url_for
import datetime
import csv
import os
import time
from pyngrok import ngrok


app = Flask(__name__) 


DATA_FILE = 'checkins.csv'




def generate_ai_tip(average):
    
    time.sleep(1) 

    
@app.route('/')
def index():
   
    return render_template('index.html')



@app.route('/submit_checkin', methods=['POST'])
def submit_checkin():
    
    mood = request.form['mood_score']
    note = request.form['quick_note']
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

   
    data = [timestamp, mood, note]

    
    try:
        
        write_header = not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0
        
        with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            
            if write_header:
                writer.writerow(['Timestamp', 'Mood Score', 'Note'])

            writer.writerow(data)
            
        print(f"--- DATA SAVED: {timestamp}, Score {mood} ---") 

    except Exception as e:
        print(f"Error saving data: {e}") 

    
    return redirect(url_for('index'))



@app.route('/history')
def history():
    data = []
    total_score = 0
    num_entries = 0
    average_mood = "N/A" 

    try:
        if os.path.exists(DATA_FILE) and os.stat(DATA_FILE).st_size > 0:
            with open(DATA_FILE, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None) 
                
                
                for row in reader:
                    data.append(row)
                    
                    score = int(row[1]) 
                    total_score += score
                    num_entries += 1
                
                
                if num_entries > 0:
                    
                    average_mood = round(total_score / num_entries, 2)
        
    except Exception as e:
        print(f"Error reading or calculating data: {e}")
        
    
    return render_template('history.html', checkins=data, average_mood=average_mood)



@app.route('/clear_history', methods=['POST'])
def clear_history():
    print("ATTEMPTING TO CLEAR HISTORY...")
    try:
        
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            print(f"SUCCESS: {DATA_FILE} has been deleted.")
        else:
            print("INFO: Data file not found, nothing to delete.")
            
    except Exception as e:
        print(f"ERROR: Could not clear history: {e}") 
        
    
    return redirect(url_for('history'))



if __name__ == '__main__':
    
    public_url = ngrok.connect(5000).public_url
    print(f"\n ********************************************************")
    print(f" * MindCheck Public URL: {public_url}")
    print(f" * SUBMIT THIS LINK FOR JUDGING: {public_url}")
    print(f" ********************************************************\n")

    
    app.run(port=5000, debug=True, use_reloader=False)