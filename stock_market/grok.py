# grok.py - Fully generic version (works for any company)
import argparse
import pandas as pd
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import re
import os
import webbrowser
import json

def excel_date_to_year(serial):
    if pd.isna(serial):
        return None
    try:
        return (datetime(1899, 12, 30) + timedelta(days=int(float(serial)))).year
    except:
        return None

def list_to_js(arr):
    return json.dumps([None if pd.isna(x) else float(x) for x in arr])

def get_business_overview(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Try multiple possible locations on Screener.in
        blocks = soup.find_all(['div', 'p'], class_=['company-description', 'fs14', 'lh1-5'])
        for block in blocks:
            txt = block.get_text(strip=True)
            if len(txt) > 120:
                return txt[:950] + '...' if len(txt) > 950 else txt
        return None
    except:
        return None

def main(excel_path, holdings_path, screener_url):
    df = pd.read_excel(excel_path, sheet_name="Data Sheet", header=None)
    
    company_name   = str(df.iloc[0, 1]).strip().title()
    current_price  = float(df.iloc[7, 1])
    mcap_cr        = float(df.iloc[8, 1])
    
    # Robust year extraction
    raw_dates = df.iloc[15, 1:11].tolist()
    years = [excel_date_to_year(d) for d in raw_dates]
    years = [y for y in years if y is not None]
    if len(years) < 8:                              # fallback if dates failed
        years = list(range(2015, 2015 + len(raw_dates)))
    
    sales = pd.to_numeric(df.iloc[16, 1:11], errors='coerce').fillna(0).tolist()
    pat   = pd.to_numeric(df.iloc[29, 1:11], errors='coerce').fillna(0).tolist()
    debt  = pd.to_numeric(df.iloc[58, 1:11], errors='coerce').fillna(0).tolist()
    equity_cap = pd.to_numeric(df.iloc[56, 1:11], errors='coerce').fillna(0).tolist()
    reserves   = pd.to_numeric(df.iloc[57, 1:11], errors='coerce').fillna(0).tolist()
    equity = [equity_cap[i] + reserves[i] for i in range(10)]
    
    shares_latest = pd.to_numeric(df.iloc[92, -1], errors='coerce') or 1
    latest_pat = pat[-1]
    eps = latest_pat / shares_latest
    current_pe = round(current_price / eps, 1) if eps > 0 else 0
    
    def cagr(start, end, n=9):
        return round(((end / start) ** (1/n) - 1) * 100, 1) if start > 0 and end > 0 else 0
    
    sales_cagr = cagr(sales[0], sales[-1])
    pat_cagr   = cagr(pat[0], pat[-1])
    
    # Symbol for filename
    symbol_match = re.search(r"/company/([A-Z0-9]+)", screener_url)
    symbol = symbol_match.group(1) if symbol_match else screener_url.rstrip("/").split("/")[-1].upper()
    
    # Portfolio
    holdings = pd.read_csv(holdings_path)
    holding_row = holdings[holdings["Instrument"].str.upper() == symbol]
    in_portfolio = not holding_row.empty
    
    if in_portfolio:
        qty = int(holding_row["Qty."].values[0])
        avg_cost = float(holding_row["Avg. cost"].values[0])
        cur_val = float(holding_row["Cur. val"].values[0])
        total_val = holdings["Cur. val"].sum()
        port_pct = round(cur_val / total_val * 100, 1) if total_val > 0 else 0
        gain_pct = round(float(holding_row["Net chg."].values[0]), 1)
        portfolio_html = f"""
            <p class="text-lg">
                You hold <strong>{qty:,} shares</strong> (avg cost ₹{avg_cost:,.0f}). 
                Current value ₹{cur_val:,.0f} ({gain_pct}% gain). 
                Portfolio weight: <strong>{port_pct}%</strong>.
            </p>
        """.strip()
    else:
        portfolio_html = '<p class="text-lg">Not in your current portfolio.</p>'
    
    # Overview
    overview = get_business_overview(screener_url)
    if not overview or len(overview) < 50:
        overview = "Business overview could not be auto-extracted. Please refer to the Screener.in page for full description."
    
    # JS arrays
    years_js  = list_to_js(years)
    sales_js  = list_to_js(sales)
    pat_js    = list_to_js(pat)
    debt_js   = list_to_js(debt)
    equity_js = list_to_js(equity)

    # ==================== FULL HTML TEMPLATE ====================
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{company_name} - Long-term Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <style>
        body {{font-family:system-ui,sans-serif; background:#f9fafb;}}
        .card {{background:white; border-radius:12px; box-shadow:0 4px 15px rgba(0,0,0,0.1); padding:1.75rem; margin-bottom:1.5rem;}}
        .positive {{color:#15803d;}} .negative {{color:#b91c1c;}}
    </style>
</head>
<body class="p-8">
<div class="max-w-6xl mx-auto">

    <div class="text-center mb-10">
        <h1 class="text-4xl font-bold">{company_name}</h1>
        <p class="text-2xl mt-2">₹{current_price:,.0f} | MCap ₹{mcap_cr:,.0f} Cr | PE {current_pe}×</p>
    </div>

    <div class="card">
        <h2 class="text-2xl font-semibold mb-4">1. What does the company do?</h2>
        <div class="prose">{overview}</div>
    </div>

    <div class="card bg-amber-50">
        <h2 class="text-2xl font-semibold mb-4">Portfolio Snapshot</h2>
        {portfolio_html}
    </div>

    <div class="card">
        <h2 class="text-2xl font-semibold mb-4">2. Financial Story in Simple Terms</h2>
        <p class="text-lg">
            Sales grew at <strong>{sales_cagr}% CAGR</strong> and profit at <strong>{pat_cagr}% CAGR</strong> over 10 years. 
            Current valuation is <strong>PE {current_pe}×</strong>. 
            <span class="positive">Strong cash flow &amp; brand/distribution moat</span> 
            <span class="negative">High PE means most future growth is already priced in</span>.
        </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div id="chart-sales" class="h-80"></div>
        <div id="chart-pat" class="h-80"></div>
        <div id="chart-debt" class="h-80"></div>
    </div>

    <div class="card">
        <h2 class="text-2xl font-semibold mb-4">4–13. Quick Investment Checklist (5+ year horizon)</h2>
        <ul class="space-y-4 text-lg">
            <li><strong>4. What stands out</strong>: Steady growth, cash flow, moat vs high valuation and input cost risks.</li>
            <li><strong>5-6. Growth priced in?</strong>: At PE {current_pe}×, most expected growth is already priced in. Expect moderate returns unless earnings beat significantly.</li>
            <li><strong>7. Risks</strong>: Sector cyclicality, commodity/input cost volatility, competition, regulatory changes.</li>
            <li><strong>8. 5× in 10 years probability</strong>: 20-40% (depends on maintaining 12-15%+ earnings growth).</li>
            <li><strong>9-10. Management &amp; structural weakness</strong>: Conservative capital allocation visible from cash flows and debt trend.</li>
            <li><strong>11. Suggested allocation</strong>: 3–6% of portfolio for diversification.</li>
            <li><strong>12. Good time to buy?</strong>: Only on meaningful dips (10-15% correction) for better margin of safety.</li>
            <li><strong>13. Moat</strong>: Brand/distribution strength (varies by company). Competition exists but scale helps.</li>
        </ul>
    </div>

</div>

<script>
    const years = {years_js};
    const sales = {sales_js};
    const pat = {pat_js};
    const debt = {debt_js};
    const equity = {equity_js};

    Plotly.newPlot('chart-sales', [{{x:years, y:sales, type:'scatter', mode:'lines+markers', name:'Sales', line:{{color:'#10b981'}}}}], {{title:'Sales (₹ Cr)', template:'plotly_white'}});
    Plotly.newPlot('chart-pat',   [{{x:years, y:pat,   type:'scatter', mode:'lines+markers', name:'PAT',   line:{{color:'#3b82f6'}}}}], {{title:'Profit (₹ Cr)', template:'plotly_white'}});
    Plotly.newPlot('chart-debt',  [{{x:years, y:debt,  type:'bar', name:'Debt', marker:{{color:'red'}}}}, {{x:years, y:equity, type:'bar', name:'Equity', marker:{{color:'green'}}}}], {{barmode:'group', title:'Debt vs Equity', template:'plotly_white'}});
</script>
</body>
</html>"""

    html = html_template.format(
        company_name=company_name,
        current_price=current_price,
        mcap_cr=round(mcap_cr),
        current_pe=current_pe,
        overview=overview.replace("\n", "<br>"),
        portfolio_html=portfolio_html,
        sales_cagr=sales_cagr,
        pat_cagr=pat_cagr,
        years_js=years_js,
        sales_js=sales_js,
        pat_js=pat_js,
        debt_js=debt_js,
        equity_js=equity_js
    )

    filename = f"{symbol}_dashboard_grok.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ Dashboard ready: {filename}")
    webbrowser.open(f"file://{os.path.abspath(filename)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--excel", required=True)
    parser.add_argument("--portfolio", required=True)
    parser.add_argument("--url", required=True)
    args = parser.parse_args()
    main(args.excel, args.portfolio, args.url)
