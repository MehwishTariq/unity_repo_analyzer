import os
import shutil
import tempfile
from urllib.parse import urlparse
from git import Repo
from unity_repo_analyzer.crew import UnityRepoReader

class Crawler:
    """Handles ephemeral sandboxing for remote target projects."""

    @staticmethod
    def remove_readonly(func, path, excinfo):
        """
        Clears the read-only bit on files that block Windows from deleting them.
        """
        try:
            # 0o777 gives full read, write, and execute permissions across platforms
            os.chmod(path, 0o777)
            func(path)
        except Exception:
            # Absolute fallback: If Python's os module is locked out by Windows,
            # use a direct command line 'attrib' call to strip the read-only flag.
            if os.name == 'nt': # Checks if running on Windows
                os.system(f'attrib -R "{path}"')
                try:
                    func(path)
                except Exception:
                    pass # Guard against crashing if file was already wiped out

    @staticmethod
    def sanitize_github_url(url: str) -> str:
        url_str = str(url).strip()
        if url_str.startswith("http://"):
            url_str = url_str.replace("http://", "https://", 1)
        parsed = urlparse(url_str)
        path_parts = [part for part in parsed.path.split("/") if part]
        if len(path_parts) >= 2:
            username = path_parts[0]
            repo_name = path_parts[1].replace(".git", "")
            return f"https://github.com/{username}/{repo_name}.git"
        return url_str
        

    @staticmethod
    def analyze_public_repo(github_url: str, project_name: str, client_api_key: str | None, provider: str | None) -> str:
        clean_url = Crawler.sanitize_github_url(github_url)

        try:
            tmp_dir = Crawler.sparse_checkout(clean_url)

            inputs = {'repo': tmp_dir}

            print(f"[CREW] Initializing multi-agent setup utilizing provider: {provider}")
            # PASS THE ENGINE CONFIG: We pass both parameters down to our updated crew class
            crew_instance = UnityRepoReader(project_name=project_name, api_key=client_api_key, provider=provider)#type: ignore 

            crew_output = crew_instance.crew().kickoff(inputs=inputs)
            return str(crew_output)

        except Exception as error:
            raise error
        finally:
            if os.path.exists(tmp_dir):
                print(f"[CLEANUP] Safely purging directory: {tmp_dir}")
                shutil.rmtree(tmp_dir, onexc=Crawler.remove_readonly)
                print("[CLEANUP] Directory fully purged.")
                
    @staticmethod
    def sparse_checkout(clean_url: str) -> str:
        tmp_dir = tempfile.mkdtemp(prefix="crew_audit_")

        try:
            print(f"[SPARSE INIT] Bootstrapping empty git container at: {tmp_dir}")
            # 1. Initialize a blank local repository inside our temporary folder
            repo = Repo.init(tmp_dir)
            
            # 2. Add the remote tracking target destination
            origin = repo.create_remote('origin', clean_url)
            
            print("[SPARSE CONFIG] Activating cone filter selections...")
            # 3. Configure Git to allow selective sparse checkout directories
            with repo.config_writer() as writer:
                writer.set_value("core", "sparseCheckout", "true")
                writer.set_value("core", "sparseCheckoutCone", "true")
            
            # 4. Define the exact path constraint rules (only materialize Assets/Scripts)
            # This populates the internal sparse-checkout file profile
            sparse_checkout_path = os.path.join(tmp_dir, ".git", "info", "sparse-checkout")
            os.makedirs(os.path.dirname(sparse_checkout_path), exist_ok=True)
            with open(sparse_checkout_path, "w", encoding="utf-8") as file:
                # This captures it at the root, inside subfolders, and handles variations smoothly
                file.write("**/Assets/Scripts/**\n")
                file.write("**/assets/scripts/**\n")

            print("[GIT FETCH] Running narrow data pull...")
            # 5. Execute shallow fetch. The 'filter' parameter tells GitHub 
            # not to send binary contents (blobs) for files outside our selection filter list.
            origin.fetch(
                depth=1, 
                filter="blob:none",
                refspec="HEAD"
            )
            
            print("[GIT CHECKOUT] Realizing file systems...")
            # 6. Pull the trigger to materialize ONLY the scripts into our work folder
            repo.git.checkout("FETCH_HEAD")
            print("[CRAWLER] Workspace ready. Heavy assets omitted successfully!")
            return tmp_dir
        
        except Exception as error:
            raise error