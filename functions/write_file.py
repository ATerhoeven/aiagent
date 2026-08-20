import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        # validate, that the path to the directory is inside the working directory
        working_directory_abs_path = os.path.abspath(working_directory)
        file_path_abs_path = os.path.normpath(os.path.join(working_directory_abs_path, file_path))
        validate_target_directory = os.path.commonpath([working_directory_abs_path, file_path_abs_path]) == working_directory_abs_path
        
        # guardrail to prevent the LLM from going outside the directory
        if not validate_target_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            
        # check if file_path points to a directory
        if os.path.isdir(file_path_abs_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        try:
            # check if all parent directories exist and create them if neccessary
            # this line will do nothing, if all parent directories exist
            
            os.makedirs(os.path.dirname(file_path_abs_path), exist_ok=True)
            
            
            with open(file_path_abs_path, "w") as file:
                file.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except:
            return f'Error: something went wrong'

    except:
        return f'Error: something went wrong, please check if {file_path} is a valid file and inside the permitted working directory'