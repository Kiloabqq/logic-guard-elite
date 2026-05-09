from flask import Flask, jsonify, request
import base64

app = Flask(__name__)

# The keys you found in the config
VALID_API_KEY = "9cebbce5-a47b-4396-9538-28eb1f9d0412"
VALID_SECRET_KEY = "tmvtJoc+3YrVB7h+i6plk8PRelqYn37bNRdw"

# Mock database
users_data = {
    "100": {"name": "Neo", "role": "User", "secret": "Public SDK Config"},
    "101": {"name": "Admin_Kilo", "role": "Admin", "secret": "HACKATHON_FLAG{FULL_CREDENTIAL_HIJACK_2026}"}
}

@app.route('/')
def home():
    return "Secure V3 API - Target: /api/v1/user/<id> (Requires Basic Auth)"

@app.route('/api/v1/user/<user_id>', methods=['GET'])
def get_user(user_id):
    # AUTH CHECK: Require Basic Auth with Key + Secret
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header.startswith('Basic '):
        return jsonify({"error": "Unauthorized. Basic Auth Required."}), 401

    try:
        decoded = base64.b64decode(auth_header.replace('Basic ', '')).decode('utf-8')
        user_part, pass_part = decoded.split(':')
        
        if user_part != VALID_API_KEY or pass_part != VALID_SECRET_KEY:
             return jsonify({"error": "Unauthorized. Invalid Credentials."}), 401
    except:
        return jsonify({"error": "Invalid Auth Format."}), 401

    # IDOR VULNERABILITY: No check to see if the requester owns this ID!
    if user_id in users_data:
        return jsonify(users_data[user_id])
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    print("LOGIC GUARD LAB (v3 Secure): Starting at http://127.0.0.1:5000")
    print(f"Required Key: {VALID_API_KEY}")
    print(f"Required Secret: {VALID_SECRET_KEY}")
    app.run(port=5000)
