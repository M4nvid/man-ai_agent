import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
def get_files_info(working_directory, directory="."):
     try:
          absolute_path = os.path.abspath(working_directory)
          target_dir = os.path.normpath(os.path.join(absolute_path, directory))     
          valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path
          if valid_target_dir == False:
               return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
          if os.path.isdir(target_dir) == False:
               return f'Error: "{target_dir}" is not a directory'
          lines = []
          for name in os.listdir(target_dir):
               full_path = os.path.join(target_dir, name)
               size = os.path.getsize(full_path)
               lines.append( f'- {name}: file_size={size} bytes, is_dir={os.path.isdir(full_path)}' )
          return "\n".join(lines)
     except Exception as e:
          return f"Error: {e}"