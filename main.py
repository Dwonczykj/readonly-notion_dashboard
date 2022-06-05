import json
import os
from typing import Any

import requests

token = "secret_DW43FBbmZ802ktq7wYPgId3Mw9vtHwfwE08iE85x2EI"

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16",
}

payload = {"page_size": 100}

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

def getRecentPages(payload:dict[str,Any], headers:dict[str,str]):
    readUrl = f"https://api.notion.com/v1/search"

    res = requests.request("POST", readUrl, json=payload, headers=headers)
    data = res.json()
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
    page_names = [nullPipe(((page_obj["properties"]["title"] if 'title' in page_obj["properties"] else page_obj["properties"]["Name"] if "Name" in page_obj["properties"] else page_obj["properties"][next((k for k in page_obj["properties"].keys() if page_obj["properties"][k]['type'] == 'title'))]) if page_obj["object"] == 'page' else page_obj)["title"], valIfNull=[{'text': {'content': "Undefined"}}], emptyVal=[])[0]["text"]["content"] for page_obj in full_list]
    return data

query = ""
filter = ""
getRecentPages(
    payload={
        **payload,
        **({
            "query": "",
            } if query else {}),
        **({
            "filter": "",
            } if filter else {}),
        },
    headers=headers
    )
