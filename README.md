# justine's notes

GitHub Pages 기반 개인 기록 블로그입니다.

https://justinweon.github.io

## 글 작성

아래 폴더에 Markdown 파일을 추가하면 다음 Pages 배포에서 탭별로 표시됩니다.

```text
posts/
  daily/
  code/
  projects/
```

예시:

```md
---
title: 글 제목
date: 2026-09-11
excerpt: 카드에 보여 줄 짧은 설명
---

# 글 제목

본문을 Markdown으로 작성합니다.
```

## TIL 자동 동기화

`justinweon/TIL` 공개 저장소의 모든 Markdown 기록은 빌드 때 자동으로 읽어 `TIL` 탭에 표시됩니다. 이 저장소의 Pages 워크플로는 다음 때 다시 빌드됩니다.

- 이 저장소의 `main` 브랜치에 push할 때
- GitHub Actions에서 수동 실행할 때
- 6시간마다 자동 실행될 때

TIL을 새로 올린 직후 반영하고 싶다면 이 저장소의 **Actions → Build and deploy notes → Run workflow**를 누르면 됩니다.
