import json
import os
import shutil
import subprocess
from datetime import datetime
import markdown

GITHUB_TOKEN = os.getenv('TARGET_REPO_TOKEN')
REPO_URL = 'github.com/FinnyJakey/finnyjakey.github.io.git'
# REPO_URL = 'https://github.com/FinnyJakey/finnyjakey.github.io.git'
REPO_DIR = 'finnyjakey.github.io'


def run_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Command failed with error: {result.stderr}")
    return result.stdout


def make_list_index(category, datas):
    sorted_datas = sorted(datas, key=lambda x: datetime.strptime(x['date'], "%Y.%m.%d %H:%M"), reverse=True)

    li = ""

    for data in sorted_datas:
        li += f"""<li class="flex flex-col gap-1">
                        <div class="flex flex-row items-center justify-between">
                            <a href="{data["path"].split('/')[1]}">
                                <span class="text-[#0000EE] font-medium underline underline-offset-4">
                                    {data["title"]}
                                </span>
                            </a>
                            <span class="text-xs text-[#09090B] tracking-tight">
                                {data["date"]}
                            </span>
                        </div>
                        <span class="text-sm text-[#09090B]">
                            {data["description"]}
                        </span>
                    </li>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="../tailwind.config.js"></script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap"
          rel="stylesheet">

    <link rel="icon" type="image/x-icon" href="../favicon.ico">
    <title>FinnyJakey's Dev Blog</title>
</head>
<body class="min-h-screen bg-white antialiased font-jetbrainsMono text-[0.9rem] max-w-lg">
    <div class="flex min-h-screen flex-col py-8">
        <main class="container flex flex-col px-8">
            <article class="pt-6">
                <h2 class="font-jetbrainsMono text-lg tracking-tighter">
                    {category}
                </h2>
                <ul class="space-y-4 py-4">
                    {li}
                </ul>
            </article>
        </main>
    </div>
</body>
</html>"""


def make_index(header, categories, miscellaneous):
    header_element = ""
    for header_data in header:
        header_element += f"""<a class="text-[#0000EE] underline underline-offset-4" href="{header_data['link']}" target="_blank">
                {header_data['title']}
            </a>"""
        if header_data != header[-1]:
            header_element += """
            /
            """

    def status_element(category_data):
        if "status" not in category_data or category_data["status"] is None:
            return ""
        else:
            return f"""-
            <span class="text-xs text-[#09090B] tracking-tight underline underline-offset-4">
                {category_data["status"]}
            </span>"""

    categories_element = ""
    for categories_data in categories:
        categories_element += f"""<li class="flex flex-col items-start gap-1">
                    <a class="flex items-center gap-1.5" href="{categories_data['path']}">
                        <span class="text-[#0000EE] font-medium underline underline-offset-4">
                            {categories_data['title']}
                        </span>
                        {status_element(categories_data)}
                    </a>
                <span class="text-sm text-[#09090B]">
                   {categories_data['description']}
                </span>
            </li>
            """

    miscellaneous_element = ""
    if miscellaneous:
        sorted_miscellaneous = sorted(miscellaneous, key=lambda x: datetime.strptime(x['date'], "%Y.%m.%d %H:%M"), reverse=True)
        miscellaneous_element += """<article class="pt-6">
            <h2 class="font-jetbrainsMono text-lg tracking-tighter"
                >miscellaneous
            </h2>
            <ul class="space-y-4 py-4">
            """

        for miscellaneous_data in sorted_miscellaneous:
            miscellaneous_element += f"""<li class="flex flex-col gap-1">
                <div class="flex flex-row items-center justify-between">
                    <a href="{miscellaneous_data['path']}">
                        <span class="text-[#0000EE] font-medium underline underline-offset-4">
                            {miscellaneous_data['title']}
                        </span>
                    </a>
                    <span class="text-xs text-[#09090B] tracking-tight">
                        {miscellaneous_data['date']}
                    </span>
                </div>
                <span class="text-sm text-[#09090B]">
                    {miscellaneous_data['description']}
                </span>
            </li>
            """

        miscellaneous_element += """</ul>
        </article>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <script src="https://cdn.tailwindcss.com"></script>
    <script src="tailwind.config.js"></script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap"
          rel="stylesheet">

    <link rel="icon" type="image/x-icon" href="favicon.ico">

    <title>FinnyJakey's Dev Blog</title>
</head>

<body class="min-h-screen bg-white antialiased font-jetbrainsMono text-[0.9rem] max-w-lg">
<div class="flex min-h-screen flex-col py-8">
    <header class="container px-8">
        <div class="flex flex-wrap items-center gap-2 font-medium">
            {header_element}
        </div>
    </header>
    <main class="container flex flex-col px-8" id="main">
        <article class="pt-6">
            <h2 class="font-jetbrainsMono text-lg tracking-tighter">
                categories
            </h2>
            <ul class="space-y-4 py-4">
                {categories_element}
            </ul>
        </article>
        {miscellaneous_element}
    </main>
</div>
</body>

</html>"""


def make_html(text):
    content_html = markdown.markdown(text, extensions=['extra', 'nl2br'])

    return f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="../tailwind.config.js"></script>

        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap"
              rel="stylesheet">

        <link rel="icon" type="image/x-icon" href="../favicon.ico">
        
        <link rel="stylesheet" href="../github-markdown-light.css">
        
        <title>FinnyJakey's Dev Blog</title>
    </head>
    <body class="markdown-body min-h-screen bg-white antialiased font-jetbrainsMono text-[0.9rem] max-w-2xl">
        <div class="flex min-h-screen flex-col py-8">
            <main class="container flex flex-col px-8">
                {content_html}
            </main>
        </div>
    </body>
    </html>"""


# Categories Dir
categories_dir = 'categories'

# Git 설정
run_command(f'git config --global user.name "github-actions[bot]"')
run_command(f'git config --global user.email "github-actions[bot]@users.noreply.github.com"')

# github.io 클론
if os.path.exists(REPO_DIR):
    run_command(f'cd {REPO_DIR} && git pull')
else:
    run_command(f'git clone https://{GITHUB_TOKEN}@{REPO_URL} {REPO_DIR}')

# 0. [html] -> index.html 제거 -> header_links.json, categories/categories_info.json, categories/miscellaneous/posts_list.json -> index.html 생성
os.remove(f'{REPO_DIR}/index.html')

with open('header_links.json', 'r') as f:
    header_links_data = json.load(f)

categories_info_path = os.path.join(categories_dir, 'categories_info.json')
with open(categories_info_path, 'r') as f:
    categories_info_data = json.load(f)

miscellaneous_posts_list_path = os.path.join(categories_dir, 'miscellaneous/posts_list.json')
with open(miscellaneous_posts_list_path, 'r') as f:
    miscellaneous_posts_list_data = json.load(f)

main_index = os.path.join(REPO_DIR, 'index.html')
with open(main_index, 'w') as f:
    f.write(make_index(header_links_data, categories_info_data, miscellaneous_posts_list_data))


# 1. [html] -> 모든 디렉토리 제거
for subdir in os.listdir(REPO_DIR):
    subdir_path = os.path.join(REPO_DIR, subdir)

    if not os.path.isdir(subdir_path) or subdir == '.git':
        continue

    shutil.rmtree(subdir_path)

# 2. [storage] -> [categories] -> all directories -> posts_list.json 순회 -> [html/[slug]] index.html 생성
for subdir in os.listdir(categories_dir):
    subdir_path = os.path.join(categories_dir, subdir)

    if not os.path.isdir(subdir_path):
        continue

    posts_list_file = os.path.join(subdir_path, 'posts_list.json')

    with open(posts_list_file, 'r') as f:
        posts_list_data = json.load(f)

    # print(subdir_path)  # categories/daily
    # print(subdir)  # daily, miscellaneous, ios

    os.makedirs(f'{REPO_DIR}/{subdir}')

    index = os.path.join(f'{REPO_DIR}/{subdir}', 'index.html')

    with open(index, 'w') as f:
        f.write(make_list_index(subdir, posts_list_data))

# 3. [storage] -> [categories] -> all directories -> [posts] 순회 -> [html/[slug]/[aaaa-aaaa].html] 생성
for subdir in os.listdir(categories_dir):
    subdir_path = os.path.join(categories_dir, subdir)

    if not os.path.isdir(subdir_path):
        continue

    posts_path = os.path.join(subdir_path, "posts")  # categories/daily/posts

    if not os.path.exists(posts_path):
        # os.makedirs(posts_path)
        continue

    posts = [f for f in os.listdir(posts_path) if f.endswith('.md')]

    for post in posts:
        with open(f'{posts_path}/{post}', 'r') as file:
            md = file.read()

        content = os.path.join(f'{REPO_DIR}/{subdir}', f'{post.removesuffix(".md")}.html')

        with open(content, 'w') as f:
            f.write(make_html(md))

# Git 커밋 및 푸시
run_command(f'cd {REPO_DIR} && git add .')
run_command(f'cd {REPO_DIR} && git commit -m "Add changes from Auto Update HTML script"')
run_command(f'cd {REPO_DIR} && git push')
