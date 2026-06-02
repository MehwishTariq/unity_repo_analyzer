---
title: Unity Repo Analyzer
emoji: 🛠️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# 🛠️ AI-Driven Unity Repository Analyzer

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![AI Engine](https://img.shields.io/badge/AI_Engine-CrewAI-ff69b4.svg)](https://www.crewai.com/)
[![LLM Platform](https://img.shields.io/badge/LLM-Groq%20%2F%20Llama3-orange.svg)](https://groq.com/)
[![Deployment](https://img.shields.io/badge/Deployment-Docker%20%2F%20HuggingFace-blue.svg)](https://huggingface.co/)

An advanced, production-ready **Agentic RAG (Retrieval-Augmented Generation) pipeline** that automates architectural reviews of public Unity C# repositories. Built with **FastAPI** and **CrewAI**, the system optimizes context windows by executing high-speed, sparse Git checkouts, processing raw code structures, and serving structured markdown analysis via high-throughput **Groq LLM** hardware.

---

## 🔗 Live Interactive API Demo

Skip the local installation and test the live, containerized production API right now:
**(https://huggingface.co/spaces/MehwishTariq/unity_repo_analyzer)**

---
### 📄 View Pre-Generated Output
Don't have a Unity repository on hand? Look at a production-grade architectural review generated entirely by this system:
👉 **[Read the Sample Architecture Report](./Reports/count_master/architecture_report_v1.md)**

---

## 💡 Key Engineering Wins & Architecture Highlights

This project demonstrates production-grade backend engineering, solving complex bottlenecks inherent to distributed AI agent execution:

* **Platform-Agnostic File IO Sandbox:** Engineered a dynamic, cross-platform workspace system that fluidly translates file paths and execution parameters across local Windows developer environments and cloud Linux containers natively.
* **Strict LLM Schema Interception:** Authored a robust custom runtime middleware layer (`SafeFileReadTool`) to intercept, clean, and cast unstable LLM JSON tool payloads into strictly validated types. This effectively mitigates schema-drift crashes common in hyper-fast inference models like Groq.
* **High-Performance Context Isolation:** Implemented Git sparse-checkout routines to isolate game logic structures (C# scripts) away from heavy game binary metadata (`.meta`, assets), reducing LLM token consumption by up to **80%**.
* **Robust Automated Verification:** Designed a test suite leveraging `pytest` and `unittest.mock` to validate critical route path-generation mechanics deterministically without causing disk-write side effects.

---

## 📦 System Architecture Diagram

```text
[User Request: GitHub URL] 
         │
         ▼
 ┌───────────────┐
 │  FastAPI End  │
 └───────┬───────┘
         │ (Trigger Pipeline)
         ▼
 ┌───────────────┐
 │ Git Checkout  ├─► [Isolates C# Logic, Drops Heavy Assets]
 └───────┬───────┘
         │ (Clean Code Sandbox)
         ▼
 ┌───────────────┐     ┌───────────────────────┐
 │ CrewAI Engine ├────►│ SafeFileReadTool  │ ◄─ [Intercepts & Fixes Type Schemas]
 └───────┬───────┘     └───────────┬───────────┘
         │                         │
         ▼                         ▼
 ┌─────────────────────────────────────────────┐
 │    Groq Llama-3 Inference Processing        │
 └─────────────────────┬───────────────────────┘
                       │
                       ▼
         [Production Architectural Report]

```

---

## 🛠️ Local Installation & Development Guide

This project utilizes `uv`, a ultra-fast Python package installer and resolver.

### 1. Environment Setup

Clone the repository and automatically synchronize the locked project workspace environment:

```bash
git clone https://github.com/MehwishTariq/unity_repo_analyzer.git
cd unity_repo_analyzer
uv sync
```

### 2. Launching the Combined Gradio + FastAPI App

The application now runs as a single integrated service: **Gradio UI** (frontend) + **FastAPI** (backend) in one process.

```bash
# From the repository root
python src/unity_repo_analyzer/app.py
```

The Gradio interface will open automatically on `http://127.0.0.1:7860`.

- **Gradio UI:** http://127.0.0.1:7860 (interactive web interface)
- **FastAPI backend:** http://127.0.0.1:8000 (runs internally, called by Gradio)

### 3. Running the Comprehensive Test Suite

Validate the core routing utilities across platform abstractions:

```bash
uv run pytest
```

### 4. Custom Environment Variables (Optional)

Override default ports or backend URL:

```bash
# Set custom Gradio port
$env:PORT = "7861"
python src/unity_repo_analyzer/app.py

# Set custom backend host/port (if running FastAPI separately)
$env:FASTAPI_HOST = "127.0.0.1"
$env:FASTAPI_PORT = "8000"
$env:FASTAPI_PATH = "/api/v1/audit"
python src/unity_repo_analyzer/app.py
```

### 5. Docker Build & Deployment

Build and run the containerized application for Hugging Face Spaces or local Docker:

```bash
docker build -t unity-repo-analyzer .
docker run -p 7860:7860 unity-repo-analyzer
```

Then visit `http://127.0.0.1:7860` in your browser.

---

## 🚀 Hugging Face Spaces Deployment

This application is optimized for **Hugging Face Spaces** using Docker.

1. **Create a new Space** on Hugging Face with Docker SDK
2. **Push this repository** to your Space
3. **Set environment variables** in Space Settings if needed (optional):
   - `FASTAPI_HOST` (default: `127.0.0.1`)
   - `FASTAPI_PORT` (default: `8000`)
   - `PORT` (default: `7860` — Spaces requirement)

The Space automatically detects the Dockerfile and deploys the combined Gradio + FastAPI application.

