import os

def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:
    # validate, that the path to the directory is inside the working directory
        working_directory_abs_path = os.path.abspath(working_directory)
        target_directory_path = os.path.normpath(os.path.join(working_directory_abs_path, directory))
        validate_target_directory = os.path.commonpath([working_directory_abs_path, target_directory_path]) == working_directory_abs_path

    # guardrail to prevent the LLM from going outside the directory
        if not validate_target_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
    # check if directory is a valid directory
        if os.path.isdir(directory):
            return f'Success: "{directory}" is within the working directory'

        return f'Error: "{directory}" is not a directory'
    except:
        return f'Error: something went wrong, please check if {directory} is a valid directory'