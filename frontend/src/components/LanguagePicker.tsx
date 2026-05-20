import { Swiper, SwiperSlide } from "swiper/react";
import { FreeMode } from "swiper/modules";
import type { LanguageOption } from "../types";
import "swiper/css";
import "swiper/css/free-mode";

interface Props {
  languages: LanguageOption[];
  selected: string;
  onSelect: (code: string) => void;
}

export function LanguagePicker({ languages, selected, onSelect }: Props) {
  return (
    <div className="lang-picker">
      <p className="label">輸出語言</p>
      <Swiper
        modules={[FreeMode]}
        slidesPerView="auto"
        spaceBetween={8}
        freeMode
        className="lang-swiper"
      >
        {languages.map((lang) => (
          <SwiperSlide key={lang.code} className="lang-slide">
            <button
              type="button"
              className={`lang-chip ${selected === lang.code ? "active" : ""}`}
              onClick={() => onSelect(lang.code)}
            >
              {lang.label}
            </button>
          </SwiperSlide>
        ))}
      </Swiper>
    </div>
  );
}
