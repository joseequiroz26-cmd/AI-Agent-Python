import os

def get_file_content(working_directory: str, file_path: str) -> str:
    try:    
        the_directory = os.path.abspath(working_directory)
        target_file = os.path.abspath(os.path.join(the_directory, file_path))


        
        if  os.path.commonpath([the_directory, target_file])!=the_directory:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        MAX_CHARS = 10000

        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
        
    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads files from the specified file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory were we are getting file content",
                },
            },
            "required": ["file_path"],
        },
    },
}