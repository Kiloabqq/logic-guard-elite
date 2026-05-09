import argparse
import os
import sys
from logic_guard.agent.orchestrator import AgentOrchestrator
from logic_guard.core.logger import logger

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Logic Guard Elite - Agentic API IR Framework",
        formatter_class=argparse.RawTextHelpFormatter,
        allow_abbrev=False
    )
    parser.add_argument("-t", "--target", help="The target API URL")
    parser.add_argument("-k", "--token", help="The JWT or API Key")
    parser.add_argument("-s", "--secret", help="The Secret Key (if available)")
    parser.add_argument("-u", "--userid", help="User ID for IDOR testing")
    parser.add_argument("-m", "--memory", help="Path to a memory image (.img, .raw) to extract data from")
    parser.add_argument("--stealth", action="store_true", help="Reduces concurrency")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enables verbose investigative output")
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Initialize the Agentic Orchestrator
    orchestrator = AgentOrchestrator(
        target=args.target,
        token=args.token,
        secret=args.secret,
        userid=args.userid,
        memory_path=args.memory,
        stealth=args.stealth,
        verbose=args.verbose
    )
    
    try:
        orchestrator.run_investigation()
    except KeyboardInterrupt:
        logger.error("\n[X] Investigation halted by user.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"[X] Critical System Failure: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
