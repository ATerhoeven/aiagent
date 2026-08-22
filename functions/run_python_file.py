import os
import subprocess
from openai.types.chat import ChatCompletionToolUnionParam

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        # validate, that the path to the directory is inside the working directory
        working_directory_abs_path = os.path.abspath(working_directory)
        file_path_abs_path = os.path.normpath(os.path.join(working_directory_abs_path, file_path))
        validate_target_directory = os.path.commonpath([working_directory_abs_path, file_path_abs_path]) == working_directory_abs_path
            
        # guardrail to prevent the LLM from going outside the directory
        if not validate_target_directory:
           return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
                
        # check if file_path is a file and exists
        if not os.path.isfile(file_path_abs_path) and not os.path.exists(file_path_abs_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # check if file_path is a python file
        if not file_path_abs_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        try:
            command = ["python", file_path_abs_path]
            if args != None:
                command.extend(args)

            completed_process = subprocess.run(command, capture_output=True, timeout=30, text=True, cwd=working_directory_abs_path)
            output_string_list = []

            if completed_process.returncode != 0:
                output_string_list.append(f"Process exited with code {completed_process.returncode}")

            if len(completed_process.stderr) == len(completed_process.stdout) == 0:
                output_string_list.append("No output produced")

            if len(completed_process.stdout) != 0:
                output_string_list.append(f"STDOUT: {completed_process.stdout}")

            if len(completed_process.stderr) != 0:
                output_string_list.append(f"STDERR: {completed_process.stderr}")

            output_string = "\n".join(output_string_list)
            return output_string

        except Exception as e:
            return f"Error: executing Python file: {e}"
    
            
    
    except:
        return f'Error: something went wrong, please check if {file_path} is a valid file and inside the permitted working directory'

schema_run_python_file: ChatCompletionToolUnionParam = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a python file on a specified file path relative to the working directory, after checking, if the file exists and is a python file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the python file to run, relative to the working directory",
                },
                "args": {
                    "type": "array[string]",
                    "description": "Array of strings that contain additional inputs for specified python files"
                }
            },
        },
    },
}