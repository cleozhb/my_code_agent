import os
from config import MAX_FILE_SIZE
from .tool import Tool

def get_file_content(working_directory, file_path):
    # 构建完整路径
    full_path = os.path.join(working_directory, file_path)
    
    # 获取绝对路径以进行边界检查
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(full_path)
    
    # 验证路径是否在working_directory边界内
    if not os.path.commonpath([abs_working_dir]) == os.path.commonpath([abs_working_dir, abs_file_path]):
        return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'
    
    # 检查文件是否存在
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" does not exist'
    
    # 检查是否为文件而非目录
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" is not a file'
    
    try:
        # 读取文件内容
        with open(abs_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 检查文件大小并截断（如果需要）
        if len(content) > MAX_FILE_SIZE:
            truncated_content = content[:MAX_FILE_SIZE]
            return truncated_content + f'\n[...File "{file_path}" truncated at {MAX_FILE_SIZE} characters]'
        
        return content
    except PermissionError:
        return f'Error: Permission denied when accessing "{file_path}"'
    except UnicodeDecodeError:
        return f'Error: Cannot read "{file_path}" as text (binary file detected)'
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

schema_get_file_content = Tool(
    name="get_file_content",
    description="Reads and returns the first {MAX_FILE_SIZE} characters of the content from a specified file within the working directory.",
    input_schema={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path to the file whose content should be read, relative to the working directory.",
            }
        },
        "required": ["file_path"],
    }
)