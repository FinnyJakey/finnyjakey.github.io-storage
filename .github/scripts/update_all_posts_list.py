import os
import json
from datetime import datetime
import pytz

categories_dir = '../../categories'
kst = pytz.timezone('Asia/Seoul')

# if it has no posts directory or posts_list.json, make one and give it []
for subdir in os.listdir(categories_dir):
    subdir_path = os.path.join(categories_dir, subdir)

    if not os.path.isdir(subdir_path):
        continue

    posts_list_file = os.path.join(subdir_path, 'posts_list.json')

    if not os.path.isfile(posts_list_file):
        with open(posts_list_file, 'w') as f:
            json.dump([], f, indent=2)

    posts_dir = os.path.join(subdir_path, 'posts')

    if not os.path.exists(posts_dir):
        with open(posts_list_file, 'w') as f:
            json.dump([], f, indent=2)

# posts_list.json Update
for subdir in os.listdir(categories_dir):
    subdir_path = os.path.join(categories_dir, subdir)

    if not os.path.isdir(subdir_path):
        continue

    posts_list_file = os.path.join(subdir_path, 'posts_list.json')

    with open(posts_list_file, 'r') as f:
        posts_list_data = json.load(f)

    posts_dir = os.path.join(subdir_path, 'posts')

    if not os.path.exists(posts_dir):
        # os.makedirs(posts_dir)
        continue

    posts = [f for f in os.listdir(posts_dir) if f.endswith('.md')]

    for data in posts_list_data:
        data_path = f'{data["path"].split("/")[1].removesuffix(".html")}.md'

        if data_path not in posts:
            posts_list_data.remove(data)

    for post in posts:
        if post not in [f'{item["path"].split("/")[1].removesuffix(".html")}.md' for item in posts_list_data]:
            now = datetime.now(kst)

            posts_list_data.append(
                {
                    "title": post.removesuffix(".md"),
                    "description": "-",
                    "path": f'{subdir}/{post.removesuffix(".md")}.html',
                    "date": now.strftime("%Y.%m.%d %H:%M")
                }
            )

    with open(posts_list_file, 'w') as f:
        json.dump(posts_list_data, f, indent=2)
