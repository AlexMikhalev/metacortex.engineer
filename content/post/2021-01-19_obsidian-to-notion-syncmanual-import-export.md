---
title: "Obsidian to Notion sync — manual import export"
author: "Alex Mikhalev"
date: 2021-01-19T13:51:02.729Z
lastmod: 2021-06-11T10:00:10+01:00

description: ""

subtitle: ""




aliases:
- "/obsidian-to-notion-sync-manual-import-export-49ad429a6533"

---

If you are a developer or engineer you normally have a multiple enviroments: vs code to work on a code, Typora to edit markdown file and then Obsidian/Roam Research to take your notes and Notion (Coda) or Confluence to share it with your team. It’s it confusing?

In debate which is the better tool, my answer is — the one which allows you to integrate it with another. This is why I prefer Obsidian over RoamResearch, plan markdown I can import into Notion and then share with my collegues and then export back. Here is how:

```
pip install notion md2notion
```

Get notion token as per guidance in [Unoficcial Notion Python Client](https://github.com/jamalex/notion-py) and create a fresh workspace for experiment (mine is called Obsidian World), get workspace URL by clicking on Share button and “Copy link”

```
python3 -m md2notion notion_token https://notion.so/workspace_url  World/*.md
```

which is times out for me or throws 500 error at the moment. There is an official Markdown import, which can be used instead, but it fails for me too :(

Fetching data from notion to markdown is easier via this [gist](https://gist.github.com/AlexMikhalev/f21585a6a3138934f8a7adbf6a905af6) you need to export NOTIN_TOKEN and `export NOTION_ROOT_PAGE_ID=https://notion.so/workspace_url` and it will fetch clean new obsidian world from Notion Workspace. Be careful with existing Obsidian world - the script will wipe a destination folder.

* * *
Written on January 19, 2021 by Alex Mikhalev.

Originally published on [Medium](https://medium.com/@alexmikhalev/obsidian-to-notion-sync-manual-import-export-49ad429a6533)
