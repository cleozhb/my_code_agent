import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# 获取当前工作目录
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 构建calculator目录的绝对路径
calculator_dir = os.path.join(base_dir, "calculator")

print('===== 测试用例1: get_files_info("calculator", ".") =====')
result1 = get_files_info(calculator_dir, ".")
print(result1)
print()

print('===== 测试用例2: get_files_info("calculator", "pkg") =====')
result2 = get_files_info(calculator_dir, "pkg")
print(result2)
print()

print('===== 测试用例3: get_files_info("calculator", "/bin") =====')
result3 = get_files_info(calculator_dir, "/bin")
print(result3)
print()

print('===== 测试用例4: get_files_info("calculator", "../") =====')
result4 = get_files_info(calculator_dir, "../")
print(result4)
print()

# 测试get_file_content函数
print('===== 测试用例5: get_file_content("calculator", "main.py") =====')
result5 = get_file_content(calculator_dir, "main.py")
print(result5[:100] + '\n...' if len(result5) > 100 else result5)
print()

print('===== 测试用例6: get_file_content("calculator", "pkg/calculator.py") =====')
result6 = get_file_content(calculator_dir, "pkg/calculator.py")
print(result6[:100] + '\n...' if len(result6) > 100 else result6)
print()

print('===== 测试用例7: get_file_content("calculator", "/bin/cat") =====')
result7 = get_file_content(calculator_dir, "/bin/cat")
print(result7)
print()

print('===== 测试用例8: get_file_content("calculator", "pkg/does_not_exist.py") =====')
result8 = get_file_content(calculator_dir, "pkg/does_not_exist.py")
print(result8)
print()

# 测试write_file函数
print('===== 测试用例9: write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum") =====')
result9 = write_file(calculator_dir, "lorem.txt", "wait, this isn't lorem ipsum")
print(result9)
print()

print('===== 测试用例10: write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet") =====')
result10 = write_file(calculator_dir, "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print(result10)
print()

print('===== 测试用例11: write_file("calculator", "/tmp/temp.txt", "this should not be allowed") =====')
result11 = write_file(calculator_dir, "/tmp/temp.txt", "this should not be allowed")
print(result11)
print()

# 测试run_python_file函数
print('===== 测试用例12: run_python_file("calculator", "main.py") =====')
result12 = run_python_file(calculator_dir, "main.py")
print(result12)
print()

print('===== 测试用例13: run_python_file("calculator", "main.py", ["3 + 5"]) =====')
result13 = run_python_file(calculator_dir, "main.py", ["3 + 5"])
print(result13)
print()

print('===== 测试用例14: run_python_file("calculator", "tests.py") =====')
result14 = run_python_file(calculator_dir, "tests.py")
print(result14)
print()

print('===== 测试用例15: run_python_file("calculator", "../main.py") =====')
result15 = run_python_file(calculator_dir, "../main.py")
print(result15)
print()

print('===== 测试用例16: run_python_file("calculator", "nonexistent.py") =====')
result16 = run_python_file(calculator_dir, "nonexistent.py")
print(result16)