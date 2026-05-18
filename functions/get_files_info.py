import os
def get_files_info(working_directory, directory="."):
     absolute_path = os.path.abspath(working_directory)
     target_dir = os.path.normpath(os.path.join(absolute_path, directory))     
     valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path
     if valid_target_dir == False:
          return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
     if os.path.isdir(directory) == False:
          return f'Error: "{directory}" is not a directory'
     return f'Success: "{directory}" is within the working directory'