from setuptools import setup, find_packages

setup(
    name="logic-guard-elite",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
        "colorama",
        "rich",
        "anthropic",
        "langchain",
    ],
    entry_points={
        "console_scripts": [
            "logic-guard=logic_guard.main:main",
        ],
    },
    author="Neo",
    description="Agentic API Incident Response & Auditing Framework for SIFT",
    license="MIT",
    keywords="pentest, forensics, agentic, api, sans, sift",
)
