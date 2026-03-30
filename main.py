import datetime
import json
import os
from email.utils import parsedate_to_datetime

import feedparser

RSS_URL = "https://topgun-ai.tistory.com/rss"
STATE_FILE = "last_post.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {"links": []}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as file:
            state = json.load(file)
            if isinstance(state, dict) and isinstance(state.get("links"), list):
                return state
            return {"links": []}
    except json.JSONDecodeError:
        return {"links": []}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(state, file, ensure_ascii=False, indent=2)


def get_post_date(entry):
    if entry.get("published_parsed"):
        return datetime.datetime(*entry.published_parsed[:6])
    published = entry.get("published", "")
    if published:
        try:
            return parsedate_to_datetime(published)
        except (TypeError, ValueError):
            pass
    return datetime.datetime.now()


def already_recorded(link, file_name, state):
    if link in state.get("links", []):
        return True
    if os.path.exists(file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                return link in file.read()
        except OSError:
            return False
    return False


def main():
    feed = feedparser.parse(RSS_URL)
    print("피드 상태:", feed.status if hasattr(feed, "status") else "상태 코드 없음")
    print("가져온 글 개수:", len(feed.entries))

    if not feed.entries:
        print("새 글이 없거나 RSS 피드가 비어 있습니다.")
        return

    state = load_state()
    created = 0

    for entry in feed.entries:
        title = entry.get("title", "제목 없음")
        link = entry.get("link", "")
        published = entry.get("published", "")
        post_date = get_post_date(entry)
        file_name = f"{post_date:%Y-%m-%d}-post.md"

        if not link:
            continue
        if already_recorded(link, file_name, state):
            continue

        content = (
            "## 오늘의 최신 포스팅\n"
            f"**[{title}]({link})**\n\n"
            f"- 발행일: {published}\n"
        )

        mode = "a" if os.path.exists(file_name) else "w"
        with open(file_name, mode, encoding="utf-8") as file:
            if mode == "a":
                file.write("\n")
            file.write(content)

        state["links"].append(link)
        created += 1
        print(f"{file_name} 파일에 글 추가: {title}")

    save_state(state)
    if created == 0:
        print("새로 기록할 글이 없습니다.")
    else:
        print(f"총 {created}개 글을 기록했습니다.")


if __name__ == "__main__":
    main()
