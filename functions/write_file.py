import os
from .tool import Tool

def write_file(working_directory, file_path, content):
    # 构建完整路径
    full_path = os.path.join(working_directory, file_path)
    
    # 获取绝对路径以进行边界检查
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(full_path)
    
    # 验证路径是否在working_directory边界内
    if not os.path.commonpath([abs_working_dir]) == os.path.commonpath([abs_working_dir, abs_file_path]):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        # 确保目录存在
        directory = os.path.dirname(abs_file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        # 写入/覆盖文件内容
        with open(abs_file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        # 返回成功消息
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except PermissionError:
        return f'Error: Permission denied when writing to "{file_path}"'
    except IsADirectoryError:
        return f'Error: "{file_path}" is a directory, not a file'
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

schema_write_file = Tool(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    input_schema={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The file path to write the content to, relative to the working directory.",
            },
            "content": {
                "type": "string",
                "description": "The content you want to write into the file.",
            }
        },
        "required": ["file_path", "content"],
    }
)