import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_directory = os.path.abspath(working_directory)
        target_dir = os.path.abspath(os.path.join(absolute_directory, directory))

        if os.path.commonpath(
            [absolute_directory, target_dir]) != absolute_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        items = []

        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)

            items.append(
                f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
            )

        return "\n".join(items)

    except Exception as e:
        return f"Error: {e}"
    

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


