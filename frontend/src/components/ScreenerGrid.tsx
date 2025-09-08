import TradingViewMiniChart from "../widgets/TradingViewMiniChart";
import { Card } from "react-bootstrap";

type Item = { symbol: string; exchange: string; change24h: number; volume24h: number; };

export default function ScreenerGrid({ items }: { items: Item[] }) {
  return (
    <div className="container py-3">
      <div className="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-xl-4 g-3">
        {items.map((it) => (
          <div className="col" key={it.exchange + it.symbol}>
            <Card className="h-100 bg-dark text-light">
              <Card.Body>
                <div className="d-flex justify-content-between align-items-center mb-2">
                  <div className="fw-semibold">{it.symbol}</div>
                  <div className={it.change24h >= 0 ? "text-success" : "text-danger"}>
                    {it.change24h.toFixed(2)}%
                  </div>
                </div>
                <TradingViewMiniChart symbol={`${it.exchange}:${it.symbol}`} />
                <div className="mt-2 small text-secondary">Vol 24h: {Intl.NumberFormat().format(it.volume24h)}</div>
              </Card.Body>
            </Card>
          </div>
        ))}
      </div>
    </div>
  );
}
