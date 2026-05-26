import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the given python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file, needed to run the function.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguments to give commands in the function.",
            ),
        },
    ),
)

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(absolute_path, file_path))     
        valid_target_path = os.path.commonpath([absolute_path, target_path]) == absolute_path
        if valid_target_path is False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_path) is False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if target_path.endswith('.py') is False:
            return f'Error: "{file_path}" is not a Python file'
        command = ["python3", target_path]
        if args is not None:
            command.extend(args)
        result = subprocess.run(command, cwd=absolute_path, capture_output=True, text=True, timeout=30)
        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        else:
            output.append(f"STDOUT: {result.stdout}")
            output.append(f"STDERR: {result.stderr}")
        return "\n".join(output)
        
    except Exception as e:
          return f"Error: executing Python file: {e}"