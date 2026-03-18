import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import argparse
import sys

class MalikAnalyzer:
    def __init__(self, excel_path, portfolio_path, screener_url):
        self.excel_path = excel_path
        self.portfolio_path = portfolio_path
        self.symbol = screener_url.strip('/').split('/')[-1].upper()
        
    def _clean(self, val):
        try:
            if pd.isna(val) or str(val).strip().lower() in ["", "nan", "-"]: return 0.0
            return float(str(val).replace(',', '').replace('%', '').strip())
        except: return 0.0

    def _find_row(self, df, keywords):
        """Finds data by checking multiple label variations."""
        for kw in keywords:
            mask = df.iloc[:, 0].astype(str).str.contains(kw, case=False, na=False)
            if mask.any():
                idx = df[mask].index[0]
                # Extract columns 1 to 11 (the 10 years of data)
                return [self._clean(v) for v in df.iloc[idx, 1:11].tolist()]
        return [0.0] * 10

    def load_and_calculate(self):
        print(f"--- Analyzing {self.symbol}: Joining the Dots ---")
        xls = pd.ExcelFile(self.excel_path)
        # Target the Data Sheet specifically
        sheet = 'Data Sheet' if 'Data Sheet' in xls.sheet_names else xls.sheet_names[-1]
        df = pd.read_excel(xls, sheet_name=sheet, header=None)

        # 1. Row Extraction
        self.sales = self._find_row(df, ["^Sales$"])
        self.pat = self._find_row(df, ["^Net profit$"])
        self.cfo = self._find_row(df, ["Cash from Operating Activity"])
        self.dep = self._find_row(df, ["Depreciation"])
        self.div = self._find_row(df, ["Dividend Amount"])
        self.debt = self._find_row(df, ["Borrowings"])
        
        # Fixed Assets for Capex: Screener uses 'Net Block'
        net_block = self._find_row(df, ["Net Block"])
        cwip = self._find_row(df, ["Capital Work in Progress"])
        assets = [n + c for n, c in zip(net_block, cwip)]
        
        # Calculate annual Capex
        self.capex = [0.0] # First year baseline
        for i in range(1, 10):
            change = assets[i] - assets[i-1]
            self.capex.append(max(0, change + self.dep[i]))

        # 2. The 'Joined Dots' Logic
        self.total_pat = sum(self.pat)
        self.total_cfo = sum(self.cfo)
        self.total_capex = sum(self.capex)
        self.fcf = self.total_cfo - self.total_capex
        
        # Check if growth is faster than debt
        sales_growth = (self.sales[-1] - self.sales[0]) / self.sales[0] if self.sales[0] > 0 else 0
        debt_growth = (self.debt[-1] - self.debt[0]) / self.debt[0] if self.debt[0] > 0 else 0

        self.checks = {
            "Profit is Cash": "PASS" if self.total_cfo > self.total_pat else "FAIL",
            "Free Cash Flow": "PASS" if self.fcf > 0 else "FAIL",
            "Debt Control": "PASS" if sales_growth > debt_growth else "FAIL"
        }

    def generate_report(self):
        years = [f"Y{i+1}" for i in range(10)]
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # The Plot: Visualizing the gap between Cash and Profit
        fig.add_trace(go.Bar(x=years, y=self.sales, name="Sales", marker_color='lightgrey'), secondary_y=False)
        fig.add_trace(go.Scatter(x=years, y=self.pat, name="Net Profit (PAT)", line=dict(color='#2ecc71', width=4)), secondary_y=False)
        fig.add_trace(go.Scatter(x=years, y=self.cfo, name="Cash from Ops (CFO)", line=dict(color='#3498db', width=4, dash='dot')), secondary_y=False)
        
        fig.update_layout(title=f"The Malik Check: {self.symbol}", template="plotly_white", hovermode="x unified")
        chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

        html = f"""
        <html>
        <head>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                .check-card {{ padding: 20px; border-radius: 10px; text-align: center; font-weight: bold; color: white; }}
                .pass {{ background: #27ae60; }} .fail {{ background: #e74c3c; }}
                .val {{ font-size: 24px; font-weight: bold; }}
            </style>
        </head>
        <body class="p-5 bg-light">
            <div class="container bg-white p-5 rounded shadow">
                <h1 class="mb-4">Analysis: {self.symbol}</h1>
                <div class="row g-3 mb-4">
                    <div class="col-md-4"><div class="check-card {'pass' if self.checks['Profit is Cash']=='PASS' else 'fail'}">CFO > PAT: {self.checks['Profit is Cash']}</div></div>
                    <div class="col-md-4"><div class="check-card {'pass' if self.checks['Free Cash Flow']=='PASS' else 'fail'}">FCF > 0: {self.checks['Free Cash Flow']}</div></div>
                    <div class="col-md-4"><div class="check-card {'pass' if self.checks['Debt Control']=='PASS' else 'fail'}">Sales Gr > Debt Gr: {self.checks['Debt Control']}</div></div>
                </div>
                <div class="row text-center mb-5 border-top pt-4">
                    <div class="col-3"><h6>10Y Total PAT</h6><div class="val">₹{self.total_pat:.0f} Cr</div></div>
                    <div class="col-3"><h6>10Y Total CFO</h6><div class="val">₹{self.total_cfo:.0f} Cr</div></div>
                    <div class="col-3"><h6>10Y Total Capex</h6><div class="val">₹{self.total_capex:.0f} Cr</div></div>
                    <div class="col-3"><h6>Free Cash Flow</h6><div class="val">₹{self.fcf:.0f} Cr</div></div>
                </div>
                <div>{chart_html}</div>
            </div>
        </body>
        </html>
        """
        out_file = f"{self.symbol}_Malik_Analysis.html"
        with open(out_file, "w") as f: f.write(html)
        print(f"Success! Open {out_file} to see the result.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--excel", required=True)
    parser.add_argument("--portfolio", required=True)
    parser.add_argument("--url", required=True)
    args = parser.parse_args()

    m = MalikAnalyzer(args.excel, args.portfolio, args.url)
    m.load_and_calculate()
    m.generate_report()