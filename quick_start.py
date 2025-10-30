import asyncio
from cursor_agent_tools import create_agent
from cursor_agent_tools import run_agent_interactive

#meta-llama/llama-3.3-70b-instruct:free
#meta-llama/llama-4-maverick:free
#moonshotai/kimi-k2:free
#qwen/qwen3-235b-a22b:free
#qwen/qwen3-coder:free

#场景开始时，主车以指定速度在车道上行驶，前方有前车保持2秒时距。3秒后激活ALKS控制器。当前车接近阻挡物（距离小于50m）时，前车会执行cut-out操作，以正弦曲线方式变道至相邻车道（横向速度不超过2m/s）。主车需要识别这一突发情况并做出适当反应。场景在预计主车到达阻挡物位置后10秒结束。
#cut_out_fully_blocking.osc

async def main():

    #openai_api_key = "EMPTY"
    #openai_api_base = "http://221.12.22.162:8888/test/8006/v1"
    #model="holo-model/function-call"

    #attention = input("请输入需要实现的意图: ")
    #save_name = input("请输入保存的文件路径: ")

    attention = 'ego 连续超车'
    save_name = 'ego_overtake_multiple_qwennext.oslk'

    #ego_overtake_right.osc

    # Create a Claude agent instance
    agent = create_agent(model='remote-holo-model/function-call')
    # agent = create_agent(model='remote-functioncall/qwen3-next')
    # agent = create_agent(model='remote-openai/function-call')

    agent.register_default_tools()
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
                        最终结果保存到当前目录下的{}文件中，不要生成其他文件'''.format(attention,save_name), max_iterations=15,
        agent=agent
        #user_info=user_info,
        # auto_continue=True is the default - agent continues automatically
        # To disable automatic continuation, set auto_continue=False
    )


if __name__ == "__main__":
    asyncio.run(main())