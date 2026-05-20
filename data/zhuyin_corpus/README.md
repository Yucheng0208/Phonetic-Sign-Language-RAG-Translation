# 注音詞庫格式

目錄內所有 `*.json` 會被後端自動載入合併。

## JSON 陣列格式

```json
[
  {
    "zhuyin": "ㄓㄨㄥ ㄒㄧㄣ",
    "text": "中心",
    "tags": ["地點", "常用"]
  }
]
```

| 欄位 | 必填 | 說明 |
|------|------|------|
| `zhuyin` | 是 | 空格分隔注音，例：`ㄋㄧˇ ㄏㄠˇ` |
| `text` | 是 | 對應中文詞或短語 |
| `tags` | 否 | 分類標籤，供 RAG / UI 顯示 |

## 同音多義

同一 `zhuyin` 可有多筆 `text`（RAG 會全部列入候選）。

## 匯入工具

```bash
python scripts/import_corpus.py --zhuyin "ㄒㄧㄝˋ ㄒㄧㄝˋ" --text "謝謝" --tags 問候
```
