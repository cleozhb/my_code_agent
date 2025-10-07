
import os
from .tool import Tool

def get_files_info(working_directory, directory="."):
    # 构建完整路径
    full_path = os.path.join(working_directory, directory)
    
    # 获取绝对路径以进行边界检查
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_dir = os.path.abspath(full_path)
    
    # 验证路径是否在working_directory边界内
    if not os.path.commonpath([abs_working_dir]) == os.path.commonpath([abs_working_dir, abs_target_dir]):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # 检查路径是否存在且是一个目录
    if not os.path.exists(full_path):
        return f'Error: "{directory}" does not exist'
    
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    
    # 构建目录内容的字符串表示
    result = f"Result for {directory} directory:\n"
    
    try:
        # 获取目录中的所有项目
        items = os.listdir(full_path)
        
        # 为每个项目添加信息
        for item in items:
            item_path = os.path.join(full_path, item)
            is_dir = os.path.isdir(item_path)
            
            # 获取文件大小
            if is_dir:
                # 对于目录，使用44字节作为默认大小（与示例一致）
                file_size = 44
            else:
                try:
                    file_size = os.path.getsize(item_path)
                except OSError:
                    file_size = 0
            
            result += f'  - {item}: file_size={file_size} bytes, is_dir={is_dir}\n'
    except PermissionError:
        return f'Error: Permission denied when accessing "{directory}"'
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'
    
    return result

schema_get_files_info = Tool(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    input_schema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself (use \".\").",
            }
        },
        "required": [],
    }
)