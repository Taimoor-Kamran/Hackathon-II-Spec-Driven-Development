# Hackathon II: The Evolution of Todo

This repository contains the implementation of the Hackathon II project: "The Evolution of Todo – Mastering Spec-Driven Development & Cloud Native AI". The project consists of 5 phases, each building upon the previous one to evolve from a simple console app to a cloud-native AI chatbot.

## Project Overview

The Evolution of Todo is a 5-phase project that takes a simple console application and evolves it into a fully-featured, cloud-native AI chatbot deployed on Kubernetes. This journey teaches the Nine Pillars of AI-Driven Development, Claude Code, Spec-Driven Development with Reusable Intelligence, and Cloud-Native AI technologies through hands-on implementation.

## Phases

- **[Phase I](./Phase_I): Todo In-Memory Python Console App** - Basic CLI app with in-memory storage
- **Phase II**: Full-Stack Web Application - Next.js + FastAPI with database
- **Phase III**: AI-Powered Todo Chatbot - OpenAI integration with MCP
- **Phase IV**: Local Kubernetes Deployment - Minikube with Helm
- **Phase V**: Advanced Cloud Deployment - DOKS/GKE/AKS with Kafka and Dapr

## Getting Started

Each phase is contained in its own directory with its own documentation and implementation. Start with Phase I and work your way through sequentially.

### Running Phase I

To run the Phase I Todo In-Memory Python Console App:

1. **Prerequisites:**
   - Python 3.13+
   - UV package manager (install with `pip install uv`)

2. **Quick Setup:**
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd Hackathon_II/Phase_I

   # Create virtual environment
   uv venv

   # Activate virtual environment
   source .venv/bin/activate  # On Linux/Mac
   # or
   source .venv\Scripts\activate  # On Windows

   # Install the application
   uv pip install -e .

   # Run the application
   python -m src.main
   ```

3. **Alternative:**
   You can also run the application using the provided runner script:
   ```bash
   cd Hackathon_II/Phase_I
   python run_app.py
   ```

## Development Workflow

This project follows the Space-Driven Development workflow:
1. Constitution (/sp.constitution): Define/update project principles
2. Specify (/sp.specify): Create features specification with user stories
3. Clarify (/sp.clarify): Resolve ambiguities in specifications
4. Plan (/sp.plan): Generate technical implementation plan
5. Tasks (/sp.tasks): Break down into actionable, testable tasks
6. Implement (/sp.implement): Execute tasks using Red-Green-Refactor
7. Document (/sp.adr): Record architectural decisions when significant
8. Record (/sp.phr): Create prompt History Records for traceability