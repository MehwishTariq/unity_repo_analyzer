import os
import threading
import time

import gradio as gr
import requests
import uvicorn

# Configuration
FASTAPI_HOST = os.getenv("FASTAPI_HOST", "127.0.0.1")
FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", "8000"))
FASTAPI_PATH = "/api/v1/audit"
FASTAPI_URL = f"http://{FASTAPI_HOST}:{FASTAPI_PORT}{FASTAPI_PATH}"

GRADIO_PORT = int(os.getenv("PORT", "7860"))


def start_fastapi_server():
    """Launch FastAPI backend in a daemon thread."""
    from unity_repo_analyzer.server import app as fastapi_app
    uvicorn.run(
        fastapi_app,
        host=FASTAPI_HOST,
        port=FASTAPI_PORT,
        log_level="warning"
    )


def run_gradio_audit(github_url, project_name, provider, api_key):
    """
    Acts as a client proxy. Triggered by the Gradio UI button, it sends an HTTP
    POST request to our local running FastAPI backend.
    """
    if not api_key:
        return "### Error: API Token is required to authenticate the model provider."
    if not github_url:
        return "### Error: Please provide a valid GitHub repository URL."
    
    headers = {"X-API-Key": api_key}
    payload = {
        "github_url": github_url,
        "project_name": project_name if project_name else "default_project",
        "provider": provider
    }
    
    try:
        # Route request to local FastAPI backend on correct port
        response = requests.post(FASTAPI_URL, json=payload, headers=headers, timeout=300)
        
        if response.status_code == 200:
            return response.json()["report"]
        else:
            error_msg = response.json().get("detail", "Unknown execution crash.")
            return f"### Audit Failed (Status {response.status_code})\n\n{error_msg}"
            
    except Exception as conn_error:
        return f"### UI Connection Timeout\nFailed to connect to backend at {FASTAPI_URL}\n\nError: {str(conn_error)}"


if __name__ == "__main__":
    # Start FastAPI backend in a daemon thread
    backend_thread = threading.Thread(target=start_fastapi_server, daemon=True)
    backend_thread.start()
    time.sleep(2)  # Give FastAPI time to start
    
    # Build Gradio UI
    with gr.Blocks(title="Unity Codebase Auditor Hub", theme=gr.themes.Soft()) as ui_dashboard:
        gr.Markdown("# Unity Repo Analyzer Hub")
        gr.Markdown(
            "Provide a public Unity GitHub repository to pull raw C# scripts via optimized "
            "Git sparse-checkouts, executing multi-agent architectural audits directly in your browser."
        )

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Audit Configuration")
                url_input = gr.Textbox(
                    label="GitHub Repository URL", 
                    placeholder="https://github.com/username/repo",
                    max_lines=1
                )
                name_input = gr.Textbox(
                    label="Project Identifier Tag", 
                    placeholder="e.g., SpaceShooterMVP",
                    value="Unity_Project_Audit",
                    max_lines=1
                )
                provider_dropdown = gr.Dropdown(
                    label="LLM Infrastructure Provider", 
                    choices=["groq", "openai", "anthropic"], 
                    value="groq"
                )
                key_input = gr.Textbox(
                    label="Provider Authentication Token (X-API-Key)", 
                    placeholder="paste your sk-... or gsk-... key here",
                    type="password"
                )
                audit_button = gr.Button("Execute Architectural Review", variant="primary")
                
            with gr.Column(scale=2):
                gr.Markdown("### Generated Architectural Analysis Report")
                report_output = gr.Markdown(value="*Awaiting input submission. Provide variables and trigger audit parameters...*")

        # Connect UI trigger button logic 
        audit_button.click(
            fn=run_gradio_audit, 
            inputs=[url_input, name_input, provider_dropdown, key_input], 
            outputs=report_output
        )

    # Launch Gradio UI
    ui_dashboard.launch(server_name="127.0.0.1", server_port=GRADIO_PORT)