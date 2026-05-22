import os
import re
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class UnityMapperInput(BaseModel):
    repo_path: str = Field(description="The absolute path to the Unity project folder.")

class UnityCSharpMapperTool(BaseTool):
    name: str = "Unity C# Structural Mapper Tool"
    description: str = "Scans a Unity project directory to map out custom C# classes, their inheritances, and core methods."
    args_schema: Type[BaseModel] = UnityMapperInput

    def _run(self, repo_path: str) -> str:
        architecture_map = []
        
        # 1. Clean the input from standard string wrappers
        raw_str = str(repo_path).strip()
        
        # 2. FIX: If the LLM spilled the whole Pydantic dictionary representation into the string
        if "value:" in raw_str:
            # Extract whatever is inside 'value: ...' up until the closing brace
            match = re.search(r'value:\s*([^}]+)', raw_str)
            if match:
                raw_str = match.group(1).strip()
        elif "repo_path:" in raw_str:
            match = re.search(r'repo_path:\s*([^\,]+)', raw_str)
            if match:
                raw_str = match.group(1).strip()
                
        # Clean up any rogue quotation marks and normalize Windows backslashes
        cleaned_path = repo_path.replace('"', '').replace("'", "").strip()
        cleaned_path = os.path.abspath(cleaned_path)
        
        print(f"\n[DEBUG] Tool is actively scanning path: {cleaned_path}")

        # Enhanced regex: matches classes inside namespaces, structs, or custom formatting
        class_pattern = re.compile(r'(?:public|internal|private|protected)?\s*(?:abstract|partial)?\s*class\s+(\w+)(?:\s*:\s*([\w\s,<>]+))?')
        method_pattern = re.compile(r'(?:public|protected|private|internal)\s+(?:virtual|override|static|async\s+)?[\w<>\s]+\s+(\w+)\s*\([^)]*\)')

        if not os.path.exists(cleaned_path):
            print(f"[DEBUG ERROR] Path does not exist: {cleaned_path}")
            return f"Error: The directory path '{cleaned_path}' does not exist on this machine."

        file_count = 0
        for root, _, files in os.walk(cleaned_path):
            # Skip noise directories completely
            if any(dir_name in root for dir_name in ['Editor', 'Plugins', 'Packages', '.git', 'ThirdParty']):
                continue
                
            for file in files:
                if file.lower().endswith('.cs'):
                    file_count += 1
                    file_path = os.path.normpath(os.path.join(root, file))
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                            classes = class_pattern.findall(content)
                            methods = method_pattern.findall(content)
                            
                            lifecycle_methods = ['Start', 'Update', 'Awake', 'FixedUpdate', 'LateUpdate', 'OnEnable', 'OnDisable']
                            core_methods = list(set([m for m in methods if m not in lifecycle_methods and not m.startswith('if')]))
                            unity_lifecycle = list(set([m for m in methods if m in lifecycle_methods]))

                            for class_name, base_classes in classes:
                                # Filter out false matches from standard code keywords
                                if class_name in ['set', 'get', 'value', 'class']:
                                    continue
                                    
                                base_info = base_classes.strip() if base_classes else "Pure C# Class"
                                
                                snippet = (
                                    f"Script Path: {file_path}\n"
                                    f"  - Class Name: {class_name}\n"
                                    f"  - Inherits From: [{base_info}]\n"
                                    f"  - Unity Lifecycle Used: {unity_lifecycle}\n"
                                    f"  - Custom Methods: {core_methods}\n"
                                    f"----------------------------------------"
                                )
                                architecture_map.append(snippet)
                    except Exception as e:
                        print(f"[DEBUG] Failed to read file {file}: {str(e)}")
                        continue
                            
        print(f"[DEBUG] Total C# files processed by tool: {file_count}")
        print(f"[DEBUG] Total architecture blocks generated: {len(architecture_map)}")
        
        return "\n".join(architecture_map) if architecture_map else "No custom C# classes or structures could be parsed from this directory layout."