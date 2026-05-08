import re
import os
from logic_guard.core.logger import logger

def extract_api_data_from_memory(filepath):
    """
    Scans a memory image for JWTs and API endpoints.
    A key requirement for the SIFT hackathon.
    """
    if not os.path.exists(filepath):
        logger.error(f"[X] Memory file not found: {filepath}")
        return None

    logger.info(f"[*] Analyzing Memory Image: {os.path.basename(filepath)}...")
    
    # Patterns
    jwt_pattern = re.compile(rb'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+')
    url_pattern = re.compile(rb'https?://[A-Za-z0-9.-]+(?:/api/v[0-9]+|/graphql)[A-Za-z0-9/._-]*')
    
    findings = {"tokens": [], "urls": []}
    
    try:
        # We read in chunks to handle large 3GB+ files without crashing RAM
        chunk_size = 1024 * 1024 * 10 # 10MB chunks
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                
                # Find JWTs
                for match in jwt_pattern.findall(chunk):
                    token = match.decode('utf-8', errors='ignore')
                    if token not in findings["tokens"]:
                        findings["tokens"].append(token)
                        logger.info(f"[+] Found JWT in Memory: {token[:20]}...")

                # Find API Endpoints
                for match in url_pattern.findall(chunk):
                    url = match.decode('utf-8', errors='ignore')
                    if url not in findings["urls"]:
                        findings["urls"].append(url)
                        logger.info(f"[+] Found API Endpoint in Memory: {url}")
                
                # Move back slightly to catch patterns split across chunks
                if f.tell() < os.path.getsize(filepath):
                    f.seek(f.tell() - 1024)

        return findings
    except Exception as e:
        logger.error(f"[X] Memory Analysis Error: {e}")
        return None
