from pathlib import Path
import sys
parent_dir = str(Path(__file__).parent.parent.parent.absolute())
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    
import asyncio
from cursor_agent_tools import create_agent, run_agent_interactive
from intention import IntentionGenerator
from cursor_agent_tools import PermissionOptions

async def osc_generator(initial_query: str, save_name: str):

    #attention = 'ego 连续超车'
    #save_name = 'ego_overtake_multiple_qwennext.oslk'

    #ego_overtake_right.osc
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
    intentionrewriter = IntentionGenerator(agent)
    intention = await intentionrewriter.generate_intention(initial_query)
    print("Generated Intention:", intention)
    agent.register_default_tools()

    await run_agent_interactive(
        # model='claude-3-5-sonnet-latest',
        initial_query='''基于rag_osc/standard_test_scenarios 文件夹下的例子，写一个测试意图为{}的dsl代码,
                        注意以下一些常见的问题:
                        1. 只生成一个osc文件就可以了，千万不要生成多个osc文件；
                        2. 注释用 #，而不是 //，注释不要用中文，注释请使用英文；
                        3. 开头使用 import 导入osc文件，不要使用 include 导入osc文件；
                        4. 使用 extend test_config: 来导入地图文件；
                        5. 写文件使用create_file工具, 注意create_file的路径传参用file_path参数，不要多余explanation参数;
                        6. 生成了osc文件后就停止，不要多余操作；
                        7. 如果需要用到新的scenarios, 请参考在 rag_osc/basic_scenarios下面的内容，如有需要需要自己创建一个scenarios
                        最终结果保存到当前目录下的{}文件中，不要生成其他文件'''.format(intention, save_name), max_iterations=15,
        agent=agent
        #user_info=user_info,
        # auto_continue=True is the default - agent continues automatically
        # To disable automatic continuation, set auto_continue=False
    )

async def osc_generator_from_video(video_path: str, save_name: str):

    #attention = 'ego 连续超车'
    #save_name = 'ego_overtake_multiple_qwennext.oslk'

    #ego_overtake_right.osc
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
    intentionrewriter = IntentionGenerator(agent)
    xml_path = video_path.replace(".mp4", ".xosc")
    intention_video = await intentionrewriter.generate_intention_from_video(video_path)
    print("Generated Intention:", intention_video)
    intention_xml = await intentionrewriter.generate_intention_from_xmlfile(xml_path)
    print("Generated Intention from XML:", intention_xml)
    intention = await intentionrewriter.merge_intention(intention_video, intention_xml)
    print("Generated Merged Intention:", intention)
    agent.register_default_tools()
    with open(save_name.replace(".osc", ".json"), "w") as f:
        f.write(intention)

    await run_agent_interactive(
        # model='claude-3-5-sonnet-latest',
        initial_query='''基于rag_osc/standard_test_scenarios 文件夹下的例子，写一个测试意图为{}的dsl代码,
                        注意以下一些常见的问题:
                        1. 只生成一个osc文件就可以了，千万不要生成多个osc文件；
                        2. 注释用 #，而不是 //，注释不要用中文，注释请使用英文；
                        3. 开头使用 import 导入osc文件，不要使用 include 导入osc文件；
                        4. 使用 extend test_config: 来导入地图文件；
                        5. 写文件使用create_file工具, 注意create_file的路径传参用file_path参数，不要多余explanation参数;
                        6. 生成了osc文件后就停止，不要多余操作；
                        7. 如果需要用到新的scenarios, 请参考在 rag_osc/basic_scenarios下面的内容，如有需要需要自己创建一个scenarios
                        最终结果保存到当前目录下的{}文件中，不要生成其他文件'''.format(intention, save_name), max_iterations=15,
        agent=agent
        #user_info=user_info,
        # auto_continue=True is the default - agent continues automatically
        # To disable automatic continuation, set auto_continue=False
    )