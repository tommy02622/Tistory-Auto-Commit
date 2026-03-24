# 📝 Tistory Auto-Sync Bot
> 티스토리 기술 블로그의 최신 포스팅을 감지하여 깃허브에 자동으로 커밋(잔디 심기)하는 봇입니다.

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)]()
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)]()

## 🔗 My Tech Blog
* **Blog Name:** TOP_GUN
* **URL:** [https://topgun-ai.tistory.com](https://topgun-ai.tistory.com)

## ⚙️ How it works
1. **GitHub Actions**의 `cron` 스케줄러를 통해 매일 지정된 시간에 워크플로우가 실행됩니다.
2. Python `feedparser` 라이브러리를 이용하여 티스토리 RSS 피드에서 최신 글을 파싱합니다.
3. 새로운 포스팅이 감지되면 해당 글의 제목, 링크, 발행일을 마크다운(`.md`) 파일로 생성합니다.
4. 생성된 파일을 이 레포지토리에 자동으로 `git commit & push` 하여 활동 기록(잔디)을 남깁니다.
