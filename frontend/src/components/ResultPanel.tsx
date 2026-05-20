import type { TranslateResponse } from "../types";

interface Props {
  result: TranslateResponse | null;
  loading: boolean;
}

export function ResultPanel({ result, loading }: Props) {
  if (loading) {
    return <div className="result-panel loading">翻譯中…</div>;
  }
  if (!result) {
    return (
      <div className="result-panel empty">
        輸入注音序列並按下「翻譯」，或選擇示範詞組。
      </div>
    );
  }

  return (
    <div className="result-panel">
      <section>
        <h3>注音</h3>
        <p className="zhuyin">{result.zhuyin}</p>
      </section>
      <section>
        <h3>RAG 候選</h3>
        <ul className="candidates">
          {result.rag_candidates.map((c) => (
            <li key={`${c.text}-${c.score}`}>
              <span className="cand-text">{c.text}</span>
              <span className="cand-score">{(c.score * 100).toFixed(1)}%</span>
              {c.tags.length > 0 && (
                <span className="cand-tags">{c.tags.join(" · ")}</span>
              )}
            </li>
          ))}
        </ul>
      </section>
      <section>
        <h3>中文</h3>
        <p className="highlight">{result.chinese}</p>
      </section>
      <section>
        <h3>譯文</h3>
        <p className="highlight">{result.translation}</p>
        {result.llm_mock && (
          <p className="mock-badge">LLM mock（請設定 GEMINI_API_KEY）</p>
        )}
      </section>
    </div>
  );
}
