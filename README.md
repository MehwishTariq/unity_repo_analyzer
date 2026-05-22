sdk: docker
---
title: Unity Repo Analyzer
emoji: 🛠️
colorFrom: blue
colorTo: indigo
app_port: 7860
pinned: false
---

# Unity Repo Analyzer API

This is a FastAPI application driving an automated, Agentic RAG review crew built on top of CrewAI. 
It clones public GitHub repositories, performs sparse checkouts targeting code logic, and leverages Groq models to output production-ready project overviews.