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
👉 **[Interactive Swagger API Documentation](https://codename1999-unity_repo_analyzer.hf.space/docs)**

---

## 💡 Key Engineering Wins & Architecture Highlights

This project demonstrates production-grade backend engineering, solving complex bottlenecks inherent to distributed AI agent execution:

* **Platform-Agnostic File IO Sandbox:** Engineered a dynamic, cross-platform workspace system that fluidly translates file paths and execution parameters across local Windows developer environments and cloud Linux containers natively.
* **Strict LLM Schema Interception:** Authored a robust custom runtime middleware layer (`SafeGroqFileReadTool`) to intercept, clean, and cast unstable LLM JSON tool payloads into strictly validated types. This effectively mitigates schema-drift crashes common in hyper-fast inference models like Groq.
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
git clone [https://github.com/YOUR_USERNAME/unity_repo_analyzer.git](https://github.com/YOUR_USERNAME/unity_repo_analyzer.git)
cd unity_repo_analyzer
uv sync

```

### 2. Launching the Local API

Run the Uvicorn ASGI server locally with hot-reloading active:

```bash
uv run uvicorn unity_repo_analyzer.main:app --reload --port 8000

```

Open `http://127.0.0.1:8000/docs` in your browser to view the interactive API playground.

### 3. Running the Comprehensive Test Suite

Validate the core routing utilities across platform abstractions:

```bash
uv run pytest

```
