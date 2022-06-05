# Read-Only Notion Dashboard
This project connects to a Notion Workspace (defaults to the user's default workspace) and exposes a list of recently updated pages in the user's workspace.

## Requirements
1. Connect a notion integration [linked here](https://www.notion.so/my-integrations) and call it whatever you like i.e. (readonly-notion-dashboard)
   1. Set to an Internal-Integration for the notion integration type
   2. Give the integration permissions:
      1. Read Content
      2. No user information
2. Then navigate to each parent page within notion that you want to share with the integration you created in the step above.
   1. Navigate to the page in Notion
   2. Select Share from the header
   3. Share with the integration you created above.
3. Finally, run the express server to host the webpage and view the list of recently accessed pages. Alternatively port the code into your own python project.

## References
- [My Notion Integrations](https://www.notion.so/my-integrations)
- [Search Endpoint Docs](https://developers.notion.com/reference/post-search)
- [Pagination Docs](https://developers.notion.com/reference/pagination)