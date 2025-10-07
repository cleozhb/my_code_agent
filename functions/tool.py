from pydantic import BaseModel
from typing import Dict, Any

# 定义工具类，用于描述每个工具的名称、描述和输入参数的JSON模式
class Tool(BaseModel):
    name: str
    description: str
    input_schema: Dict[str, Any]
