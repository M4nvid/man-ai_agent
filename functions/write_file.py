import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file and/or it's contents in the given path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file, needed to run the function.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content of the file being written.",
            ),
        },
    ),
)

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_path, file_path))     
        valid_target_path = os.path.commonpath([absolute_path, target_path]) == absolute_path
        if valid_target_path == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        parent_dir = os.path.dirname(target_path)
        os.makedirs(parent_dir, exist_ok=True)
        with open(target_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
          return f"Error: {e}"