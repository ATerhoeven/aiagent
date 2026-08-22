from collections.abc import Iterable
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from openai.types.chat import ChatCompletionToolUnionParam


available_functions: Iterable[ChatCompletionToolUnionParam] = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
]