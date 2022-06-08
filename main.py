from notion import getRecentPages, notion_request_payload, notion_request_headers

if __name__ == '__main__':
    query = ""
    filter = ""

    (data, page_names) = getRecentPages(
        payload={
            **notion_request_payload,
            **({
                "query": "",
                } if query else {}),
            **({
                "filter": "",
                } if filter else {}),
            },
        headers=notion_request_headers
        )
    
    print(page_names)
