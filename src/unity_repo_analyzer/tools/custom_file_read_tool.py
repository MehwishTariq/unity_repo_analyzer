from crewai_tools import FileReadTool


class SafeFileReadTool(FileReadTool):
    def _run(self, **kwargs):
        # Explicitly clean 'start_line' if Groq sent it as a string
        if 'start_line' in kwargs and isinstance(kwargs['start_line'], str):
            try:
                kwargs['start_line'] = int(kwargs['start_line'])
            except ValueError:
                kwargs['start_line'] = 1 # Safe default fallback

        # Explicitly clean 'line_count' if Groq sent "none" or text numbers
        if 'line_count' in kwargs:
            if isinstance(kwargs['line_count'], str):
                try:
                    kwargs['line_count'] = int(kwargs['line_count'])
                except ValueError:
                    kwargs['line_count'] = None # Safe default fallback for "none"
                    
        return super()._run(**kwargs)