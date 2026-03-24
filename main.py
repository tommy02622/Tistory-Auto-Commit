import feedparser
import datetime
import os

# 티스토리 RSS 주소
RSS_URL = 'https://topgun-ai.tistory.com/rss'

# RSS 피드 파싱
feed = feedparser.parse(RSS_URL)

# 최신 글 1개 가져오기
if feed.entries:
    latest_post = feed.entries
    title = latest_post.title
    link = latest_post.link
    published = latest_post.published

    # 오늘 날짜로 마크다운 파일명 생성
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    file_name = f"{today}-post.md"

    # 파일 내용 작성 (포스팅 제목과 링크)
    content = f"## 📝 최근 포스팅\n\n**[{title}]({link})**\n\n- 발행일: {published}\n"

    # 파일 저장 (이 동작이 깃허브에 커밋을 발생시켜 잔디를 심습니다)
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ {file_name} 생성 완료!")
else:
    print("❌ 새로운 글을 찾을 수 없습니다.")
