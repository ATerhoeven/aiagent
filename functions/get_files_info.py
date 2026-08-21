import os
from openai.types.chat import ChatCompletionToolUnionParam

def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:
    # validate, that the path to the directory is inside the working directory
        working_directory_abs_path = os.path.abspath(working_directory)
        target_directory_path = os.path.normpath(os.path.join(working_directory_abs_path, directory))
        validate_target_directory = os.path.commonpath([working_directory_abs_path, target_directory_path]) == working_directory_abs_path

    # guardrail to prevent the LLM from going outside the directory
        if not validate_target_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
    # check if directory is a valid directory and return its contents with filesize and if each item is a directory
        if os.path.isdir(target_directory_path):
            
            try:
                directory_list = os.listdir(target_directory_path)
                files_list_detailed = []
                for file in directory_list:
                    path_to_file = "/".join([target_directory_path, file])
                    files_list_detailed.append(f"- {file}: file_size={os.path.getsize(path_to_file)} bytes, is_dir={os.path.isdir(path_to_file)}")
                return "\n".join(files_list_detailed)

            except:
                return f'Error: something went wrong, please check if {directory} is a valid directory'

            return f'Success: "{directory}" is within the working directory'

        return f'Error: "{directory}" is not a directory'
    except:
        return f'Error: something went wrong, please check if {directory} is a valid directory and inside the permitted area'


schema_get_files_info: ChatCompletionToolUnionParam = {
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