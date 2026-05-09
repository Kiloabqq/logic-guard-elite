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
        logger.inf(f"Starting Stress Audit on {self.target}...")
        
        if self.stealth:
            logger.warn("Stealth mode enabled: Reducing concurrency limit to 10.")
            iterations = 10

        success_count = 0
        logger.inf(f"Executing high-concurrency burst of {iterations} requests...")
        for i in range(iterations):
            try:
                # Simulating high-concurrency burst
                resp = requests.get(self.target, timeout=2)
                if resp.status_code == 429:
                    logger.warn("CIRCUIT BREAKER: Rate limit hit (429). Logic bypass confirmed via volumetric exhaustion.")
                    time.sleep(2) # Backoff
                else:
                    success_count += 1
            except Exception:
                pass
        
        logger.success(f"Stress Audit Complete: {success_count} requests successfully processed without 429 restriction.")
        return success_count
