from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'  # Replace with a secure key in real projects

# Initialize the database
def init_db():
    conn = sqlite3.connect('intel.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS intel (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

init_db()

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Anonymous Submission Page
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        content = request.form['intel']
        conn = sqlite3.connect('intel.db')
        c = conn.cursor()
        c.execute('INSERT INTO intel (content) VALUES (?)', (content,))
        conn.commit()
        conn.close()
        return redirect('/')  # redirect to home after submission
    return render_template('submit.html')

# Admin Login Page
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'youradminpass':  # Replace with your real password
            session['admin'] = True
            return redirect('/intel')
        else:
            return render_template('admin.html', error='Wrong password')
    return render_template('admin.html')

# Protected Intel View
@app.route('/intel')
def intel():
    if not session.get('admin'):
        return redirect('/')
    conn = sqlite3.connect('intel.db')
    c = conn.cursor()
    c.execute('SELECT content, timestamp FROM intel ORDER BY timestamp DESC')
    posts = c.fetchall()
    conn.close()
    return render_template('intel.html', posts=posts)

# Optional: Logout Route
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')
    
if __name__ == '__main__':
    app.run(debug=True)
