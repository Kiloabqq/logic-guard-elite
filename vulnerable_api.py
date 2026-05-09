from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock database
users_data = {
    "100": {"name": "Neo", "role": "User", "secret": "This is your public profile."},
    "101": {"name": "Admin_Kilo", "role": "Admin", "secret": "HACKATHON_FLAG{IDOR_SUCCESSFUL_2026}"}
}

@app.route('/')
def home():
    return "Vulnerable Lab API - Target: /api/v1/user/<id>"

@app.route('/api/v1/user/<user_id>', methods=['GET'])
def get_user(user_id):
    # IDOR VULNERABILITY: No check to see if the requester owns this ID!
    if user_id in users_data:
        return jsonify(users_data[user_id])
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    print("LOGIC GUARD LAB: Starting vulnerable API at http://127.0.0.1:5000")
    print("Test URL: http://127.0.0.1:5000/api/v1/user/101")
    app.run(port=5000)
