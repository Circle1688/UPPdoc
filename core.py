import os

from PySide6.QtCore import *
from openai import AsyncOpenAI
from config import load_config
import json
from markdown_func import *
import aiofiles
import asyncio

client = AsyncOpenAI(
    api_key=load_config()['api_key'],
    base_url="https://api.moonshot.cn/v1",
)

class GenerateThread(QThread):
    finished = Signal(str)
    def run(self):
        results = asyncio.run(run_multi())
        markdowns = []
        for result in results:
            markdowns += generate_markdown(result)
        categorized_dict = build_hierarchy(markdowns)
        markdown_output = hierarchy_to_markdown(categorized_dict)
        self.finished.emit(markdown_output)

async def run_multi():
    config = load_config()
    h_files = find_h_files(config['search_path'])

    tasks = [get_json(h_file) for h_file in h_files]

    results = await asyncio.gather(*tasks)
    return results

def find_h_files(directory):
    h_files = []  # 存储.h文件的绝对路径
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.h'):
                absolute_path = os.path.abspath(os.path.join(root, file))
                h_files.append(absolute_path)
    return h_files

async def get_json(filename):
    async with aiofiles.open(filename, 'r', encoding='utf8') as f:
        h_content = await f.read()

    content = "代码\n```[header]```\n注意不要其他函数，只要UFUNCTION标记的函数，填到以下的json里，注意参数的描述要用中文\n```[json]```\n请严格按照json格式输出"
    json_t = {
        "ufunctions":[
            {
                "classname":"",
                "displayname":"",
                "description":"",
                "is_static": True,
                "is_blueprintAsyncActionBase": False,
                "category":"",
                "input_params":[
                    {
                        "name":"",
                        "type":"",
                        "description":""
                    }
                ],
                "output_params":[
                    {
                        "name":"OnSuccess",
                        "type":"FCreateTextureDelegate",
                        "description":""
                    }
                ],
                "delegate_params":[
                    {
                        "name":"OutTexture",
                        "type":"UTexture2D*",
                        "description":""
                    }
                ]
            }
        ]
    }

    content = content.replace("[header]", h_content)
    content = content.replace("[json]", json.dumps(json_t))


    completion = await client.chat.completions.create(
        model="moonshot-v1-32k",
        messages=[
            {
                "role": "system",
                "content": "你是一个UE5 c++专家，你将从以下ue5 c++代码中找出所有UFUNCTION标记的函数，并在一个 JSON 对象中输出。",
            },
            {
                "role": "user",
                "content": content,
            },
            {
                "role": "assistant",
                "content": "{",
                "partial": True
            },
        ],
        temperature=0.3,
        # response_format={"type": "json_object"},
        max_tokens=4096
    )

    result = '{'+completion.choices[0].message.content
    # print(result)
    # if result.startswith("```json") and result.endswith("```"):
    #     result = result.replace("```json", "")
    #     result = result.replace("```", "")
    #     result = json.loads(result)
    #     return result
    # else:
    #     result = json.loads(result)
    #     return result
    return json.loads(result)
