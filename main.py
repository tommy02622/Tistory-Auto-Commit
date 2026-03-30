import datetime
import json
import os
from email.utils import parsedate_to_datetime

import feedparser

RSS_URL = "https://topgun-ai.tistory.com/rss"
STATE_FILE = "last_post.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}


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
    if state.get("link") == link:
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

    latest = feed.entries[0]
    title = latest.get("title", "제목 없음")
    link = latest.get("link", "")
    published = latest.get("published", "")
    post_date = get_post_date(latest)
    file_name = f"{post_date:%Y-%m-%d}-post.md"

    print(f"최신 글 제목: {title}")
    print(f"작성 파일: {file_name}")

    state = load_state()
    if already_recorded(link, file_name, state):
        print("이미 기록된 글입니다. 새 파일을 생성하지 않습니다.")
        return

    content = (
        "## 오늘의 최신 포스팅\n"
        f"**[{title}]({link})**\n\n"
        f"- 발행일: {published}\n"
    )

    with open(file_name, "w", encoding="utf-8") as file:
        file.write(content)

    save_state(
        {
            "title": title,
            "link": link,
            "published": published,
            "file": file_name,
        }
    )
    print(f"{file_name} 파일 생성 완료!")


if __name__ == "__main__":
    main()
