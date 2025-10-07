import os
import logging
from typing import List, Dict, Any
from anthropic import Anthropic
from functions.tool import Tool
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

# 配置日志
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 定义AI智能体类
class AIAgent:
    def __init__(self):
        self.client = Anthropic()
        self.messages: List[Dict[str, Any]] = []
        self.tools: List[Tool] = []
        self.callable_function = {}
        self._setup_tools()
        logger.info(f"Agent initialized with {len(self.tools)} tools")
        print(f"Agent initialized with {len(self.tools)} tools")
    
    def _setup_tools(self):
        self.tools.extend([
            schema_get_file_content,
            schema_get_files_info,
            schema_run_python_file,
            schema_write_file,
        ])
        self.callable_function = {
            "get_file_content": get_file_content,
            "get_files_info": get_files_info,
            "run_python_file": run_python_file,
            "write_file": write_file,
        }

    def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        try:
            # 构建工作目录路径, 这里能操作的就是calculator目录下的文件，这里写死
            current_dir = os.path.dirname(os.path.abspath(__file__))
            working_directory = os.path.join(current_dir, "calculator")
            
            # 验证工作目录是否存在
            if not os.path.exists(working_directory):
                return f"Error: Working directory 'calculator' not found at {working_directory}"
            
            # 检查工具是否存在
            if tool_name not in self.callable_function:
                return f"Error: Tool '{tool_name}' not found. Available tools: {', '.join(self.callable_function.keys())}"
            
            # 执行工具函数并捕获可能的异常
            try:
                logger.info(f"[Executing tool] {tool_name} with input {tool_input}")
                return self.callable_function[tool_name](working_directory, **tool_input)
            except TypeError as e:
                # 参数类型错误
                return f"Error: Type error when executing {tool_name}: {str(e)}"
            except ValueError as e:
                # 参数值错误
                return f"Error: Value error when executing {tool_name}: {str(e)}"
            except PermissionError as e:
                # 权限错误
                return f"Error: Permission denied when executing {tool_name}: {str(e)}"
            except Exception as e:
                # 其他未知错误
                return f"Error: Unexpected error when executing {tool_name}: {str(e)}"
        except Exception as e:
            # 捕获整个执行过程中的任何异常
            return f"Error: Failed to execute tool: {str(e)}"


    def chat(self, user_input: str) -> str:
        logger.info(f"User input: {user_input[:50]}{'...' if len(user_input) > 50 else ''}")
        self.messages.append({"role": "user", "content": user_input})

        tool_schemas = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema,
            }
            for tool in self.tools
        ]

        while True:
            try:
                response = self.client.messages.create(
                    model="deepseek-chat",
                    max_tokens=4096,
                    system="You are a helpful coding assistant operating in a terminal environment. Output only plain text without markdown formatting, as your responses appear directly in the terminal. Be concise but thorough, providing clear and practical advice with a friendly tone. Don't use any asterisk characters in your responses.",
                    messages=self.messages,
                    tools=tool_schemas,
                )

                assistant_message = {"role": "assistant", "content": []}

                for content in response.content:
                    if content.type == "text":
                        assistant_message["content"].append(
                            {
                                "type": "text",
                                "text": content.text,
                            }
                        )
                    elif content.type == "tool_use":
                        assistant_message["content"].append(
                            {
                                "type": "tool_use",
                                "id": content.id,
                                "name": content.name,
                                "input": content.input,
                            }
                        )

                self.messages.append(assistant_message)

                tool_results = []
                for content in response.content:
                    if content.type == "tool_use":
                        result = self._execute_tool(content.name, content.input)
                        tool_results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": content.id,
                                "content": result,
                            }
                        )

                if tool_results:
                    self.messages.append({"role": "user", "content": tool_results})
                else:
                    return response.content[0].text if response.content else ""

            except Exception as e:
                logger.error(f"Chat error: {str(e)}")
                return f"Error: {str(e)}"

# 主程序入口,实现人类交互
if __name__ == "__main__":
    logger.info("Starting AI Agent application")
    # Initialize the agent
    agent = AIAgent()
    print("AI Code Assistant")
    print("=================")
    print("A conversational AI agent that can read, list, and edit files.")
    print("Type 'exit' or 'quit' to end the conversation.")
    print()    

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            if not user_input:
                continue

            print("\nAssistant: ", end="", flush=True)
            response = agent.chat(user_input)
            print(response)
            print()

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Runtime error: {str(e)}")
            print(f"\nError: {str(e)}")
            print()

# 参考 https://www.boot.dev/courses/build-ai-agent-python 实现