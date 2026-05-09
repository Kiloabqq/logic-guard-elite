import time
import os
from logic_guard.core.logger import logger
from logic_guard.core.validators import validate_url, validate_token
from logic_guard.agent.reporter import InvestigativeReporter

# Import our functional modules
from logic_guard.modules.passive import analyze_jwt_locally, scan_for_env_files
from logic_guard.modules.active_logic import assess_business_logic

class AgentOrchestrator:
    def __init__(self, target, token, userid, stealth, secret=None, memory_path=None, verbose=False):
        self.target = validate_url(target) if target else None
        self.token = validate_token(token) if token else None
        self.secret = secret
        self.memory_path = memory_path
        self.userid = userid or "100"
        self.stealth = stealth
        self.verbose = verbose
        self.reporter = InvestigativeReporter()
        self.findings = []
        
    def run_investigation(self):
        logger.inf("="*60)
        logger.inf(" LOGIC GUARD ELITE: AGENTIC REASONING ENGINE")
        logger.inf("="*60)
        
        # Step 0: Forensic Memory Pivot
        if self.memory_path:
            logger.inf(f"🔍 STEP 0: Initiating Forensic Pivot from RAM: {os.path.basename(self.memory_path)}")
            self._step_memory_forensics()
        else:
            logger.warn("⚠️  Skipping Step 0: No Memory Artifact provided. Using manual input targets.")

        if not self.target:
            logger.error("[X] NO TARGET: Provide a target URL via -t or provide -m for memory extraction.")
            return

        # Step 1: Recon & Target Discovery
        logger.inf("🌐 STEP 1: Discovering API Footprint and Hidden Assets...")
        self._step_discovery_recon()

        # Step 2: JWT/Session Analysis
        logger.inf("🔐 STEP 2: Analyzing Session Tokens and Cryptographic Integrity...")
        self._step_passive_discovery()
        self._step_cryptographic_audit()

        # Step 3: Business Logic & IDOR Audit
        logger.inf("🧠 STEP 3: Executing Agentic Logic Audit (IDOR/Bypass Checks)...")
        self._step_access_control()

        # Step 4: Stress/Concurrency Audit
        logger.inf("⚡ STEP 4: Stress Testing Concurrent Execution Limits...")
        self._step_stress_audit()
        
        # Final Narrative Generation
        self.reporter.generate_final_narrative(self.findings, self.target, self.token)

    def _step_discovery_recon(self):
        from logic_guard.modules.discovery import DiscoveryEngine
        discovery = DiscoveryEngine(self.target)
        discovery.run_recon()

    def _step_cryptographic_audit(self):
        if self.token:
            from logic_guard.modules.crypto import CryptoFuzzer
            crypto = CryptoFuzzer(self.token)
            crypto.audit_jwt_strength()

    def _step_stress_audit(self):
        from logic_guard.modules.stress import StressAuditor
        stress = StressAuditor(self.target, self.stealth)
        stress.run_volumetric_test()

    def _step_memory_forensics(self):
        from logic_guard.modules.memory import extract_api_data_from_memory
        logger.info("\n[ANALYSIS] Reasoning: No target provided, but memory dump detected. Analyzing RAM for traces of Evil...")
        mem_data = extract_api_data_from_memory(self.memory_path)
        
        if mem_data:
            if mem_data["tokens"] and not self.token:
                self.token = validate_token(mem_data["tokens"][0])
                logger.info(f"[REASONING] SELF-CORRECTION: Successfully extracted JWT from memory. Using token for audit.")
            
            if mem_data["urls"] and not self.target:
                self.target = validate_url(mem_data["urls"][0])
                logger.info(f"[REASONING] SELF-CORRECTION: Successfully discovered API URL in memory: {self.target}")
            
            self.findings.append({"type": "MemoryForensics", "data": mem_data})

    def _step_passive_discovery(self):
        logger.info("\n[ANALYSIS] Reasoning: Initializing Passive Discovery Phase...")
        if self.token:
            results = analyze_jwt_locally(self.token)
            self.findings.append({"type": "Passive", "data": results})
        scan_for_env_files(self.target)

    def _step_access_control(self):
        logger.info("\n[REASONING] Reasoning: Analyzing Access Control for IDOR/Bypass...")
        
        attempts = 0
        max_attempts = 2
        success = False
        
        while attempts < max_attempts and not success:
            logger.info(f"[*] Attempting Logic Audit (Try {attempts + 1})...")
            
            # Real execution
            results = assess_business_logic(self.target, self.token, self.userid, secret=self.secret)
            if results:
                self.findings.append({"type": "AccessControl", "data": results})
                success = True
            
            if not success:
                logger.warn("[!] SELF-CORRECTION: Pivot required. Attempting Guest bypass...")
                self.token = None
                self.secret = None
            
            attempts += 1
            
        if not success:
            logger.error("[X] ALL REASONING PATHS EXHAUSTED for Access Control.")

    def log_agent_trace(self, action, reasoning, outcome):
        trace = f"ACTION: {action} | REASONING: {reasoning} | OUTCOME: {outcome}"
        logger.debug(trace)
