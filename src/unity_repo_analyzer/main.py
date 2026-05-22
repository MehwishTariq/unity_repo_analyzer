#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from unity_repo_analyzer.crew import UnityRepoReader

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
        
def run():
    """
    Run the crew. Prompts the user interactively for a repository path.
    """
    # 1. Check if a path was passed via command line argument first (e.g., crewai run -- "C:/MyProj")
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        repo_path = sys.argv[1]
    else:
        # 2. If no argument was provided, ask the user interactively in the terminal
        print("\nUnity Codebase Architecture Audit")
        repo_path = input("Please enter the absolute path to your Unity Assets folder: ").strip()
        project_name = input("Please enter the name of your Unity project (for report naming): ").strip()
        
    # Fallback to current directory if the user just presses Enter
    if not repo_path:
        repo_path = "."
        print("No path provided. Defaulting to current directory ('.')")

    inputs = {
        'repo': repo_path
    }

    try:
        print(f"Starting analysis on: {repo_path}\n")
        UnityRepoReader(project_name=project_name).crew().kickoff(inputs=inputs) #type: ignore
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    repo_path = sys.argv[2] if len(sys.argv) > 2 else "."
    inputs = {
        'repo': repo_path,
    }
    try:
        UnityRepoReader().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        UnityRepoReader().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    repo_path = sys.argv[2] if len(sys.argv) > 2 else "."
    inputs = {
        'repo': repo_path,
    }

    try:
        UnityRepoReader().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "repo": trigger_payload.get("repo", ""),
    }

    try:
        result = UnityRepoReader().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
