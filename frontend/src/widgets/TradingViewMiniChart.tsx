import { useEffect, useRef } from "react";

type Props = {
  symbol: string; // пример: "BINANCE:BTCUSDT"
  width?: number | string;
  height?: number | string;
  interval?: "1" | "5" | "15" | "60" | "240" | "D";
  locale?: string;
  theme?: "light" | "dark";
};

declare global {
  interface Window { TradingView: any }
}

export default function TradingViewMiniChart({
  symbol,
  width = "100%",
  height = 150,
  interval = "60",
  locale = "en",
  theme = "dark",
}: Props) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const scriptId = "tv-minichart";
    if (!document.getElementById(scriptId)) {
      const s = document.createElement("script");
      s.id = scriptId;
      s.src = "https://s3.tradingview.com/tv.js";
      s.async = true;
      document.head.appendChild(s);
      s.onload = () => renderWidget();
    } else {
      renderWidget();
    }

    function renderWidget() {
      if (!ref.current || !window.TradingView) return;
      // Очищаем контейнер при повторном маунте
      ref.current.innerHTML = "";
      new window.TradingView.MiniWidget({
        container_id: ref.current,
        symbol,
        width,
        height,
        locale,
        dateRange: "1D",
        colorTheme: theme,
        trendLineColor: "#2962FF",
        underLineColor: "rgba(41, 98, 255, 0.3)",
        isTransparent: true,
        autosize: false,
        noTimeScale: false,
        interval,
      });
    }
  }, [symbol, width, height, interval, locale, theme]);

  return <div ref={ref} />;
}
