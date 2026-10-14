import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        the_directory = os.path.abspath(working_directory)
        target_file = os.path.abspath(os.path.join(the_directory, file_path))

        if os.path.commonpath([the_directory, target_file]) != the_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        parent_directory = os.path.dirname(target_file)
        os.makedirs(parent_directory, exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
            return f"Error: {e}"


schema_write_file= {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "We write the content to the specified file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File were the content must be written",
                },
                "content": {
                     "type": "string",
                     "description": "The content that we will use to write"
                }
            },
            "required": ["file_path", "content"],
        },
    },
}