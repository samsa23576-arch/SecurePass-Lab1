from flask import Flask, request, jsonify
import sqlite3
import generate  # This imports your Part A!
import security  # This imports your Part B!

app = Flask(__name__)

# --- 1. SETUP SQLITE DATABASE ---
def init_db():
    # This automatically creates a file named 'passwords.db' in your folder
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    # Create a table to store our secure hashes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hashed_password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Run the database setup when the server starts
init_db()


# --- 2. REST API: GENERATE PASSWORD ---
# URL: http://127.0.0.1:5000/generate
@app.route('/generate', methods=['GET'])
def generate_api():
    # It looks for a ?length= number in the URL, defaults to 16 if not found
    length = request.args.get('length', default=16, type=int)
    
    # Call your generator from Part A
    new_password = generate.generate_password(length)
    
    return jsonify({
        "status": "success",
        "generated_password": new_password,
        "length": length
    })


# --- 3. REST API: VALIDATE & SAVE PASSWORD ---
# URL: http://127.0.0.1:5000/validate
@app.route('/validate', methods=['POST'])
def validate_api():
    # Get the JSON data sent to the server
    data = request.get_json()
    if not data or 'password' not in data:
        return jsonify({"error": "Please provide a 'password' in your JSON"}), 400
        
    user_password = data['password']
    
    # 1. Check your Policy rules (Part A)
    passed_policy, policy_errors = generate.check_policy(user_password)
    
    # 2. Check the HIBP API (Part B)
    is_breached = security.check_hibp(user_password)
    
    # 3. Generate the secure Bcrypt Hash (Part B)
    secure_hash = security.hash_password(user_password)
    
    # 4. Save the secure hash to our SQLite Database (Never save the plain text!)
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (hashed_password) VALUES (?)", (secure_hash,))
    conn.commit()
    conn.close()
    
    return jsonify({
        "password_tested": user_password,
        "policy_passed": passed_policy,
        "policy_errors": policy_errors,
        "is_breached": is_breached,
        "database_hash": secure_hash,
        "saved_to_database": True
    })

# --- START THE SERVER ---
if __name__ == '__main__':
    print("Starting SecurePass API Server...")
    app.run(debug=True, port=5000)