import subprocess
import os
from .tool import Tool


def run_python_file(working_directory, file_path, args=[]):
    # 构建完整路径
    full_path = os.path.join(working_directory, file_path)
    
    # 获取绝对路径以进行边界检查
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(full_path)
    
    # 验证路径是否在working_directory边界内
    if not os.path.commonpath([abs_working_dir]) == os.path.commonpath([abs_working_dir, abs_file_path]):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # 检查文件是否存在
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    # 检查是否为Python文件
    if not abs_file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        # 执行Python文件
        completed_process = subprocess.run(
            ['python3', abs_file_path] + args,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir
        )
        
        # 构建输出结果
        output_lines = []
        
        # 添加stdout内容（如果有）
        if completed_process.stdout.strip():
            output_lines.append(f"STDOUT: {completed_process.stdout.strip()}")
        
        # 添加stderr内容（如果有）
        if completed_process.stderr.strip():
            output_lines.append(f"STDERR: {completed_process.stderr.strip()}")
        
        # 添加退出代码信息（如果非零）
        if completed_process.returncode != 0:
            output_lines.append(f"Process exited with code {completed_process.returncode}")
        
        # 如果没有输出，返回默认消息
        if not output_lines:
            return "No output produced."
        
        # 将所有输出行合并为一个字符串
        return '\n'.join(output_lines)
    except subprocess.TimeoutExpired:
        return f"Error: executing Python file: Process timed out after 30 seconds"
    except PermissionError:
        return f"Error: executing Python file: Permission denied"
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = Tool(
    name="run_python_file",
    description="Executes a Python 3 file within the working directory and returns the output from the interpreter.",
    input_schema={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the Python file to execute, relative to the working directory.",
            }
        },
        "required": ["file_path"],
    }
)