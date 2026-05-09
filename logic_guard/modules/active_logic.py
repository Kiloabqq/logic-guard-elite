import requests
import base64
from logic_guard.core.logger import logger

def assess_business_logic(url, token, user_id, secret=None):
    logger.inf(f"Auditing Business Logic for User ID: {user_id}")
    
    # Construct Headers
    request_headers = {}
    if token and secret:
        # Use Basic Auth for Key Pair
        auth_str = f"{token}:{secret}"
        encoded = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
        request_headers["Authorization"] = f"Basic {encoded}"
        logger.info("[*] Using Basic Authentication (Key Pair mode)")
    elif token:
        # Use Bearer for single token
        request_headers["Authorization"] = f"Bearer {token}"
        logger.info("[*] Using Bearer Authentication")
    
    # Real IDOR check
    target_id = int(user_id) + 1
    paths = ["/api/v1/user/", "/user/", "/profile/", "/api/v1/profile/"]
    
    found_any = False
    final_result = None

    for path in paths:
        target_url = f"{url.rstrip('/')}{path}{target_id}"
        logger.inf(f"[*] Testing IDOR on resource: {target_url}...")
        
        try:
            resp = requests.get(target_url, headers=request_headers, timeout=5)
            if resp.status_code == 200:
                logger.success(f"REAL VULNERABILITY FOUND: Insecure Direct Object Reference (IDOR)")
                logger.success(f"  [>] Resource: {target_url}")
                logger.success(f"  [>] Status: 200 OK (DATA LEAKAGE)")
                
                # Show the REAL data leaked
                snippet = resp.text[:300].replace('\n', ' ')
                logger.success(f"  [>] RAW LEAKAGE: {snippet}...")
                
                found_any = True
                final_result = {
                    "endpoint": target_url,
                    "method": "GET",
                    "vulnerability": "IDOR",
                    "severity": "High",
                    "leakage": snippet,
                    "description": f"Successfully leaked private data from {target_url}"
                }
                break
        except Exception as e:
            logger.error(f"Error checking {target_url}: {str(e)}")

    if not found_any:
        logger.info("[-] No active IDOR leakage confirmed on common user endpoints.")
        return None
        
    return final_result
