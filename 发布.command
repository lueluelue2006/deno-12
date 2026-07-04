#!/bin/bash
cd "$(dirname "$0")"
python3 sync.py
git add data.json web/index.html web/data.json
git diff --cached --quiet || git commit -m "sync $(date '+%Y-%m-%d %H:%M')"
git push
npx --yes gh-pages -d web
echo ""
echo "已发布 → https://lueluelue2006.github.io/zhuanyun-list/"
echo "（在线版只展示，不记录勾选）"