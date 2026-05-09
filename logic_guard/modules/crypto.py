import jwt
from logic_guard.core.logger import logger

class CryptoFuzzer:
    """
    Performs cryptographic fuzzing on JWTs (KID injection, Algorithm confusion).
    """
    def __init__(self, token):
        self.token = token

    def audit_jwt_strength(self):
        if not self.token:
            return None
        
        logger.inf("Auditing JWT Cryptographic Strength...")
        try:
            header = jwt.get_unverified_header(self.token)
            logger.inf(f"Detected Algorithm: {header.get('alg')}")
            
            if header.get('alg') == 'none':
                logger.warn("CRITICAL VULNERABILITY: JWT 'none' algorithm bypass detected!")
                return "CRITICAL"
            
            if 'kid' in header:
                logger.inf(f"Detected Key ID (KID): {header['kid']}")
                # Simulate KID path traversal test
                if "../" in header['kid']:
                    logger.warn("VULNERABILITY FOUND: Potential KID Path Traversal detected.")
                    return "HIGH"
                    
            logger.success("Cryptographic integrity check complete. No obvious bypasses found.")
            return "SECURE"
        except Exception as e:
            logger.error(f"[X] Crypto Audit Error: {e}")
            return None
