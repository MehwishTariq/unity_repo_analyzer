import os
import re

class SmartReportPathResolver:
    """
    A pure Python helper class to handle project folder classification 
    and report version auto-incrementing.
    """
    def resolve_output_path(self, project_name: str) -> str:
        # 1. Standardize folder formatting
        clean_project = project_name.strip().replace(" ", "_").lower()
        
        # 2. Map path: CurrentDirectory -> Reports -> project_name
        current_dir = os.getcwd()
        target_dir = os.path.normpath(os.path.join(current_dir, "Reports", clean_project))

        # 3. Create folders if they don't exist yet
        if not os.path.exists(target_dir):
            print(f"[SYSTEM] Creating new directory structure: {target_dir}")
            os.makedirs(target_dir)

        # 4. Scan folder to find the highest version number
        pattern = re.compile(rf"{re.escape(clean_project)}_architecture_report_v(\d+)\.md")
        highest_version = 0

        try:
            for file_name in os.listdir(target_dir):
                match = pattern.match(file_name.lower())
                if match:
                    current_version_num = int(match.group(1))
                    if current_version_num > highest_version:
                        highest_version = current_version_num
        except Exception as e:
            print(f"[SYSTEM WARN] Error scanning directory: {str(e)}")

        # 5. Increment version and return full destination string
        next_version = highest_version + 1
        new_filename = f"architecture_report_v{next_version}.md"
        
        return os.path.normpath(os.path.join(target_dir, new_filename))