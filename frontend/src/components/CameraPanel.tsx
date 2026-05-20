import { useEffect, useRef, useState } from "react";

interface Props {
  enabled: boolean;
}

export function CameraPanel({ enabled }: Props) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!enabled) return;

    let stream: MediaStream | null = null;

    async function start() {
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: "user", width: { ideal: 640 }, height: { ideal: 480 } },
          audio: false,
        });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
        setError(null);
      } catch {
        setError("無法存取攝影機，請確認瀏覽器權限。");
      }
    }

    void start();

    return () => {
      stream?.getTracks().forEach((t) => t.stop());
    };
  }, [enabled]);

  return (
    <div className="camera-panel">
      <p className="label">即時影像（手語模型串接後可送幀辨識）</p>
      {error ? (
        <p className="camera-error">{error}</p>
      ) : (
        <video ref={videoRef} autoPlay playsInline muted className="camera-video" />
      )}
    </div>
  );
}
