import json
import logging
import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


token = os.getenv('NOTION_BEARER_TOKEN')
assert token is not None
notion_request_headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16",
}

notion_request_payload = {"page_size": 100}

example_page = {
    "object": "page", 
    "id": "162ecd4f-1746-4c30-a7b8-472cc2ab9874", 
    "created_time": "2021-09-12T12:02:00.000Z", 
    "last_edited_time": "2022-06-05T09:44:00.000Z", 
    "created_by": {
        "object": "user", 
        "id": "47c7bf83-0551-44c2-bf2e-60bae3f3a502"
        }, 
    "last_edited_by": {
        "object": "user", 
        "id": "47c7bf83-0551-44c2-bf2e-60bae3f3a502"
        }, 
    "cover": {
        "type": "external", 
        "external": {
            "url": "https://www.notion.so/images/page-cover/nasa_the_blue_marble.jpg"
        }
    }, 
    "icon": {
        "type": "emoji",
        "emoji": "\ud83c\udfe1"
    }, 
    "parent": {
        "type": "workspace", 
        "workspace": True
    }, 
    "archived": False, 
    "properties": {
        "title": {
            "id": "title", 
            "type": "title", 
            "title": [
                {
                    "type": "text", 
                    "text": {"content": "Personal", "link": None}, 
                    "annotations": {
                        "bold": False, 
                        "italic": False, 
                        "strikethrough": False, 
                        "underline": False, 
                        "code": False, 
                        "color": "default"
                        }, 
                    "plain_text": "Personal", 
                    "href": None
                    }
                ]
            }
        }, 
    "url": "https://www.notion.so/Personal-162ecd4f17464c30a7b8472cc2ab9874"
    }

def nullPipe(obj:Any, valIfNull:Any, emptyVal:Any=None):
    if emptyVal is None:
        if obj is None:
            return valIfNull
        else:
            return obj
    else:
        if obj == emptyVal:
            return valIfNull
        else:
            return obj
        
_notion_page_types = [
    'page',
    'db_page',
    'db'
]

_notion_object_types = [
    *_notion_page_types,
    'block',
    'property',
]

_parsed_notion_page_types = set()

def _page_obj_is_page(page_obj:dict) -> bool:
    return page_obj["object"] == 'page' and 'title' in page_obj["properties"] and 'title' in page_obj["properties"]["title"]
def _page_obj_is_db(page_obj:dict) -> bool:
    return page_obj["object"] == 'database'
def _page_obj_is_db_page(page_obj:dict) -> bool:
    return page_obj["object"] == 'page' and bool(next((k for k in page_obj["properties"].keys(
            ) if page_obj["properties"][k]['type'] == 'title'),False))

def _get_page_name_from_page_json(page_obj:dict) -> str:
    processing = ''
    try:
        if _page_obj_is_db(page_obj):
            processing = 'db'
            page_name = page_obj["properties"][next((k for k in page_obj["properties"].keys(
            ) if page_obj["properties"][k]['type'] == 'title'))]['title']
            _parsed_notion_page_types.add('db')
            processing += ' error -> [0]["text"]["content"]'
            return nullPipe(
                list(page_name),
                valIfNull=[{'text': {'content': "Undefined"}}],
                emptyVal=[]
            )[0]["text"]["content"]
        
        if _page_obj_is_page(page_obj):
            processing = 'page'
            page_name = page_obj["properties"]["title"]["title"]
            _parsed_notion_page_types.add('page')
            processing += ' error -> [0]["text"]["content"]'
            return nullPipe(
                list(page_name),
                valIfNull=[{'text': {'content': "Undefined"}}],
                emptyVal=[]
            )[0]["text"]["content"]
        if _page_obj_is_db_page(page_obj):
            processing = 'db_page'
            if "Name" in page_obj["properties"] and page_obj["properties"]["Name"]['type'] == 'title':
                page_name = page_obj["properties"]["Name"]["title"]
            else:
                page_name = page_obj["properties"][
                    next((k for k in page_obj["properties"].keys() if page_obj["properties"][k]['type'] == 'title'))
                ]['title']
            _parsed_notion_page_types.add('db_page')
            processing += ' error -> [0]["text"]["content"]'
            return nullPipe(
                list(page_name),
                valIfNull=[{'text': {'content': "Undefined"}}],
                emptyVal=[]
            )[0]["text"]["content"]
        
        
        # nullPipe(
        #     ((page_obj["properties"]["title"] if 'title' in page_obj["properties"] else page_obj["properties"]["Name"] if "Name" in page_obj["properties"] else page_obj["properties"][next((k for k in page_obj["properties"].keys() if page_obj["properties"][k]['type'] == 'title'))]) if page_obj["object"] == 'page' else page_obj)["title"],
        #     valIfNull=[{'text': {'content': "Undefined"}}],
        #     emptyVal=[]
        # )[0]["text"]["content"]
    except Exception as e:
        logging.warn(e)
        page_types = '\',\''.join(_parsed_notion_page_types)
        return f'{type(e).__name__} processing {processing}. Already parsed notion objs [\'{page_types}\'];'
    return 'Undefined page type'
    

def getRecentPages(payload:dict[str,Any], headers:dict[str,str]):
    readUrl = f"https://api.notion.com/v1/search"

    res = requests.request("POST", readUrl, json=payload, headers=headers)
    data:dict|list = res.json()
    print(res.status_code)
    # print(res.text)
    with open('./page_list_pag1_cache.json', 'w') as f:
        json.dump(data, f)
    full_list = []
    full_list += data['results']
    while data['has_more']:
        res = requests.request("POST", readUrl, json={**payload, 'start_cursor': data['next_cursor']}, headers=headers)
        data = res.json()
        full_list += data['results']
    with open('./page_list_full_cache.json', 'w') as f:
        json.dump(full_list, f)
    page_names = ['No Notion Pages returned']
    try:
        page_names:list[str] = [
            _get_page_name_from_page_json(page_obj)
            for page_obj in full_list
        ]
    except Exception as e:
        logging.warn('Notion properties objects have changed structure')
        page_names = [str(e)]
    return (data, page_names)
