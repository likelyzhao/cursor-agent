import asyncio
import re
import os
import shutil
from oslk import oslk_generator

def slugify(text: str) -> str:
    """简单把中文/空格/特殊字符转为文件名友好格式"""
    # 把空白改为下划线，去掉不安全字符
    text = re.sub(r'\s+', '_', text.strip())
    text = re.sub(r'[^\w\u4e00-\u9fff_-]', '', text)  # 保留字母数字中文下划线和短横
    # 可选：把中文保留原样或转为拼音，这里保留原样
    return text

async def _worker(sem: asyncio.Semaphore, initial_query: str, save_name: str):
    async with sem:
        print(f"Start: {initial_query} -> {save_name}")
        try:
            await oslk_generator(initial_query, save_name)
            #mkdir and cp the file and conversation_history.json to a folder named save_name without .oslk
            folder_name = save_name[:-5]  # Remove .oslk extension
            os.makedirs(folder_name, exist_ok=True)
            shutil.copy(save_name, folder_name)
            shutil.copy("conversation_history.json", folder_name)

            print(f"Done:  {save_name}")
        except Exception as e:
            print(f"Error for {save_name}: {e}")

async def run_batch(items, concurrency=2):
    sem = asyncio.Semaphore(concurrency)
    tasks = [
        asyncio.create_task(_worker(sem, q, name))
        for q, name in items
    ]
    await asyncio.gather(*tasks)

def build_items_from_list(queries):
    """
    从一个字符串列表生成 (initial_query, save_name) 对列表。
    如有需要可在这里做更多的“处理数据”逻辑。
    """
    items = []
    for q, name in queries.items():
        fname = slugify(name)
        if not fname:
            continue
        # 统一扩展名为 .oslk
        if not fname.lower().endswith('.oslk'):
            fname = f"{fname}.oslk"
        items.append((q, fname))
    return items

def main():
    # 示例输入列表：可以替换为从文件/数据库读取
    queries = {
        "前车急刹至停止，ego 2 m 内刹停":"FullStop",
        "前车从 100 km/h 降速至 60 km/h，ego 往左变道超车":"RapidDecel",
        "插入车急刹，ego 减速保持车距":"CutInBrake",
        "前车突然遇到障碍减速后加速，ego 同步":"BrakeFollow",
        "前车连续三次急停，ego 每次保持足够车距制动":"MultiStop"
    }



# 1、FullStop – 前车急刹至停止，ego 2 m 内刹停。
# 2、RapidDecel – 前车从 100 km/h 降速至 60 km/h，ego 往左变道超车。
# 3、CutInBrake – 插入车急刹，ego 减速保持车距。
# 4、BrakeFollow – 前车突然遇到障碍减速后加速，ego 同步。
# 5、MultiStop – 前车连续三次急停，ego 每次保持足够车距制动。



    items = build_items_from_list(queries)
    # 可以通过修改concurrency控制并发量（注意模型/代理资源）
    concurrency = 1  # 推荐先用 1 或 2，避免并发占满远端模型资源
    asyncio.run(run_batch(items, concurrency=concurrency))

if __name__ == "__main__":
    main()