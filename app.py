from flask import Flask, render_template

# 1. Initialize the Flask application
# The variable 'app' is now your web application object
app = Flask(__name__)

# 2. Define the main route (Home Page)
# This function runs when a user visits the root URL (e.g., http://127.0.0.1:5000/)
@app.route('/')
def index():
    # Flask looks inside the 'templates' folder for this HTML file.
    return render_template('index.html')

# 3. Run the application
if __name__ == '__main__':
    # 'debug=True' is great for development as it auto-reloads changes
    app.run(debug=True)