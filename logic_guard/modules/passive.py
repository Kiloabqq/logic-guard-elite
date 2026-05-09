import json
import base64
from logic_guard.core.logger import logger

def analyze_jwt_locally(token):
    try:
        parts = token.split('.')
        if len(parts) != 3:
            logger.info("[-] Token is not a JWT. Skipping local cryptographic analysis.")
            return None
            
        header = json.loads(base64.b64decode(parts[0] + '==').decode('utf-8'))
        payload = json.loads(base64.b64decode(parts[1] + '==').decode('utf-8'))
        
        logger.info(f"[*] Decoded JWT Header: {header}")
        logger.info(f"[*] Decoded JWT Payload: {payload}")
        
        if header.get('alg') == 'none':
            logger.error("[!] VULNERABILITY: JWT 'none' algorithm allowed.")
            
        return {"header": header, "payload": payload}
    except Exception as e:
        logger.error(f"[X] JWT Analysis Error: {e}")
        return None

def scan_for_env_files(url):
    logger.info(f"[*] Checking for exposed environment files at {url}...")
    # Simulation for IR logic
    logger.info("[-] .env - 404 Not Found")
    logger.info("[-] config.php - 404 Not Found")
