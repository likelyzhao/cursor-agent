from openai import OpenAI
from cursor_agent_tools import create_agent

api_key = "sk-AQQ6hPsmaCrgf5ZT48952e9102F847A6A8951aC19076Ef10"
#api_key = "sk-8ux2BRt63lq1T93w080b55Bf433f422f93E512D83f77016b"
base_url = "https://api.zjuqx.cn/v1/"  # 确保URL是正确的

base_url="http://221.12.22.162:8888/test/8006/v1"
api_key="EMPTY"
model_id= "holo-model/function-call"

# R6000 coder model info
base_url = "http://10.160.199.235:8007/v1/"
api_key="EMPTY"
model_id= "holo-model"

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

import asyncio


#米点皴，雨点皴
#牛毛皴， 披麻皴，解索皴，乱柴皴，荷叶皴，折带皴
#斧劈皴，弹涡皴，拖泥带水皴，卷云皴、鬼面皴、马牙皴


async def main_test_our_model():
    try:
        # moddify env variable to test our model
        id = model_id
        agent = create_agent(model='remote-'+id)
        agent.register_default_tools()
        response = await agent.chat("你好",)
        print(response)
        if 'error' not in response["message"]:
            print("can use", id)
    # completion = client.chat.completions.create(
    #     model=model.id,
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {
    #             "role": "user",
    #             "content": "你好"
    #         }
    #     ],
    #     tools=["search"],
    # )

    #print(response.choices[0].message.content)
    except Exception as e:
        print(id)
        print(f"Error: {e}")


async def main():

    # 列出可用模型
    models_response = client.models.list()

    # 打印模型列表
    for model in models_response.data:
        if 'free' in model.id:
            try:
                model.id = "holo-model/function-call"
                agent = create_agent(model='remote-'+model.id)
                agent.register_default_tools()
                response = await agent.chat("你好",)
                print(response)
                if 'error' not in response["message"]:
                    print("can use", model.id)
            # completion = client.chat.completions.create(
            #     model=model.id,
            #     messages=[
            #         {"role": "system", "content": "You are a helpful assistant."},
            #         {
            #             "role": "user",
            #             "content": "你好"
            #         }
            #     ],
            #     tools=["search"],
            # )

            #print(response.choices[0].message.content)
            except Exception as e:
                print(model.id)
                print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main_test_our_model())