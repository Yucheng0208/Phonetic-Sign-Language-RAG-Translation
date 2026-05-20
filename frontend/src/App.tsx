import { useCallback, useEffect, useRef, useState } from "react";
import {
  checkHealth,
  createTranslateSocket,
  fetchRecognizeDemos,
  recognizeDemo,
  translate,
} from "./api";
import { CameraPanel } from "./components/CameraPanel";
import { LanguagePicker } from "./components/LanguagePicker";
import { ResultPanel } from "./components/ResultPanel";
import type { LanguageOption, RecognizeDemo, TranslateResponse } from "./types";
import "./App.css";

const LANGUAGES: LanguageOption[] = [
  { code: "zh-TW", label: "繁體中文" },
  { code: "zh-CN", label: "簡體中文" },
  { code: "en", label: "English" },
  { code: "ja", label: "日本語" },
  { code: "ko", label: "한국어" },
];

const DEMO_PHRASES = [
  "ㄓㄨㄥ ㄒㄧㄣ",
  "ㄋㄧˇ ㄏㄠˇ",
  "ㄒㄧㄝˋ ㄒㄧㄝˋ",
  "ㄕㄡˇ ㄩˇ ㄈㄢ ㄧˋ",
];

export default function App() {
  const [zhuyin, setZhuyin] = useState("ㄓㄨㄥ ㄒㄧㄣ");
  const [targetLang, setTargetLang] = useState("zh-TW");
  const [result, setResult] = useState<TranslateResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [useWs, setUseWs] = useState(false);
  const [health, setHealth] = useState<string>("檢查中…");
  const [recognizeMsg, setRecognizeMsg] = useState("");
  const [recognizeDemos, setRecognizeDemos] = useState<
    Record<string, RecognizeDemo>
  >({});
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    checkHealth()
      .then((h) => {
        setHealth(
          `後端正常 · 詞庫 ${h.corpus_entries} 筆 · Gemini ${h.gemini_configured ? "已設定" : "mock"} · 模型 ${h.model_loaded ? "已載入" : "未訓練"}`
        );
      })
      .catch(() => setHealth("後端未連線，請啟動 uvicorn"));

    fetchRecognizeDemos()
      .then(setRecognizeDemos)
      .catch(() => setRecognizeDemos({}));
  }, []);

  useEffect(() => {
    if (!useWs) {
      wsRef.current?.close();
      wsRef.current = null;
      return;
    }
    const ws = createTranslateSocket((data) => {
      setResult(data);
      setLoading(false);
    });
    wsRef.current = ws;
    return () => ws.close();
  }, [useWs]);

  const doTranslate = useCallback(async () => {
    if (!zhuyin.trim()) return;
    setLoading(true);
    try {
      if (useWs && wsRef.current?.readyState === WebSocket.OPEN) {
        wsRef.current.send(
          JSON.stringify({ zhuyin, target_lang: targetLang, top_k: 5 })
        );
      } else {
        const data = await translate(zhuyin, targetLang);
        setResult(data);
        setLoading(false);
      }
    } catch (e) {
      console.error(e);
      setLoading(false);
    }
  }, [zhuyin, targetLang, useWs]);

  const runDemoPipeline = useCallback(
    async (demoId: string) => {
      setLoading(true);
      setRecognizeMsg("");
      try {
        const rec = await recognizeDemo(demoId);
        setZhuyin(rec.zhuyin);
        setRecognizeMsg(rec.message);
        const data = await translate(rec.zhuyin, targetLang);
        setResult(data);
      } catch (e) {
        console.error(e);
        setRecognizeMsg(e instanceof Error ? e.message : "辨識失敗");
      } finally {
        setLoading(false);
      }
    },
    [targetLang]
  );

  return (
    <div className="app">
      <header className="header">
        <h1>注手快譯通</h1>
        <p className="subtitle">注音手語 · RAG 消歧 · 多語翻譯</p>
        <p className="health">{health}</p>
        <p className="todo-link">待辦清單：repo 根目錄 TODO.md</p>
      </header>

      <main className="main-grid">
        <section className="card input-card">
          <CameraPanel enabled />

          <div className="demo-section">
            <p className="label">手語辨識演示（模型訓練前）</p>
            <div className="demo-row">
              {Object.entries(recognizeDemos).map(([id, d]) => (
                <button
                  key={id}
                  type="button"
                  className="demo-chip recognize"
                  onClick={() => void runDemoPipeline(id)}
                  disabled={loading}
                >
                  {d.label}
                </button>
              ))}
            </div>
            {recognizeMsg && <p className="recognize-msg">{recognizeMsg}</p>}
          </div>

          <label className="field">
            <span>注音序列</span>
            <textarea
              value={zhuyin}
              onChange={(e) => setZhuyin(e.target.value)}
              rows={3}
              placeholder="例：ㄓㄨㄥ ㄒㄧㄣ"
            />
          </label>
          <div className="demo-row">
            {DEMO_PHRASES.map((p) => (
              <button
                key={p}
                type="button"
                className="demo-chip"
                onClick={() => setZhuyin(p)}
              >
                {p}
              </button>
            ))}
          </div>
          <LanguagePicker
            languages={LANGUAGES}
            selected={targetLang}
            onSelect={setTargetLang}
          />
          <label className="checkbox-row">
            <input
              type="checkbox"
              checked={useWs}
              onChange={(e) => setUseWs(e.target.checked)}
            />
            使用 WebSocket 即時通道
          </label>
          <button
            type="button"
            className="primary-btn"
            onClick={() => void doTranslate()}
            disabled={loading}
          >
            翻譯
          </button>
        </section>

        <section className="card">
          <ResultPanel result={result} loading={loading} />
        </section>
      </main>

      <footer className="footer">
        Phonetic Sign Language RAG Translation · 專題原型
      </footer>
    </div>
  );
}
