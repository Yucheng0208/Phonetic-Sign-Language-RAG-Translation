# Zhuyin Corpus Format / 注音詞庫格式

All `*.json` files in this directory are loaded and merged by the backend.  
目錄內所有 `*.json` 會由後端自動載入合併。

## JSON array schema / JSON 陣列格式

```json
[
  {
    "zhuyin": "ㄓㄨㄥ ㄒㄧㄣ",
    "text": "中心",
    "tags": ["location", "common"]
  }
]
```

| Field / 欄位 | Required / 必填 | Description / 說明 |
|--------------|-----------------|-------------------|
| `zhuyin` | Yes / 是 | Space-separated Zhuyin, e.g. `ㄋㄧˇ ㄏㄠˇ` |
| `text` | Yes / 是 | Chinese word or phrase / 中文詞或短語 |
| `tags` | No / 否 | Labels for RAG and UI / 分類標籤 |

## Homophones / 同音多義

Multiple `text` entries may share the same `zhuyin`; RAG returns all as candidates.  
同一 `zhuyin` 可對應多筆 `text`，RAG 會全部列入候選。

## Import tool / 匯入工具

```bash
python scripts/import_corpus.py --zhuyin "ㄒㄧㄝˋ ㄒㄧㄝˋ" --text "謝謝" --tags greeting
```
