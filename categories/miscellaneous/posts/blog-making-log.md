# GitHub으로 블로그 만들기 (feat. 라이브러리/프레임워크 쓰지 않기)

드디어 블로그를 만들었다. 어떻게 만들었는지 상세하게 설명하고자 글을 쓴다.

## 1. 어떻게 만들고 어떻게 호스팅을 해야하나?

### 아직 웹 베이비는 라이브러리, 프레임워크는 투머치 아닐까?

처음에는 얄팍한 지식이지만 배우고 있는 Next.js로 만들까 생각해봤다.
하지만, 나는 웹을 잘 모른다. React는 SPA, Next.js는 SSR, SSG 등 이점이 많다는 건 알겠는데 문제를 맞닥뜨리지 않고 왜 배우는지 깨닫지 못해서 이 기회에 HTML, CSS, JS로 만들어보기로 결정했다.

> TailwindCSS만 CDN으로 가져다 쓸게요..! 미안합니다! 이건 꼭 직접 써보면서 배워보고 싶었어요..!

### GitHub Pages로 호스팅 해야겠다!

그냥 블로그만 운영하는 건데 돈을 내면서 도메인도 사고, 호스팅을 하는 건 이치에 맞지 않겠다 싶어서 GitHub Pages로 호스팅을 하기로 결정했다.

`github.io`로 레포를 하나 만들고 `index.html`만 담아서 Pages에서 원클릭으로 띄워보기로 한다.

<img width="784" alt="Pages" src="https://github.com/user-attachments/assets/bcc2c9cf-49c7-4a58-a5d4-8dd609197e28">

> 아주 잘 되는 구만 하하 시작이 좋아.

## 2. 포스팅은 어떻게 쓰고 스토리지/DB는 뭐로 쓰지?

프론트 구현이야 HTML/CSS/JS로 하겠지만, 포스팅을 저장하려면 따로 클라우드 서비스를 써야하는 건가? 호스팅을 GitHub으로 해도 돈을 내야한다고..?

흠, 뭔가 깃허브를 클라우드처럼 사용할 수 있을 것 같은데? 나는 개발자라 포스팅은 `Markdown`으로 쓰는 게 편하니까 포스팅을 아예 깃허브에 해버리고 이 레포를 프론트에 연결시킬 수 있지 않을까?

레포를 하나 만들고 `.md` 파일을 하나 만들어 `static`하게 가져올 수 있는 방법을 테스트 해봤다. 운이 좋게 깃허브의 파일 접근 혹은 다운로드를 raw하게 할 수 있는 링크를 제공하고 있었다.

`https://raw.githubusercontent.com/[username]/[repo]/[branch]/[file_path]` 이렇게 접근하면 내가 작성한 포스팅의 `.md` 파일을 원본으로 가져와 프론트에 띄워줄 수 있겠다고 판단했다.

## 3. 저장소의 구조를 어떻게 짤까?

우선 웹 페이지 맨 위 헤더에 깃허브, 연락처 등 여러 연결페이지 링크를 달려고 한다.

`header_links.json` [헤더 링크]
```json
[
  {
    "title": "Github",
    "link": "https://github.com/[username]"
  },
  {
    "title": "Email",
    "link": "mailto:[username]@[domain].com"
  }
]
```

--

다음은 카테고리를 나눠 카테고리별 포스트를 작성할 생각이니 카테고리별로 디렉토리를 만들고 정보가 담긴 파일을 만들어야겠다.

`categories/categories_info.json` [모든 카테고리에 해당하는 정보]

```json
[
  {
    "title": "iOS/SwiftUI",
    "path": "ios/",
    "description": "iOS/SwiftUI Posts",
    "status": "Building"
  },
  {
    "title": "Daily",
    "path": "daily/",
    "description": "Daily story, chill out :D 잡다한 일상얘기",
    "status": "Building"
  }
]
```

카테고리별로 정보를 담아 배열 형태로 전달해 index에서 띄워줄 생각이다.

`a href`로 `path`를 연결시켜 카테고리별 글 리스트를 확인할 수 있게 `posts_list.json`이 담긴 페이지로 넘겨준다.

--

`categories/[category]/posts_list.json` [해당 카테고리의 모든 포스팅 정보]

```json
[
  {
    "title": "a",
    "description": "a에 해당하는 설명",
    "path": "ios/a",
    "date": "2024.08.03 19:47"
  },
  {
    "title": "b",
    "description": "b description :D",
    "path": "ios/b",
    "date": "2024.08.03 19:46"
  },
  {
    "title": "c",
    "description": "c is not my grade :(",
    "path": "ios/c",
    "date": "2024.08.03 19:45"
  }
]
```

`path`를 `a href`에 연결시키면 저장되어 있는 포스팅을 볼 수 있게 된다!

--

`categories/[category]/posts/[title].md` [포스팅]

`posts/` 디렉토리에 카테고리별 포스팅을 저장하고 이걸 프론트에서 띄워주려고 한다.

### 정리하자면

```
header_links.json (헤더 링크)
categories/
    categories_info.json (카테고리들 정보)
    [category]
        posts_list.json (포스팅들 정보)
        posts/
            [title].md (포스팅 파일)
```

이런 형태로 스토리지를 구성했다.

## 4. 포스팅을 하면 .json에 다 자동으로 반영해줘!

나에게 생소했던 GitHub Actions를 제대로 맛을 보게 해주는 섹션이다.

자동화하려던 부분은 `posts/`에 포스팅을 작성하면 상위 디렉토리의 `posts_list.json`에 자동으로 `posts/` 디렉토리를 순회하면서 작성된 포스팅 정보를 반영하는 거였다.

이 부분은 GPT 교수님께 여쭤보고 도움을 받아 `.yml` 파일과 `.py` 파일을 구성할 수 있었다.

`update_posts_list.yml`

```yml
name: Update Posts List

# Controls when the workflow will run
on:
  push:
    paths:
      - "**"

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  update-posts-list:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: "3.x"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r .github/scripts/requirements.txt

      - name: Update posts_list.json for all directories
        run: python .github/scripts/update_all_posts_list.py

      - name: Commit and push changes
        run: |
          git config --global user.name 'github-actions[bot]'
          git config --global user.email 'github-actions[bot]@users.noreply.github.com'
          git add categories/**/posts_list.json
          git commit -m 'Update posts_list.json files' || true
          git push
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

브랜치는 어차피 `main` 하나만 쓸 거라 목표하는 브랜치는 정해주지 않았으며, 경로에 상관 없이 `push`가 이루어지면 `update_all_posts_list.py`를 실행하고 Commit/Push를 하게 구성했다.

`update_all_posts_list.py`

```python
import os
import json
from datetime import datetime
import pytz

categories_dir = 'categories'
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
        data_path = f'{data["path"].split("/")[1]}.md'

        if data_path not in posts:
            posts_list_data.remove(data)

    for post in posts:
        if post not in [f'{item["path"].split("/")[1].removesuffix(".html")}.md' for item in posts_list_data]:
            now = datetime.now(kst)

            posts_list_data.append(
                {
                    "title": post.removesuffix(".md"),
                    "description": "-",
                    "path": f'{subdir}/{post.removesuffix(".md")}',
                    "date": now.strftime("%Y.%m.%d %H:%M")
                }
            )

    with open(posts_list_file, 'w') as f:
        json.dump(posts_list_data, f, indent=2)
````

간략하게 설명하면

1. 카테고리 디렉토리 안에 `posts_list.json`이 존재하지 않는다면 만들어서 빈 배열 전달
2. `posts/` 디렉토리를 돌면서 `posts_list.json`에 업데이트 진행
    - `posts/`에 포스팅이 존재하는데 `posts_list.json`에 없는 경우 -> 새로운 포스팅 -> 추가
    - `posts_list.json`에 존재하는데 `posts/`에 없는 경우 -> 포스팅이 삭제 됨 -> 반영

잘 된다. Good.

## 5. 프론트에 어떻게 보여줄까?

### SPA처럼 JS로 json을 파싱해서 프론트에 뿌려주자
스토리지를 위처럼 구성한 이유가 프론트에서 HTTP 요청을 보내 json을 가져와 DOM으로 프론트를 변경시키는 형태로 구성하려고 그랬다.

```Javascript
async function fetchData(path) {
  try {
    const response = await fetch(
      `https://raw.githubusercontent.com/[username]/[repo]/main${path}`,
    );

    if (!response.ok) {
      return {
        status: false,
        message: "Network Response Error",
      };
    }

    return {
      status: true,
      result: await response.json(),
    };
  } catch (error) {
    return {
      status: false,
      message: error.message,
    };
  }
}

// Header
fetchData("/header_links.json").then((headerResponse) => {
    if (!headerResponse.status) {
        return;
    }

    const headerItems = headerResponse.result;

    const container = document.getElementById('header-container');

    headerItems.forEach((item, index) => {
        const a = document.createElement("a");
        a.className = "text-[#0000EE] underline underline-offset-4";
        a.innerHTML = item.title;
        a.href = item.link;
        a.target = "_blank";

        container.appendChild(a);

        if (index < headerItems.length - 1) {
            const separator = document.createTextNode("/");
            container.appendChild(separator);
        }
    });
});

... Categories
```

실제로 메인 페이지인 `/index.html`을 구성하였고, Header 링크를 구성하는 데까지는 문제가 없었다. 어차피 외부 링크니까.

그렇게 Categories 섹션을 구성하다가 문득 큰일이 난 걸 알아차렸다.

```Javascript
// Categories
fetchData("/categories/categories_info.json").then((categoriesInfoResponse) => {
    if (!categoriesInfoResponse.status) {
        return;
    }

    const header = document.getElementById("categories-header");
    header.innerHTML = "categories";

    const categories = categoriesInfoResponse.result;

    const container = document.getElementById('categories-container');

    categories.forEach((item) => {
        const li = document.createElement("li");
        li.className = "flex flex-col items-start gap-1";

        const a = document.createElement("a");
        a.className = "flex items-center gap-1.5"
        a.href = item["path"];

        const span = document.createElement("span");
        span.className = "text-[#0000EE] font-medium underline underline-offset-4";
        span.innerHTML = item.title;

        a.appendChild(span);

        if (item.status !== undefined && item.status !== null) {
            const dash = document.createTextNode("-");

            a.appendChild(dash);

            const span2 = document.createElement("span");
            span2.className = "text-xs text-[#09090B] tracking-tight underline underline-offset-4";
            span2.innerHTML = item.status;

            a.appendChild(span2);
        }

        const span3 = document.createElement("span");
        span3.className = "text-sm text-[#09090B]";
        span3.innerHTML = item.description;

        li.appendChild(a);
        li.appendChild(span3);

        container.appendChild(li);
    });
});
```

> 아. 포스팅 리스트 페이지를 연결하려면 페이지가 필요한데..? `[categories]/index.html`은 어떻게 만들어야하지? 이건 그냥 내가 수동으로 만들어서 배포해야하나..? 그냥 DOM으로 바꾸는 방식으로 해볼까..?

> 아. 포스팅 리스트 페이지는 선녀인데..? 포스팅 글 페이지는 어떻게 DOM으로 바꿀래..? 그리고 적어도 `[domain]/[categories]/test-post` 링크로 접속하면 글을 볼 수 있게 하는 게 맞지 않나..? 다이나믹 라우팅은 어떻게..?

여기서 뭔가 이상하다고 느꼈다. 제일 중요했던 건 `[domain]/[categories]/test-post` 링크로 접속했을 때 글은 보여주는 게 맞다고 생각을 했다. 모든 걸 DOM으로 바꿔버리면 링크는 메인 페이지 `index.html`만 존재하게 될 거라 글을 연결시켜줄 수 없었다. (404 에러가 뜨니까.. 404 페이지에서 path를 추출해서 `index.html`로 리다이렉션 하고 DOM을 바꿔버리는 방법도 있을 것 같긴 한데 내가 원하는 방향은 아니었다.)

> 그럼 결국에는 다이나믹 라우팅을 지원하려면 라이브러리나 프레임워크를 써야하나..?

조금 생각해보고 새로운 방법을 찾았다.

### Actions를 통해 html을 생성하고 github.io 레포에 커밋해서 빌드하자

어차피 `github.io` 레포는 커밋하면 자동으로 빌드해서 배포까지 진행한다.

그럼 우리는 스토리지 레포에서 Actions로 html을 만들고 이 파일들을 `github.io` 레포에 반영해야한다.

Actions로 a 레포에서 b 레포로 레포간의 커밋이라 좀 어려워보였지만, 생각보다 복잡하지도 않고 어렵지도 않았다.

먼저 잘 생각해보자.

이 워크플로우가 실행되기 위한 조건은 `Update All Posts List`가 끝났을 때 실행하면 될 것이다.
그런 다음 `github.io` 레포를 `clone` 하고 html을 만들어서 `github.io` 레포로 커밋, 푸시를 날리면 끝이다.

그러기 위해서는 레포에 commit, push를 할 수 있는 권한을 가진 토큰을 하나 발행하고 스토리지 레포에 토큰을 저장한다.
- `update_posts_list.yml`에서 사용한 자동으로 생성되는 `secrets.GITHUB_TOKEN`을 사용하면 되는 거 아닌가? - 이 토큰은 이 워크플로우가 포함된 레포로 제한되기 때문에 새로 만들어야 한다.

`update_blog.yml`

```yml
name: Update Blog

# Controls when the workflow will run
on:
  workflow_run:
    workflows: ["Update Posts List"]
    types:
      - completed

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  update-blog:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: "3.x"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r .github/scripts/requirements.txt

      - name: Update html for blog
        env:
          TARGET_REPO_TOKEN: ${{ secrets.TARGET_REPO_TOKEN }}
        run: python .github/scripts/update_blog.py
```

간단하다. Update Posts List가 끝나면 update_blog.py를 실행하는 것.

`update_blog.py`

```python
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
    return "SOME HTML TEXT"


def make_html(text):
    return "SOME HTML TEXT"


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
```

필요한 카테고리의 index.html을 만들어주는 기능

posts/를 순회하면서 md 파일을 html로 변환시키고 [title].html로 만들어주는 기능

커밋과 푸시로 적용하는 기능

결국에는 `github.io`에서는 자바스크립트가 아예 필요 없어진 모습이다.

이렇게 스토리지 레포에서 글을 작성하면 자동으로 Pages로 호스팅하는 레포에도 적용되게 모든 걸 자동화 시킨 블로그 개발이 끝이 났다.

## 짧고 굵게 0부터 100까지 블로그를 만들어본 후기

HTML은 정말 문서가 맞다. 왜 React를 쓰게 됐는지, 자바스크립트 라이브러리에 열광하는지 조금은 알게 됐다. 안 쓸 이유가 없구나.

하면 된다. 배움을 무서워하지 말자. 발전이 없다고 생각이 들겠지만 사실 너는 빠르게 발전하고 있다.

세상에 하나밖에 없는 완전 커스텀 블로그. 더욱 애착이 가는 만큼 글도 자주 쓰고 싶다.

> 여담이지만 지금 알게 된 사실인데 많은 사람들이 GitHub Pages로 블로그를 만들 때 `Jekyll theme`을 많이 사용한다. 정말 간편하게 이것만 적용하면 바로 블로그를 사용할 수 있게 해주는데 포스팅은 어떻게 저장하고 가져오는 걸까 궁금해서 알아봤다. 신기하게도 나랑 똑같은 방식으로 레포의 `_posts/` 디렉토리에 `.md` 파일을 저장하면 `Actions`로 배포할 때 `_site/blog/[title].html`을 만들어주는 방식이다. 내가 구현한 방식과 크게 다르지 않아 내 스스로가 잘 생각하고 괜찮은 방향으로 결정을 내리고 있다고 생각했다.
