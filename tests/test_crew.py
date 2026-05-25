# tests/test_crew.py
from pathlib import Path

import pytest
from unittest.mock import MagicMock
from crewai import Task
from src.unity_repo_analyzer.crew import UnityRepoReader

@pytest.fixture
def dummy_crew():
    crew = UnityRepoReader(project_name = "default_project", api_key = "", provider ="") #type: ignore
    
    # Use setattr to bypass Pylance's static property checking rule cleanly
    setattr(crew, "inputs", {
        "project_name": "default_project", 
        "repo": "/tmp/FakeUnityPath" if Path("/tmp").exists() else "C:\\FakeUnityPath"
    })
    return crew

def test_writer_task_intercepts_inputs_and_sets_output_file(dummy_crew):
    # Intercept the actual file system checker so it doesn't execute during the test
    mock_output_path = str(Path("MockWorkspace") / "Reports" / "default" / "architecture_report_v5.md")
    
    # Intercept the actual file system checker so it doesn't execute during the test
    dummy_crew.path_resolver.resolve_output_path = MagicMock(
        return_value=mock_output_path
    )

    # Trigger the task builder function method manually
    task = dummy_crew.writer_task()

    # Verify that CrewAI successfully outputs a valid Task type wrapper instance
    assert isinstance(task, Task)
    
    # Verify our dynamic runtime override worked smoothly
    assert task.output_file == mock_output_path
    
    # Verify the underlying utility was triggered with the correct parameters
    dummy_crew.path_resolver.resolve_output_path.assert_called_once_with(project_name="default_project")