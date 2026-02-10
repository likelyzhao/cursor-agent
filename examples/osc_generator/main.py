import asyncio
import re
import os
import shutil
from oslk import oslk_generator
from osc import osc_generator, osc_generator_from_video


genarateion_path = "generated_scenarios"
os.makedirs(genarateion_path, exist_ok=True)

def slugify(text: str) -> str:
    """简单把中文/空格/特殊字符转为文件名友好格式"""
    # 把空白改为下划线，去掉不安全字符
    text = re.sub(r'\s+', '_', text.strip())
    text = re.sub(r'[^\w\u4e00-\u9fff_-]', '', text)  # 保留字母数字中文下划线和短横
    # 可选：把中文保留原样或转为拼音，这里保留原样
    return text

def force_move(src, dst):
    """
    强制移动文件或目录
    如果目标已存在，则先删除再移动
    """
    # 如果目标存在，删除它
    if os.path.exists(dst):
        if os.path.isdir(dst):
            shutil.rmtree(dst)  # 删除目录
            print(f"Removed existing directory: {dst}")
        else:
            os.remove(dst)  # 删除文件
            print(f"Removed existing file: {dst}")
    
    # 移动源到目标位置
    return shutil.move(src, dst)


async def _worker(sem: asyncio.Semaphore, initial_query: str, save_name: str):
    async with sem:
        print(f"Start: {initial_query} -> {save_name}")
        try:
            # await oslk_generator(initial_query, save_name)
            #await osc_generator(initial_query, save_name)
            await osc_generator_from_video(initial_query, save_name)
            #mkdir and cp the file and conversation_history.json to a folder named save_name without .osc
            folder_name = os.path.join(genarateion_path, save_name[:-4])  # Remove .osc extension
            if os.path.exists(folder_name):
                if os.path.isdir(folder_name):
                    shutil.rmtree(folder_name)  # 删除目录
                else:
                    os.remove(folder_name)  # 删除文件
            os.makedirs(folder_name, exist_ok=True)
            force_move(save_name, os.path.join(folder_name,save_name))
            force_move("conversation_history.json", os.path.join(folder_name,"conversation_history.json"))
            force_move(save_name.replace(".osc", ".json"), os.path.join(folder_name,save_name.replace(".osc", ".json")))
            shutil.copy(initial_query, os.path.join(folder_name,os.path.basename(initial_query)))
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
        # 统一扩展名为 .osc
        if not fname.lower().endswith('.osc'):
            fname = f"{fname}.osc"
        items.append((q, fname))
    return items

def main_query():
    # 示例输入列表：可以替换为从文件/数据库读取
    queries = {
        "前车急刹至停止，ego 2 m 内刹停":"FullStop",
        "前车从 100 km/h 降速至 60 km/h，ego 往左变道超车":"RapidDecel",
        "插入车急刹，ego 减速保持车距":"CutInBrake",
        "前车突然遇到障碍减速后加速，ego 同步":"BrakeFollow",
        "前车连续三次急停，ego 每次保持足够车距制动":"MultiStop"
    }


    items = build_items_from_list(queries)
    # 可以通过修改concurrency控制并发量（注意模型/代理资源）
    concurrency = 1  # 推荐先用 1 或 2，避免并发占满远端模型资源
    asyncio.run(run_batch(items, concurrency=concurrency))

def main():
    import os 
    items = []
    video_path = "/C20545/jeremyj/pro/volkswagen_demo/osc_converter_ui/cursor-agent/CQU"
    for file in os.listdir(video_path):
        if file.endswith(".mp4"):
            filename = os.path.splitext(file)[0]

            save_folder_name = os.path.join(genarateion_path, filename)
            if os.path.exists(save_folder_name):
                print("Folder already exists, skipping: ", save_folder_name)
            else:
                video_file_path = os.path.join(video_path, file)
                save_name = f"{filename}.osc"
                print(f"Processing video: {file} -> {save_name}")
                items.append((video_file_path, save_name))
    
    asyncio.run(run_batch(items, concurrency=1))

if __name__ == "__main__":
    main()