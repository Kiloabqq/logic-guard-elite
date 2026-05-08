import requests
import time
from logic_guard.core.logger import logger

class StressAuditor:
    """
    Audits for missing rate limits and volumetric controls.
    Implements a 'Circuit Breaker' to survive 429 blocks.
    """
    def __init__(self, target, stealth=False):
        self.target = target
        self.stealth = stealth
        self.stop_event = False

    def run_volumetric_test(self, iterations=50):
        logger.info(f"[*] Starting Stress Audit on {self.target}...")
        
        if self.stealth:
            logger.info("[!] Stealth mode enabled: Reducing concurrency.")
            iterations = 10

        success_count = 0
        for i in range(iterations):
            try:
                # Simulating high-concurrency burst
                resp = requests.get(self.target, timeout=2)
                if resp.status_code == 429:
                    logger.warning("[!] CIRCUIT BREAKER: Rate limit hit (429). Pausing...")
                    time.sleep(5) # Backoff
                else:
                    success_count += 1
            except Exception:
                pass
        
        logger.info(f"[+] Stress Audit Complete: {success_count} requests processed.")
        return success_count
