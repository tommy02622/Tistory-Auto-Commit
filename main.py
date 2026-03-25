import feedparser
import datetime
import os

# 티스토리 RSS 주소
RSS_URL = 'https://topgun-ai.tistory.com/rss'

# RSS 피드 파싱
feed = feedparser.parse(RSS_URL)

print("🔍 피드 상태 확인:", feed.status if hasattr(feed, 'status') else "상태 코드 없음")
print("📥 가져온 글 개수:", len(feed.entries))

# 글이 1개 이상 있을 때만 실행
if len(feed.entries) > 0:
    # 딕셔너리 방식으로 가장 첫 번째(최신) 글을 안전하게 가져옴
    latest_post = feed.entries
    
    # 속성(Attribute) 에러를 방지하기 위해 .get() 함수 사용
    title = latest_post.get('title', '제목 없음')
    link = latest_post.get('link', '')
    published = latest_post.get('published', '')

    print(f"🎯 타겟 글 제목: {title}")

    # 오늘 날짜로 마크다운 파일명 생성
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    file_name = f"{today}-post.md"

    # 파일 내용 작성 (포스팅 제목과 링크)
    content = f"## 📝 최근 포스팅\n\n**[{title}]({link})**\n\n- 발행일: {published}\n"

    # 파일 저장 (이 동작이 깃허브에 커밋을 발생시켜 잔디를 심습니다)
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ {file_name} 파일 생성 완료!")
else:
    print("❌ 새로운 글을 찾을 수 없거나 블로그가 비어있습니다.")
