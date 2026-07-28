"""Build DADS M02 Lab 2 — Bitcoin Analyzer (advanced).

A genuinely useful crypto-analysis lab built around free CoinGecko data and
the OpenAI client we already have:

  - live spot price + 24h change
  - 90-day price history with matplotlib chart
  - 20/50-day moving averages + RSI(14) computed from raw data
  - multi-coin returns comparison chart
  - LLM-driven technical commentary that reads the actual numbers
  - LLM-driven crypto-news summarizer (RSS-free; uses CoinGecko's status updates)
  - structured JSON-output trade signal with rationale

No paid APIs. No private keys. Runs end-to-end in Colab.
"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, "tools")
from build_lab import build, md, code

LAB_PATH = Path("labs/M02/M02_Lab2_Bitcoin_Analyzer.ipynb")
TITLE = "M02 Lab 2 — Bitcoin Analyzer"
EMOJI = "📈"
DIFFICULTY = "Intermediate"
TIME = "~45 min"

body = [
    md("""<div style="background: #f0f4ff; border-left: 4px solid #0055d4; padding: 16px 20px; border-radius: 0 8px 8px 0; margin: 12px 0;">
  <h3 style="color: #001a70; margin: 0 0 8px;">🎯 Learning Objectives</h3>
  <ol style="margin: 0; color: #1a1a2e; font-size: 14px;">
    <li>Pull <b>live crypto market data</b> from a free public API (CoinGecko)</li>
    <li>Compute classic <b>technical indicators</b> by hand: returns, moving averages, RSI</li>
    <li>Render <b>publication-quality charts</b> (price + indicators + multi-coin comparison)</li>
    <li>Have the LLM <b>read the numbers</b>, not just the prompt — feed it the indicator values and ask for a written read</li>
    <li>Produce a <b>structured JSON trade signal</b> with a confidence score and explicit rationale</li>
  </ol>
</div>

> **🚨 Disclaimer.** This lab is educational. The "trade signal" is a teaching exercise, not investment advice. Crypto is volatile; do not trade on outputs from a homework notebook.
"""),

    md("""## 🪙 Why this lab exists

Crypto markets are the perfect playground for "AI in action": the data is free, the values change minute-to-minute, and the analyses you can buy on Bloomberg cost thousands of dollars per seat. By the end of this lab you'll have built a small analyst-in-a-box that pulls live prices, computes the same indicators a chartist would compute, draws clean charts, and asks an LLM to write the commentary you'd otherwise hire for.
"""),

    md("""## 1️⃣ Pull live market data (no API key required)

CoinGecko's public endpoint returns spot prices and percentage changes for any coin pair without registration. We grab Bitcoin, Ethereum, and Solana in one call.
"""),

    code("""import requests, time

COINS = ["bitcoin", "ethereum", "solana"]

resp = requests.get(
    "https://api.coingecko.com/api/v3/simple/price",
    params={
        "ids": ",".join(COINS),
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "include_market_cap": "true",
        "include_24hr_vol": "true",
    },
    timeout=20,
)
resp.raise_for_status()
spot = resp.json()
pp(spot, title="📡 Live spot snapshot")
"""),

    md("""## 2️⃣ 90-day price history

The `/coins/{id}/market_chart` endpoint returns a list of `[timestamp_ms, price]` pairs. We pull 90 days of Bitcoin and stash it in a pandas DataFrame for downstream analysis.
"""),

    code("""import pandas as pd
from datetime import datetime, timezone

def fetch_history(coin: str, days: int = 90) -> pd.DataFrame:
    r = requests.get(
        f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart",
        params={"vs_currency": "usd", "days": days},
        timeout=30,
    )
    r.raise_for_status()
    rows = r.json()["prices"]
    df = pd.DataFrame(rows, columns=["ts_ms", "price"])
    df["date"] = pd.to_datetime(df["ts_ms"], unit="ms", utc=True).dt.tz_convert(None)
    df = df[["date", "price"]].set_index("date")
    # CoinGecko returns roughly hourly samples on a 90-day window — collapse to
    # daily closes so our indicators are easy to interpret.
    return df.resample("1D").last().dropna()

btc = fetch_history("bitcoin", days=90)
print(f"rows: {len(btc)}  |  range: {btc.index.min().date()} → {btc.index.max().date()}")
btc.tail(5)
"""),

    md("""## 3️⃣ Indicators: returns, 20-/50-day SMA, RSI(14)

These three are the bread and butter of every crypto chart you'll ever look at. We compute them straight from the price series — no `ta-lib`, no extra installs.

* **Daily return** — % change vs. yesterday
* **Moving averages (SMA20, SMA50)** — trend filters; price above both is "uptrend"
* **RSI(14)** — momentum oscillator, classically overbought >70 and oversold <30
"""),

    code("""def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["ret"] = out["price"].pct_change()
    out["sma20"] = out["price"].rolling(20).mean()
    out["sma50"] = out["price"].rolling(50).mean()

    # RSI(14) — Wilder's formula, vectorized.
    delta = out["price"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss
    out["rsi14"] = 100 - 100 / (1 + rs)

    return out

btc_ind = compute_indicators(btc)
btc_ind.tail(5)
"""),

    md("""## 4️⃣ Chart: price + moving averages + RSI

A two-panel layout you'll recognize from any trading platform: price/MAs on top, RSI on the bottom.
"""),

    code("""import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True,
                                gridspec_kw={"height_ratios": [3, 1]})

ax1.plot(btc_ind.index, btc_ind["price"], color="#001a70", lw=1.6, label="BTC price")
ax1.plot(btc_ind.index, btc_ind["sma20"], color="#0055d4", lw=1.0, ls="--", label="SMA(20)")
ax1.plot(btc_ind.index, btc_ind["sma50"], color="#d97706", lw=1.0, ls="--", label="SMA(50)")
ax1.set_ylabel("USD")
ax1.set_title("Bitcoin — last 90 days", fontsize=13, fontweight="bold", color="#001a70")
ax1.legend(loc="upper left", frameon=False)
ax1.grid(alpha=0.3)

ax2.plot(btc_ind.index, btc_ind["rsi14"], color="#0055d4", lw=1.2)
ax2.axhline(70, color="#c62828", lw=0.8, ls=":", label="overbought (70)")
ax2.axhline(30, color="#1b5e20", lw=0.8, ls=":", label="oversold (30)")
ax2.fill_between(btc_ind.index, 30, 70, alpha=0.05, color="#0055d4")
ax2.set_ylabel("RSI(14)")
ax2.set_ylim(0, 100)
ax2.legend(loc="upper left", frameon=False, fontsize=8)
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.show()
"""),

    md("""## 5️⃣ Multi-coin returns comparison

How did the three coins perform over the last 90 days, normalized to a starting value of 1.0?
"""),

    code("""hist = {c: fetch_history(c, days=90)["price"] for c in COINS}
returns = pd.DataFrame(hist)
returns_norm = returns / returns.iloc[0]

fig, ax = plt.subplots(figsize=(11, 5))
palette = {"bitcoin": "#001a70", "ethereum": "#0055d4", "solana": "#10b981"}
for coin, series in returns_norm.items():
    ax.plot(series.index, series.values, lw=1.6, label=coin.title(), color=palette.get(coin))
ax.axhline(1.0, color="#888", lw=0.6, ls="--")
ax.set_title("Cumulative return — last 90 days (normalized to 1.0)",
             fontsize=13, fontweight="bold", color="#001a70")
ax.set_ylabel("Multiplier")
ax.legend(frameon=False, loc="upper left")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
"""),

    md("""## 6️⃣ LLM commentary — let the model **read the numbers**

This is the punchline of the lab. Most "AI crypto bots" feed the LLM a vague prompt like *"is bitcoin going up?"* and get a vague answer back. We do the opposite: we summarize the actual indicator values into a tight numerical brief and ask for the read.
"""),

    code("""latest = btc_ind.dropna().iloc[-1]
prior = btc_ind.dropna().iloc[-2]

brief = f'''
Asset: Bitcoin (USD)
As of: {latest.name.date()}
Last close: ${latest['price']:,.0f}
Prior close: ${prior['price']:,.0f}
24h return: {(latest['price']/prior['price'] - 1) * 100:+.2f}%
SMA(20): ${latest['sma20']:,.0f}
SMA(50): ${latest['sma50']:,.0f}
RSI(14): {latest['rsi14']:.1f}
90-day high: ${btc_ind['price'].max():,.0f}
90-day low:  ${btc_ind['price'].min():,.0f}
'''
print(brief)
"""),

    code("""commentary = client.chat.completions.create(
    model=DEFAULT_CHAT_MODEL,
    messages=[
        {
            "role": "system",
            "content": (
                "You are a sober technical analyst writing for a graduate finance class. "
                "Use ONLY the numbers in the brief. Do not invent news or sentiment. "
                "Write 4-6 sentences covering: trend (vs SMAs), momentum (RSI), and a "
                "single conditional setup ('if price holds X, then Y; else Z'). "
                "End with a one-line risk caveat."
            ),
        },
        {"role": "user", "content": brief},
    ],
    temperature=0.2,
)
pretty_print(commentary.choices[0].message.content,
             title="🧮 Technical commentary", theme="blue")
"""),

    md("""## 7️⃣ Structured trade signal (JSON mode)

Free-form prose is great for humans. For programmatic pipelines you want JSON. Here we ask the same model to emit a strict signal object so we could feed it into a downstream system (a dashboard, a webhook, an alert).
"""),

    code("""import json

signal_response = client.chat.completions.create(
    model=DEFAULT_CHAT_MODEL,
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "system",
            "content": (
                "You are a quantitative-style signal generator. Read the numerical brief "
                "and return JSON with EXACTLY these keys:\\n"
                "{\\n"
                '  "asset": "BTC",\\n'
                '  "regime": "uptrend" | "range" | "downtrend",\\n'
                '  "momentum": "overbought" | "neutral" | "oversold",\\n'
                '  "signal": "buy" | "hold" | "reduce" | "sell",\\n'
                '  "confidence": <float 0-1>,\\n'
                '  "rationale": "<1-2 sentences citing the numbers>"\\n'
                "}\\n"
                "Use ONLY the numbers in the brief. Be conservative — if signals conflict, output 'hold'."
            ),
        },
        {"role": "user", "content": brief},
    ],
    temperature=0,
)

signal = json.loads(signal_response.choices[0].message.content)
pp(signal, title="🚦 Structured signal")
"""),

    md("""## 8️⃣ News summarizer (status updates)

CoinGecko exposes recent project announcements via `/status_updates`. We pull a handful and ask the model to summarize what's actually new — bullets only, no fluff.
"""),

    code("""news_resp = requests.get(
    "https://api.coingecko.com/api/v3/coins/bitcoin/status_updates",
    params={"per_page": 8, "page": 1},
    timeout=20,
)
news_resp.raise_for_status()
items = news_resp.json().get("status_updates", [])
news_text = "\\n\\n".join(
    f"[{u.get('created_at', '?')}] {u.get('description', '').strip()}"
    for u in items
)
print(f"{len(items)} status updates pulled")
"""),

    code("""if news_text.strip():
    summary = client.chat.completions.create(
        model=DEFAULT_MINI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Summarize crypto status updates as a tight bullet list. "
                    "Each bullet: <date> — <one-sentence what happened>. "
                    "Skip duplicates and pure marketing copy."
                ),
            },
            {"role": "user", "content": news_text},
        ],
        temperature=0.1,
    )
    pretty_print(summary.choices[0].message.content,
                 title="📰 News digest", theme="yellow")
else:
    pretty_print("No status updates available right now — try again later.",
                 title="📰 News digest", theme="gray")
"""),

    md("""## 🎯 Hands-on exercise

1. **Pick a different coin** (`solana`, `ethereum`, anything in `COINS`) and re-run the indicator pipeline + chart.
2. **Add Bollinger Bands** (SMA20 ± 2σ) to the price chart. The 20-day rolling std is a one-liner with `.rolling(20).std()`.
3. Modify the **signal prompt** to also output a `time_horizon` field (`"intraday" | "swing" | "position"`). Re-run and inspect.
4. **Reflect** in the cell below: looking at the chart, do you agree with the LLM's signal? Where would a human override it?
"""),

    code("""# Your turn — start here.
my_coin = "ethereum"

eth = compute_indicators(fetch_history(my_coin, days=90))
# (write the rest)
"""),

    md("""---
*Next module — M03 — moves from "AI in action" to controlling exactly what the model says: prompting strategies, structured output, and function calling.*
"""),
]

if __name__ == "__main__":
    build(LAB_PATH, TITLE, EMOJI, DIFFICULTY, TIME, body)
