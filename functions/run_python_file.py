import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        the_directory = os.path.abspath(working_directory)
        target_file = os.path.abspath(os.path.join(the_directory, file_path))
        
        if os.path.commonpath([the_directory, target_file])!= the_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)
        result = subprocess.run(
            command, 
            cwd=the_directory,
            capture_output=True, 
            text=True, 
            timeout=30
            )

        
        output_parts = []
        if result.returncode != 0:
             output_parts.append(f"Process exited with code {result.returncode}")
        

        if not result.stdout and not result.stderr:
            output_parts.append (f"No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")
        return "\n".join(output_parts)
    except Exception as e:
       return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file with optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "PPath to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional command-line arguments to pass to the file"
                }
            },"required": ["file_path"]
        },
    },
}

 
