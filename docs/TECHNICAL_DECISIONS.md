# Technical decisions

## Why FastAPI + Pandas (not only notebooks)

Product surface (API + UI) proves data-quality engineering as a shippable tool, not a one-off exploration.

## Why lab snapshots on Vercel (not FastAPI on Vercel)

Pandas audit workloads are heavier and less portable on serverless than a Next.js static/lab demo. Pattern mirrors DataOps Control Tower: public one-click demo with precomputed runs; full engine locally.

Trade-off: public demo cannot upload arbitrary CSVs. Documented honestly in Lab banner and methodology.

## Score is diagnostic, not certification

Weighted dimensions with severity penalties. UI must not claim “good” when critical issues remain (fixed in quality pass).

## Delimiter detection

Brazilian CSVs often use `;`. Parser scores candidates by column count (and rows), avoiding early accept of a one-column comma parse.

## CORS

Explicit allowlist (`CORS_ORIGINS`), credentials off. Avoids `*` + credentials anti-pattern.

## Encoding of snapshots

Always write with `ensure_ascii=False` and UTF-8. Regression script + test guard mojibake.
