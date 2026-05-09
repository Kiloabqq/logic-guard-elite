import logging
import os
import sys
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Force UTF-8 encoding for standard output to support emojis in Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, Exception):
        # Fallback for environments where reconfigure is not available
        pass

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, "logic_guard.log")

# Create a logger
logger = logging.getLogger("logic_guard")
logger.setLevel(logging.INFO)

# Add custom levels/colors
def success(msg): logger.info(f"{Fore.GREEN}[+] {msg}")
def warn(msg): logger.info(f"{Fore.YELLOW}[!] {msg}")
def error(msg): logger.info(f"{Fore.RED}[X] {msg}")
def info(msg): logger.info(f"{Fore.CYAN}[*] {msg}")
def debug(msg): logger.debug(f"{Fore.WHITE}[?] {msg}")

# Attach to logger instance for easy access
logger.success = success
logger.warn = warn
logger.err = error
logger.inf = info
logger.dbg = debug

# Create handlers
file_handler = logging.FileHandler(log_file, encoding='utf-8')
stream_handler = logging.StreamHandler(sys.stdout)

# Create formatters and add to handlers
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
