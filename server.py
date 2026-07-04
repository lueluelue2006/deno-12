#!/usr/bin/env python3
import json
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Timer

DIR = Path(__file__).parent
DATA = DIR / "data.json"
PORT = 8765

DEFAULT = [
    {"id": 1,  "cat": "冬季保暖", "name": "薄羽绒服",      "note": "2-3件，家里室内穿", "bought": False, "opened": False, "packed": False},
    {"id": 2,  "cat": "冬季保暖", "name": "薄款长袖/卫衣",  "note": "居家穿，轻便", "bought": False, "opened": False, "packed": False},
    {"id": 18, "cat": "冬季保暖", "name": "睡裤",          "note": "居家穿", "bought": False, "opened": False, "packed": False},
    {"id": 3,  "cat": "冬季保暖", "name": "羊毛袜/厚袜子", "note": "爸买的", "bought": True, "opened": True, "packed": False},
    {"id": 4,  "cat": "冬季保暖", "name": "围巾",          "note": "", "bought": False, "opened": False, "packed": False},
    {"id": 11, "cat": "冬季保暖", "name": "手套",          "note": "", "bought": False, "opened": False, "packed": False},
    {"id": 12, "cat": "冬季保暖", "name": "护脖帽",        "note": "能护脖子那种", "bought": False, "opened": False, "packed": False},
    {"id": 5,  "cat": "冬季小物", "name": "暖宝宝/暖贴",    "note": "？待问能否带", "bought": False, "opened": False, "packed": False},
    {"id": 7,  "cat": "冬季小物", "name": "热水袋",        "note": "？不一定能带", "bought": False, "opened": False, "packed": False},
    {"id": 8,  "cat": "文具",     "name": "中性笔/铅笔",   "note": "最后再说，得自己买去试", "bought": False, "opened": False, "packed": False},
    {"id": 10, "cat": "文具",     "name": "便利贴",        "note": "可以考虑买一点", "bought": False, "opened": False, "packed": False},
    {"id": 13, "cat": "文具",     "name": "胶带",          "note": "一定要买，细的粗的都要", "bought": False, "opened": False, "packed": False},
    {"id": 22, "cat": "文具",     "name": "订书机",        "note": "爸买的", "bought": True, "opened": False, "packed": False},
    {"id": 23, "cat": "文具",     "name": "文件袋",        "note": "", "bought": True, "opened": False, "packed": False},
    {"id": 14, "cat": "日用品",   "name": "手机壳",        "note": "已有1个，再来1个就够", "bought": False, "opened": False, "packed": False},
    {"id": 15, "cat": "日用品",   "name": "数据线",        "note": "？不一定要买", "bought": False, "opened": False, "packed": False},
    {"id": 16, "cat": "日用品",   "name": "转换插头",      "note": "小的大的都要买", "bought": False, "opened": False, "packed": False},
    {"id": 19, "cat": "日用品",   "name": "拖鞋",          "note": "", "bought": False, "opened": False, "packed": False},
    {"id": 20, "cat": "日用品",   "name": "耳塞",          "note": "考虑再买几个新的", "bought": False, "opened": False, "packed": False},
    {"id": 21, "cat": "日用品",   "name": "雨伞",          "note": "要带", "bought": False, "opened": False, "packed": False},
    {"id": 24, "cat": "日用品",   "name": "创可贴/常用药", "note": "感冒药、止痛片等，量别太大", "bought": False, "opened": False, "packed": False},
    {"id": 25, "cat": "日用品",   "name": "鞋子",          "note": "", "bought": False, "opened": False, "packed": False},
    {"id": 26, "cat": "日用品",   "name": "擦眼镜纸",      "note": "", "bought": True, "opened": False, "packed": False},
    {"id": 27, "cat": "日用品",   "name": "指甲刀",        "note": "考虑再买", "bought": False, "opened": False, "packed": False},
    {"id": 28, "cat": "日用品",   "name": "小风扇",        "note": "", "bought": False, "opened": False, "packed": False},
]


def normalize(item):
    if "brought" in item:
        item["packed"] = item.get("packed") or item["brought"]
        del item["brought"]
    return item


def load_items():
    if DATA.exists():
        items = json.loads(DATA.read_text(encoding="utf-8"))
        return [normalize(i) for i in items]
    save_items(DEFAULT)
    return DEFAULT


def save_items(items):
    DATA.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIR), **kwargs)

    def log_message(self, fmt, *args):
        if args and str(args[0]).startswith("GET /api"):
            return
        super().log_message(fmt, *args)

    def send_json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/items":
            self.send_json(load_items())
            return
        if self.path in ("/", ""):
            self.path = "/转运清单.html"
        return super().do_GET()

    def do_POST(self):
        if self.path != "/api/items":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        items = json.loads(self.rfile.read(length).decode("utf-8"))
        save_items(items)
        self.send_json({"ok": True})


def main():
    if not DATA.exists():
        save_items(DEFAULT)
    url = f"http://localhost:{PORT}/"
    print(f"转运清单 → {url}")
    print("数据文件 →", DATA)
    print("按 Ctrl+C 停止")
    Timer(0.5, lambda: webbrowser.open(url)).start()
    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()