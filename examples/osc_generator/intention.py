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
不要生成无关的信息，字数
控制在200字以内。

输入: {context}

详细的场景描述:
"""


Osc2IntentionPrompt = """
作为openscenario 2.0 DSL 语言专家，请基于以下的要求对于输入的DSL 代码片段进行理解，并生成结构化的输出:
要求包含以下几个关键要素：
1.输出代码描述的道路场景：json 字段名称为“道路场景”，输出的内容为当前输入文件描述的道路场景，可能是高速公路路口、城市交叉路口，分合流的路口，环岛等。
2.输出代码中场景的参与制：json 字段名称为“场景参与者”，输出的内容为当前输入文件中场景的主要参与者，包含主车和其他交通参与者，如NPC车辆、行人、自行车，静止物体，VRU等。
3.输出代码中场景的参与者的初始位置：json 字段名称为“初始位置”，输出内容为主要参与者与主车之间的空间关系，如：在主车对向车道20m，左侧右侧车道，前方/后方 100m等
4.输出代码中场景的主要参与者的动作：json 字段名称为“运动方向”，输出内容为当前输入文件中场景的场景参与者的动作描述，如：变道，超车，转弯，紧急制动，行人横穿马路等。
5.输出代码中主车的行驶意图：json 字段名称为“主车意图”，输出内容为当前输入文件中主车的行驶意图，如：左转弯，右转弯，直行，通过路口，避让行人，并入高速，驶出高速等。
6.输出代码中场景的触发条件：json 字段名称为“触发条件”，输出内容为当前输入文件中场景的触发条件，如：当主车与前车距离小于10米时，前车开始紧急制动等。
7.输出代码中的测试场景意图，json 字段名称为“测试意图”，输出内容为当前输入文件中场景的测试意图，如：测试鬼探头，测试车辆切入场景等。
输出的格式为 json 格式，示例如下:
{{
    "道路场景": "...",
    "场景参与者": "...",
    "初始位置": "...",
    "运动方向": "...",
    "主车意图": "...",
    "触发条件": "...",
    "测试意图": "..."
}}
不要生成无关的信息，字数
控制在500字以内。

输入: {context}

输出:

"""


Xml2IntentionPrompt = """
作为openscenario 1.0 XML 语言专家，请基于以下的要求对于输入的XML 代码片段进行理解，并生成结构化的输出:
要求包含以下几个关键要素：
1.输出代码描述的道路场景：json 字段名称为“道路场景”，输出的内容为当前输入文件描述的道路场景，可能是高速公路路口、城市交叉路口，分合流的路口，环岛等。
2.输出代码中场景的参与制：json 字段名称为“场景参与者”，输出的内容为当前输入文件中场景的主要参与者，包含主车和其他交通参与者，如NPC车辆、行人、自行车，静止物体，VRU等。
3.输出代码中场景的参与者的初始位置：json 字段名称为“初始位置”，输出内容为主要参与者与主车之间的空间关系，如：在主车对向车道20m，左侧右侧车道，前方/后方 100m等
4.输出代码中场景的主要参与者的动作：json 字段名称为“运动方向”，输出内容为当前输入文件中场景的场景参与者的动作描述，如：变道，超车，转弯，紧急制动，行人横穿马路等。
5.输出代码中主车的行驶意图：json 字段名称为“主车意图”，输出内容为当前输入文件中主车的行驶意图，如：左转弯，右转弯，直行，通过路口，避让行人，并入高速，驶出高速等。
6.输出代码中场景的触发条件：json 字段名称为“触发条件”，输出内容为当前输入文件中场景的触发条件，如：当主车与前车距离小于10米时，前车开始紧急制动等。
7.输出代码中的测试场景意图，json 字段名称为“测试意图”，输出内容为当前输入文件中场景的测试意图，如：测试鬼探头，测试车辆切入场景等。
输出的格式为 json 格式，示例如下:
{{
    "道路场景": "...",
    "场景参与者": "...",
    "初始位置": "...",
    "运动方向": "...",
    "主车意图": "...",
    "触发条件": "...",
    "测试意图": "..."
}}
不要生成无关的信息，字数
控制在500字以内。

输入: {context}

输出:

"""


Video2IntentionPrompt = """
作为自动驾驶场景视频理解专家，请基于以下的关键要素对于输入的视频片段进行理解，并生成结构化的输出:
要求包含以下几个关键要素：
1.输出代码描述的道路场景：json 字段名称为“道路场景”，输出的内容为当前输入文件描述的道路场景，可能是高速公路路口、城市交叉路口，分合流的路口，环岛等。
2.输出代码中场景的参与制：json 字段名称为“场景参与者”，输出的内容为当前输入文件中场景的主要参与者，包含主车和其他交通参与者，如NPC车辆、行人、自行车，静止物体，VRU等。
3.输出代码中场景的参与者的初始位置：json 字段名称为“初始位置”，输出内容为主要参与者与主车之间的空间关系，如：在主车对向车道20m，左侧右侧车道，前方/后方 100m等
4.输出代码中场景的主要参与者的动作：json 字段名称为“运动方向”，输出内容为当前输入文件中场景的场景参与者的动作描述，如：变道，超车，转弯，紧急制动，行人横穿马路等。
5.输出代码中主车的行驶意图：json 字段名称为“主车意图”，输出内容为当前输入文件中主车的行驶意图，如：左转弯，右转弯，直行，通过路口，避让行人，并入高速，驶出高速等。
6.输出代码中场景的触发条件：json 字段名称为“触发条件”，输出内容为当前输入文件中场景的触发条件，如：当主车与前车距离小于10米时，前车开始紧急制动等。
7.输出代码中的测试场景意图，json 字段名称为“测试意图”，输出内容为当前输入文件中场景的测试意图，如：测试鬼探头，测试车辆切入场景等。
输出的格式为 json 格式，示例如下:
{{
    "道路场景": "...",
    "场景参与者": "...",
    "初始位置": "...",
    "运动方向": "...",
    "主车意图": "...",
    "触发条件": "...",
    "测试意图": "..."
}}
不要生成无关的信息，字数
控制在500字以内。


输出:

"""

MergeIntentionPrompt = """
作为自动驾驶场景视频理解专家，请基于以下的规则对于输入两段json格式的意图进行合并，并生成结构化的输出:
规则包括以下几个关键要素：
1.尽量保留原始josn中的信息。
2.合并不互相冲突的一些信息
3.当输入的信息不一致时，对于触发条件字段和初始位置字段，主要依赖XML的意图，运动方向，道路场景字段主要依赖于video的意图，其他有冲突的字段用参考带数字的信息
输出的格式为 json 格式，示例如下:
{{
    "道路场景": "...",
    "场景参与者": "...",
    "初始位置": "...",
    "运动方向": "...",
    "主车意图": "...",
    "触发条件": "...",
    "测试意图": "..."
}}
不要生成无关的信息，字数
控制在500字以内。

video 意图：{context_video}

XML 意图：{context_xml}

输出:

"""




class IntentionGenerator:
    def __init__(self, agent:OpenAICompatibleAgent):
        self.agent = agent

    def remove_think_tags(self, text):
        import re
        # 使用正则表达式移除 <think> 和 </think> 之间的内容
        if '<think>'  in text:
            return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        elif '</think>'  in text:
            return re.sub(r'.*?</think>', '', text, flags=re.DOTALL)
        return text


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

    async def generate_intention_from_oscfile(self, osc_file_path: str) -> str:
        # model_response = await self.agent.client_simple.models.list()
        # for model in model_response:
        #     print(model.id)
        osc_file_content = ""
        with open(osc_file_path, 'r', encoding='utf-8') as f:
            osc_file_content = f.read()

        message  = Osc2IntentionPrompt.format(context=osc_file_content)
        response = await self.agent.chat(message)
        #remove thinking from response

        if type(response) == dict and 'message' in response:
            response = response['message']
        response = self.remove_think_tags(response)
        # Select the appropriate template based on context
        # import pdb
        # pdb.set_trace()
        if response:
            return response.strip()
        raise ValueError("No applicable template found for the given context.")


    async def generate_intention_from_xmlfile(self, xml_file_path: str) -> str:
        # model_response = await self.agent.client_simple.models.list()
        # for model in model_response:
        #     print(model.id)
        osc_file_content = ""
        with open(xml_file_path, 'r', encoding='utf-8') as f:
            osc_file_content = f.read()

        message  = Osc2IntentionPrompt.format(context=osc_file_content)
        response = await self.agent.chat_simple(message, enable_thinking=True)
        #remove thinking from response

        response = self.remove_think_tags(response)
        # Select the appropriate template based on context
        if response:
            return response.strip()
        raise ValueError("No applicable template found for the given context.")


    async def generate_intention_from_video(self, video_path: str) -> str:
        # model_response = await self.agent.client_simple.models.list()
        # for model in model_response:
        #     print(model.id)

        message  = Video2IntentionPrompt.format()
        response = await self.agent.chat_simple_video(message, video_path)
        #remove thinking from response

        response = self.remove_think_tags(response)
        # Select the appropriate template based on context
        if response:
            return response.strip()
        raise ValueError("No applicable template found for the given context.")

    async def merge_intention(self, video_intention: str, xml_intention: str) -> str:
        # model_response = await self.agent.client_simple.models.list()
        # for model in model_response:
        #     print(model.id)

        message  = MergeIntentionPrompt.format(context_video=video_intention, context_xml=xml_intention)
        response = await self.agent.chat_simple(message, enable_thinking=True)
        #remove thinking from response

        response = self.remove_think_tags(response)
        # Select the appropriate template based on context
        if response:
            return response.strip()
        raise ValueError("No applicable template found for the given context.")

if __name__ == "__main__":
    import asyncio
    from cursor_agent_tools import create_agent, PermissionOptions

    async def main():
        permissions = PermissionOptions(
            yolo_mode=True,
            command_allowlist=["ls", "echo", "git","cat", "cp", "mv", "mkdir","find"],
            delete_file_protection=True
        )

        # Create a Claude agent instance
        agent = create_agent(
            model='remote-holo-model',
            permissions=permissions
        )
        video_path = "/C20545/jeremyj/pro/volkswagen_demo/osc_converter_ui/cursor-agent/CQU/CDA_001.mp4"
        xml_path = video_path.replace(".mp4", ".xosc")
        intentionrewriter = IntentionGenerator(agent)
        intention_video = await intentionrewriter.generate_intention_from_video(video_path)
        print("Generated Intention:", intention_video)
        intention_xml = await intentionrewriter.generate_intention_from_xmlfile(xml_path)
        print("Generated Intention from XML:", intention_xml)
        intention = await intentionrewriter.merge_intention(intention_video, intention_xml)
        print("Generated Merged Intention:", intention)

    asyncio.run(main())