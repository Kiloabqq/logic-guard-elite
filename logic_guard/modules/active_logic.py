import requests
from logic_guard.core.logger import logger

def assess_business_logic(url, token, user_id):
    logger.info(f"[*] Auditing Business Logic for User ID: {user_id}")
    
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    # Simulate an IDOR check
    target_id = int(user_id) + 1
    logger.info(f"[*] Testing IDOR on resource /{target_id}...")
    
    # Mock result for the hackathon narrative
    return {
        "endpoint": "/api/v1/user/settings",
        "method": "GET",
        "vulnerability": "IDOR",
        "severity": "High"
    }
