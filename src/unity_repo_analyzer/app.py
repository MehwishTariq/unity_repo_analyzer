from unity_repo_analyzer.helper.monkey_patch import patch

patch()
  
import os
import gradio as gr

from unity_repo_analyzer.crawler import Crawler

GRADIO_PORT = int(os.getenv("PORT", "7860"))

def run_gradio_audit(github_url, project_name, provider, api_key):
    """
    Bypasses the local HTTP network layer entirely. Calls the Crawler runtime 
    directly in-memory to prevent stream latency and eliminate tool-use crashes.
    """
    if not api_key:
        return "### Error: API Token is required to authenticate the model provider."
    if not github_url:
        return "### Error: Please provide a valid GitHub repository URL."
        
    # Clean and sanitize inputs just like our endpoint does
    selected_provider = provider.lower().strip()
    proj_name = project_name if project_name else "Unity_Project_Audit"
    
    try:
        # CRITICAL CHANGE: Invoke the crawler directly in-memory!
        # No 'requests.post', no local network delays, no blocked sockets.
        report_markdown_content = Crawler().analyze_public_repo(
            github_url=str(github_url),
            project_name=proj_name,
            client_api_key=api_key,
            provider=selected_provider 
        )
        
        return report_markdown_content
        
    except Exception as engine_error:
        return f"### Audit Failed during direct agent execution:\n\n{str(engine_error)}"


if __name__ == "__main__":
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
    ui_dashboard.launch(server_name="0.0.0.0", server_port=GRADIO_PORT)