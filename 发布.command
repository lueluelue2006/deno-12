#!/bin/bash
cd "$(dirname "$0")"
python3 sync.py
git add data.json web/index.html web/data.json
git commit -m "sync $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || true
git push
npx --yes gh-pages -d web -t true
echo ""
echo "在线地址：https://lueluelue2006.github.io/zhuanyun-list/"