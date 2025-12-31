# Jarvis DevOps Project

## Project Overview
Jarvis DevOps is a Dockerized Python command-line assistant designed to demonstrate core DevOps concepts such as containerization, automation, environment isolation, and production-safe application design.

The application accepts commands via CLI arguments, executes predefined actions, and produces structured logs suitable for containerized environments.

---

## Key Features
- Command-driven execution (CLI-based)
- Dockerized application using best practices
- Headless, production-safe design (no GUI dependency)
- Environment variable–based configuration
- Graceful degradation when optional services are unavailable

---

## Technologies Used
- **Containerization**: Docker
- **Programming Language**: Python 3.13
- **Automation & Scripting**: Python
- **Version Control**: Git & GitHub
- **DevOps Concepts**: ENTRYPOINT vs CMD, environment isolation, logging

---

## Project Structure
```text
Jarvis-Devops/
├── .gitignore          # Git ignore rules
├── Dockerfile          # Container definition
├── requirements.txt    # Python dependencies
├── main.py             # Main application logic
├── client.py           # Supporting logic/modules
└── README.md           # Project documentation

Getting Started for New Users

This section explains how a new user can set up and run the project locally using Docker.

Prerequisites

Make sure the following tools are installed on your system:

Docker

Git

Optional (for AI and news features):

API keys from:

OpenRouter
 (free tier available)

NewsAPI
 (free tier available)

 # 1. Clone the repository
git clone https://github.com/affan-bhutta/Jarvis-Devops.git
cd Jarvis-Devops

# 2. Configure environment variables
cp .env.example .env
# Edit .env and add your API keys if required

# 3. Build the Docker image
docker build -t jarvis-devops .

# 4. Run the application
docker run jarvis-devops open google



