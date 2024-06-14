from flask import Flask, render_template, request, redirect, url_for, session ,  send_file
import sqlite3
import anthropic
import os 

app = Flask(__name__)
app.secret_key = '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'

# Initialize Anthropics client
client = anthropic.Anthropic(api_key="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")

# SQLite database initialization
def get_db():
    db = getattr(session, '_database', None)
    if db is None:
        db = session._database = sqlite3.connect('database.db')
    return db

def close_db():
    db = getattr(session, '_database', None)
    if db is not None:
        db.close()

# Function to check if user is logged in
def logged_in():
    return 'username' in session

# Index route
@app.route('/')
def index():
     return render_template('index.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        if user:
            # Store user_id in session upon successful login
            session['id'] = user[0]  # Assuming user_id is the first column in the users table
            session['username'] = user[1]
            return redirect(url_for('protected'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

# Registration route

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phone_number = request.form['phone_number']  # Get phone number from the form
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (username, password, phone_number) VALUES (?, ?, ?)', (username, password, phone_number))
        db.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html')


# Protected route
@app.route('/dashboard')
def protected():
    if logged_in():
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/stacks', methods=["GET", "POST"])
def stacks():
    if logged_in():  # Check if the user is authenticated
        mood = None
        if request.method == "POST":
            message_content = request.form["message"]

            # Create a message using Anthropics API
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=100,
                temperature=0,
                system="Hey, can we figure out someone's emotions just by reading their messages? Tell me what mood they might be in and state the one answer mood i just need mood and nothing other else , with no explanation MOOD CAN ONLY BE HAPPY ,SAD,HOPE,ROMANTIC,NOSTALGIC,PEACEFUL",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": message_content
                            }
                        ]
                    }
                ]
            )

            # Extract the mood identified by Anthropics
            mood = response.content[0].text

            # Save the mood and user_id to the database
            db = get_db()
            cursor = db.cursor()
            user_id = session.get('id')
            if user_id is not None:
                cursor.execute("INSERT INTO moods (mood_name, user_id) VALUES (?, ?)", (mood, user_id))
                db.commit()
                return render_template("stacks.html", mood=mood)
            else:
                return "User ID not found in session. Please log in."
        return render_template("stacks.html", mood=mood)
    else:
        return redirect(url_for('login'))  # Redirect to login page if the user is not authenticated



@app.route('/add_genre', methods=['GET', 'POST'])
def add_genre():
    if logged_in():  # Check if the user is authenticated
        if request.method == 'POST':
            # Get id from the session 
            user_id = session.get('id')
            if user_id is not None:
                # Get genre_name from the form
                genre_name = request.form['genre_name']

                # Insert user_id and genre_name into the database
                cursor = get_db().cursor()
                cursor.execute("INSERT INTO genre (user_id, genre_name) VALUES (?, ?)", (user_id, genre_name))
                get_db().commit()

                return render_template('add_genre.html')
            else:
                return 'Session Expired. Please log in.'
        else:
            return render_template('add_genre.html')  # Create an HTML form to select genres
    else:
        return redirect(url_for('login'))  # Redirect to login page if the user is not authenticated

base_path = "home/ec2-user/"


@app.route('/play_audio')
def play_audio():
    user_id = session.get('id')
    if user_id is not None:
        user_folder_path = os.path.join(base_path, str(user_id))
        
        if not os.path.exists(user_folder_path):
            return "User folder not found."

        audio_files = [f for f in os.listdir(user_folder_path) if os.path.isfile(os.path.join(user_folder_path, f))]
        if audio_files:
            # Assume you want to play the first audio file found
            file_name = audio_files[0]
            s3_url = f"https://mfs-mcee.s3.eu-north-1.amazonaws.com/{file_name}"
            return render_template('dashboard.html', file_path=s3_url)
        else:
            return "No Mixes Generated"
    else:
        return "User not logged in"

if __name__ == '__main__':
    app.run(debug=False)




if __name__ == '__main__':

    app.run(debug=False)