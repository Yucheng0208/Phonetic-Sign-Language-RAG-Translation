import type { RecognizeDemo, RecognizeResponse, TranslateResponse } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE ?? "";

export async function translate(
  zhuyin: string,
  targetLang: string,
  topK = 5
): Promise<TranslateResponse> {
  const res = await fetch(`${API_BASE}/api/translate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ zhuyin, target_lang: targetLang, top_k: topK }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || `HTTP ${res.status}`);
  }
  return res.json() as Promise<TranslateResponse>;
}

export async function recognizeDemo(demoId: string): Promise<RecognizeResponse> {
  const res = await fetch(`${API_BASE}/api/recognize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ demo_id: demoId }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || `HTTP ${res.status}`);
  }
  return res.json() as Promise<RecognizeResponse>;
}

export async function fetchRecognizeDemos(): Promise<
  Record<string, RecognizeDemo>
> {
  const res = await fetch(`${API_BASE}/api/recognize/demos`);
  return res.json() as Promise<Record<string, RecognizeDemo>>;
}

export function createTranslateSocket(
  onMessage: (data: TranslateResponse) => void,
  onError?: (err: Event) => void
): WebSocket {
  const wsBase = import.meta.env.VITE_WS_BASE;
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const host = wsBase ?? `${protocol}//${window.location.host}`;
  const url = `${host}/ws/translate`;
  const ws = new WebSocket(url);
  ws.onmessage = (ev) => {
    const data = JSON.parse(ev.data as string) as TranslateResponse & {
      error?: string;
    };
    if (data.error) {
      console.error(data.error);
      return;
    }
    onMessage(data);
  };
  if (onError) ws.onerror = onError;
  return ws;
}

export async function checkHealth(): Promise<{
  status: string;
  corpus_entries: number;
  gemini_configured: boolean;
  model_loaded: boolean;
}> {
  const res = await fetch(`${API_BASE}/api/health`);
  return res.json();
}
