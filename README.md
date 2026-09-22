# Justine's Git Log

A GitHub Pages archive for TIL, AX study notes, AI news, and small projects.

https://justinweon.github.io

## Add writing

Add a Markdown file to one of these folders, then push to `main`:

```text
posts/
  daily/       # General notes (included in All Notes)
  code/        # Existing coding notes (shown as AX Study)
  ax-study/    # New AX Study notes
  ai-news/     # AI news and opinion posts
  projects/    # Mini-project writeups and repository links
```

Each post can use this optional front matter:

```md
---
title: A clear post title
date: 2026-09-15
excerpt: A short sentence shown on the home page.
---

# A clear post title

Write the rest in Markdown. Tables and fenced code blocks are supported.
```

## TIL sync

Markdown files from the public [`justinweon/TIL`](https://github.com/justinweon/TIL) repository are imported automatically as TIL notes during the Pages build. The workflow runs on pushes to `main`, manually from GitHub Actions, and every six hours.
