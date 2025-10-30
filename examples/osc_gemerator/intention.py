#!/usr/bin/env python3
## generation intention with LLM model using template
# Add the parent directory to the path so we can import the agent package
from pathlib import Path
import sys
parent_dir = str(Path(__file__).parent.parent.parent.absolute())
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from typing import List
from cursor_agent_tools import OpenAICompatibleAgent


IntentionRewritePrompt = """
作为自动驾驶场景设计专家，请基于以下输入改写生成详细的场景描述:
要求包含以下几个关键要素：
静态环境：这是场景发生的舞台。你需要定义地图（如高速公路、城市十字路口）和道路结构（车道数、交通标志、路缘石等）。。
动态实体：指场景中所有会动的参与者及其属性。主要包括：
    主车：被测的自动驾驶车辆。需要定义其初始位置、速度、车型等属性。
    其他交通参与者：如NPC车辆、行人、自行车等。需要定义他们的初始状态，如位置、速度、车型。
行为与动作：这是场景的灵魂，定义了动态实体如何随时间演变和交互。例如：车辆A在T1时刻发起变道。行人B在T2时刻从路边闯入车道。主车需要对这些事件做出反应。
触发与条件：场景中事件发生的规则。例如，“当主车与前方车辆距离小于10米时，前车开始紧急制动”。

输入: {context}

详细的场景描述:
"""

class IntentionGenerator:
    def __init__(self, agent:OpenAICompatibleAgent):
        self.agent = agent

    def remove_think_tags(self, text):
        import re
        # 使用正则表达式移除 <think> 和 </think> 之间的内容
        return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)


    async def generate_intention(self, context: str) -> str:
        # model_response = await self.agent.client_simple.models.list()
        # for model in model_response:
        #     print(model.id)

        message  = IntentionRewritePrompt.format(context=context)
        response = await self.agent.chat_simple(message, enable_thinking=True)
        #remove thinking from response

        response = self.remove_think_tags(response)
        # Select the appropriate template based on context
        if response:
            return response.strip()
        raise ValueError("No applicable template found for the given context.")
