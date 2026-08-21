from collections.abc import Iterable

from functions.get_files_info import schema_get_files_info
from openai.types.chat import ChatCompletionToolUnionParam


available_functions: Iterable[ChatCompletionToolUnionParam] = [
    schema_get_files_info,
]