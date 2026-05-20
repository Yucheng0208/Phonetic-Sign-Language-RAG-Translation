export interface RagCandidate {
  text: string;
  zhuyin: string;
  score: number;
  tags: string[];
}

export interface TranslateResponse {
  zhuyin: string;
  rag_candidates: RagCandidate[];
  chinese: string;
  translation: string;
  target_lang: string;
  llm_mock: boolean;
}

export interface RecognizeResponse {
  zhuyin: string;
  source: string;
  message: string;
}

export interface RecognizeDemo {
  zhuyin: string;
  label: string;
}

export interface LanguageOption {
  code: string;
  label: string;
}
