import asyncio
from cursor_agent_tools import create_agent
from cursor_agent_tools import run_agent_interactive

#meta-llama/llama-3.3-70b-instruct:free
#meta-llama/llama-4-maverick:free
#moonshotai/kimi-k2:free
#qwen/qwen3-235b-a22b:free
#qwen/qwen3-coder:free



async def main():

    #openai_api_key = "EMPTY"
    #openai_api_base = "http://221.12.22.162:8888/test/8006/v1"
    #model="holo-model/function-call"

    attention = input("请输入需要实现的意图: ")
    save_name = input("请输入保存的文件路径: ")
    
    #ego_overtake_right.osc

    # Create a Claude agent instance
    agent = create_agent(model='remote-moonshotai/kimi-k2:free')
    #agent = create_agent(model='remote-holo-model/function-call')

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

        initial_query='''基于rag_osc/carla_examples文件夹下的例子写一个{}的dsl代码,
                        注意以下一些常见的问题:
                        1. scenario 的名字必须叫top
                        2. 在osc 文件的最后添加一个回车空行
                        3. 不要使用变量声明和引用。
                        4. 不要使用任意的assert 等断言来判断状态
                        5. 在变量使用前要严格检查是否声明，严格保证先声明后使用.
                        6. postion 只能在开始的时候使用，不能用于最终的位置控制。
                        最终结果保存到当前目录下的{}文件中，不要生成其他文件'''.format(attention,save_name), max_iterations=15,
        agent=agent
        #user_info=user_info,
        # auto_continue=True is the default - agent continues automatically
        # To disable automatic continuation, set auto_continue=False
    )

    
    # "基于rag_osc 文件夹下的例子写一个 ego cut in 的dsl 代码"
    # # Chat with the agent
    # run_agent_interactive(agent, user_info=user_info)
    # response = await agent.chat("基于rag_osc 文件夹下的例子写一个 ego cut in 的dsl 代码", user_info=user_info)
    # print(response)

if __name__ == "__main__":
    asyncio.run(main())