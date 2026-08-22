import os
from openai.types.chat import ChatCompletionToolUnionParam

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_directory_abs_path = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_directory_abs_path, file_path))
        validate_file_path = os.path.commonpath([working_directory_abs_path, abs_file_path]) == working_directory_abs_path
        
        
        # check if file_path is in the working directory
        if not validate_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # check if file_path is a file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        file = open(abs_file_path)

        # read the first 10000 characters
        content = file.read(10000)

        # check if the file continues after 10000 characters and if it does, add a message
        if file.read(1):
            content += f'[...File "{file_path}" truncated at 10000 characters]'

        return content

    except:
        return f"Error: please check {file_path} again"

schema_get_file_content: ChatCompletionToolUnionParam = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Lists the content of a file on a specified file path relative to the working directory, providing file content up to 10000 chracters and file status",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to list content from, relative to the working directory",
                },
            },
        },
    },
}