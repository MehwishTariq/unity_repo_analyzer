# tests/test_resolver.py
import os
import pytest
from unity_repo_reader.helper.report_path_resolver import SmartReportPathResolver

@pytest.fixture
def temp_workspace(tmp_path):
    """
    Creates a temporary sandbox directory for the duration of the test.
    Pytest deletes this folder automatically when the test finishes.
    """
    original_cwd = os.getcwd()
    os.chdir(tmp_path)  # Force Python to treat the sandbox as the active root directory
    yield tmp_path
    os.chdir(original_cwd)  # Restore your actual workspace directory after the test

def test_resolver_creates_v1_on_empty_folder(temp_workspace):
    resolver = SmartReportPathResolver()
    
    # Run the resolver on a brand new project name
    generated_path = resolver.resolve_output_path(project_name="default_project")
    
    # Verify the output string formatting maps exactly to your structural requirements
    expected_suffix = os.path.normpath("Reports/default_project/architecture_report_v1.md")
    assert generated_path.endswith(expected_suffix)
    
    # Verify the physical directory path was created on the disk sandbox
    assert os.path.exists(os.path.dirname(generated_path))

def test_resolver_auto_increments_existing_version(temp_workspace):
    resolver = SmartReportPathResolver()
    
    # Manually mimic an existing structure in our sandbox: Reports -> default_project
    mock_target_dir = os.path.join(temp_workspace, "Reports", "default_project")
    os.makedirs(mock_target_dir)
    
    # Plant a fake v1 and v2 report file inside the folder
    with open(os.path.join(mock_target_dir, "architecture_report_v1.md"), "w") as f:
        f.write("dummy content")
    with open(os.path.join(mock_target_dir, "architecture_report_v2.md"), "w") as f:
        f.write("dummy content")

    # Execute the resolver—it should read the folder, find v2, and return v3
    next_path = resolver.resolve_output_path(project_name="default_project")
    
    assert next_path.endswith(os.path.normpath("architecture_report_v3.md"))