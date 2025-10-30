from pathlib import Path
import sys
parent_dir = str(Path(__file__).parent.parent.parent.absolute())
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    
import asyncio
from cursor_agent_tools import create_agent, run_agent_interactive
from intention import IntentionGenerator

async def oslk_generator(initial_query: str, save_name: str):

    #attention = 'ego 连续超车'
    #save_name = 'ego_overtake_multiple_qwennext.oslk'

    #ego_overtake_right.osc

    # Create a Claude agent instance
    agent = create_agent(model='remote-holo-model/function-call')
    intentionrewriter = IntentionGenerator(agent)
    intention = await intentionrewriter.generate_intention(initial_query)
    print("Generated Intention:", intention)
    agent.register_default_tools()
    # agent = create_agent(model='remote-functioncall/qwen3-next')
    # agent = create_agent(model='remote-openai/function-call')
    # query = '''基于rag_osc/carla_examples文件夹下的例子写一个{}的dsl代码,
    #                 注意以下一些常见的问题:
    #                 1. scenario 的名字必须叫top
    #                 2. 在osc 文件的最后添加一个'\n'的空行
    #                 3. 不要使用变量声明和引用。
    #                 4. 不要使用任意的assert 等断言来判断状态
    #                 5. 在变量使用前要严格检查是否声明，严格保证先声明后使用.
    #                 6. postion 只能在开始的时候使用，不能用于最终的位置控制。
    #                 最终结果保存到当前目录下的{}文件中，不要生成其他文件'''.format(attention,save_name)
    # print(query)


    await run_agent_interactive(
        # model='claude-3-5-sonnet-latest',

        initial_query='''基于rag_osc/oslk_example 文件夹下的例子写一个{}的oslk代码,
                        注意以下一些常见的问题:
                        1. oslk 生成的使用到的scenarios在rag_osc/mini_sc_scenarios 下
                        2. oslk 文件的格式和osc 文件的格式不一样
                        3. 如果需要用到scenarios在 rag_osc/mini_sc_scenarios 里面没有，需要自己创建一个scenarios
                        4. oslk 文件是一个json格式，请保证文件的格式正确。
                        最终结果保存到当前目录下的{}文件中，不要生成其他文件'''.format(intention, save_name), max_iterations=15,
        agent=agent
        #user_info=user_info,
        # auto_continue=True is the default - agent continues automatically
        # To disable automatic continuation, set auto_continue=False
    )