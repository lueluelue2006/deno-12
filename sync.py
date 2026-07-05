#!/usr/bin/env python3
import json
import shutil
from pathlib import Path

root = Path(__file__).parent
web = root / "web"
web.mkdir(exist_ok=True)
(web / ".nojekyll").touch()

data = json.loads((root / "data.json").read_text(encoding="utf-8"))
shutil.copy2(root / "data.json", web / "data.json")

template = (web / "template.html").read_text(encoding="utf-8")
marker = "/*__DATA__*/"
if marker not in template:
    raise SystemExit("template.html 缺少数据占位符")

from datetime import datetime

meta = f"{len(data)} 项 · {datetime.now().strftime('%m-%d %H:%M')}"
html = template.replace(marker, json.dumps(data, ensure_ascii=False))
html = html.replace("/*__META__*/", meta)
(web / "index.html").write_text(html, encoding="utf-8")
print(f"已同步 {len(data)} 项 → web/index.html")