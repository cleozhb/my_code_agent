# 背景
一个简单的code agent，参考 https://www.boot.dev/courses/build-ai-agent-python 实现，目的在于使用原生的python实现agent的全部功能，不用langchain这样的框架，从底层理解一下agent是如何工作的。
- agent的大脑：LLM（这个demo中用deepseek的api）
- memory：存储历史对话信息
- tools：预定义的工具，如代码执行器、文件操作器等
大多数框架都推行：让LLM理解一切。实际上我们并不想让LLM决定一切，只需要LLM完成它擅长的根据上下文推理，而其他的具体操作由确定性的代码完成。

# 安装依赖
``` 
uv venv .venv
source .venv/bin/activate
uv pip install anthropic
```
在运行之前需要设置环境变量 ANTHROPIC_API_KEY, MAC系统中是在 ~/.zshrc 中设置
```
export PATH="/Users/zhanghuibin/.npm-global/bin:$PATH"
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
DEEPSEEK_API_KEY="your-deepseek-api-key"
export ANTHROPIC_AUTH_TOKEN=${DEEPSEEK_API_KEY}
export API_TIMEOUT_MS=600000
export ANTHROPIC_MODEL=deepseek-chat
export ANTHROPIC_SMALL_FAST_MODEL=deepseek-chat
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
```

# 项目说明
这个demo实现的是一个简单的code agent。tools都放在了`functions`文件夹下，每个tool都是一个python文件，文件名就是tool的名称，文件内容就是tool的实现。
参考文档：
https://docs.claude.com/en/docs/agents-and-tools/tool-use/implement-tool-use
https://api-docs.deepseek.com/zh-cn/guides/anthropic_api

LLM的主流程在`main.py`中，实现了与用户的交互。
- 读文件内容
- list 文件夹下的内容
- 编辑现有文件，或创建新文件
- 执行python 文件
- 交互式的聊天，调用llm处理输入，llm调用文件处理工具
- 打印日志

因为能执行python文件，能读写python文件，所以这是个很危险的操作，我们必须指定操作的目录，不能操作任意目录下的文件。calculator这个目录下的文件实现了一个简单的计算器，能够进行加减乘除运算。最终可以用这个code agent完成对计算器功能的完善，bug修改，添加新功能，生成测试用例等，以此来验证自己实现的简易版code agent

# 运行项目
```
python main.py 
```
输入你想让code agent完成的任务，例如：
- 实现新功能：实现三角函数sin, cos, tan，并生成测试用例
- 实现生成随机数的功能，包括整数和浮点数
- 实现开平方根的功能，并生成测试用例