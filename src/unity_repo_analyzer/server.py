from unity_repo_analyzer.helper.helper_functions import patch_for_groq

patch_for_groq()
  
import os
import uvicorn
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, HttpUrl
from typing import Optional
from unity_repo_analyzer.crawler import Crawler

app = FastAPI(
    title="Multi-LLM Unity Codebase Auditor Engine",
    description="Analyze codebase architectures using OpenAI, Anthropic, or Groq API tokens."
)

class AuditRequest(BaseModel):
    github_url: HttpUrl
    project_name: str
    # PROVIDER SELECTOR: Choose which engine to execute
    provider: str = "groq" # Options: "groq", "openai", "anthropic"

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")
    
@app.post("/api/v1/audit")
def trigger_repository_audit(
    payload: AuditRequest, 
    # Provide flexible header inputs for any API key type matching their preference
    X_API_Key: Optional[str] = Header(None, description="Your personal OpenAI, Anthropic, or Groq API token")
):
    """
    Accepts repository data, identifies selected LLM provider,
    safely validates the token, and runs the specific agent crew configuration.
    """
    if not X_API_Key:
        raise HTTPException(
            status_code=401, 
            detail="Missing Token. Please supply your API key in the 'X-API-Key' header parameter."
        )

    # Sanitize the input choice
    selected_provider = payload.provider.lower().strip()
    valid_providers = ["groq", "openai", "anthropic"]
    if selected_provider not in valid_providers:
        raise HTTPException(status_code=400, detail=f"Unsupported provider. Choose from: {valid_providers}")

    try:
        # Route the request payload and key downward to our crawler runtime
        report_markdown_content = Crawler().analyze_public_repo(
            github_url=str(payload.github_url),
            project_name=payload.project_name,
            client_api_key=X_API_Key,
            provider=selected_provider 
        )
        
        return {
            "status": "success",
            "project_name": payload.project_name,
            "provider_used": selected_provider,
            "scope_analyzed": ".../Assets/Scripts (All subdirectories)",
            "performance_mode": "Sparse checkout enabled (skipped assets/scenes/textures)",
            "report": report_markdown_content
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal engine execution crash: {str(e)}")
  

if __name__ == "__main__":
    # Fallback to 7860 if the PORT environment variable isn't specified
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("server:app", host="0.0.0.0", port=port)