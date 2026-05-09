import requests
from logic_guard.core.logger import logger

class DiscoveryEngine:
    """
    Multithreaded reconnaissance for hidden API assets and configuration files.
    """
    def __init__(self, target):
        self.target = target
        self.common_paths = [
            "/.env", "/config.php", "/api/v1/health", 
            "/swagger.json", "/.git/config", "/actuator/env"
        ]

    def run_recon(self):
        logger.inf(f"Starting Discovery Scan on {self.target}...")
        findings = []
        
        for path in self.common_paths:
            url = f"{self.target.rstrip('/')}{path}"
            try:
                # Using a generic User-Agent for stealth
                headers = {"User-Agent": "Mozilla/5.0 (LogicGuard/1.0)"}
                resp = requests.get(url, headers=headers, timeout=3)
                
                if resp.status_code == 200:
                    logger.success(f"DISCOVERED: {url} (200 OK)")
                    findings.append(url)
                elif resp.status_code == 403:
                    logger.warn(f"FORBIDDEN: {url} (403) - Potential protected asset.")
            except Exception:
                pass
                
        return findings
