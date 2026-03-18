# ================================================
# DR. VIJAY MALIK ANALYZER 2.1 – FIXED & ROBUST
# Last fix: Proper conditional formatting in PDF f-strings
# Run: python analyze_grok.py --excel "YourCompany.xlsx"
# ================================================

import argparse
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fpdf import FPDF

# ====================== PDF REPORT CLASS ======================
class MalikReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Dr. Vijay Malik Stock Analysis Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} | Powered by Grok ~ Faithful to Dr. Malik Framework', 0, 0, 'C')

    def chapter_title(self, title, color=(0, 0, 0)):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(*color)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(3)
        self.set_text_color(0, 0, 0)

    def key_line(self, label, value, color=(0, 0, 0)):
        self.set_font('Arial', '', 11)
        self.set_text_color(*color)
        self.cell(90, 8, label, 0, 0)
        self.cell(0, 8, str(value), 0, 1)
        self.ln(1)

# ====================== HELPERS ======================
def safe_year(value):
    if pd.isna(value):
        return "NA"
    if isinstance(value, datetime):
        return value.strftime('%Y')
    if isinstance(value, (int, float)) and value > 40000:
        try:
            dt = datetime(1899, 12, 30) + timedelta(days=float(value))
            return dt.strftime('%Y')
        except:
            pass
    if isinstance(value, str):
        try:
            dt = pd.to_datetime(value)
            return dt.strftime('%Y')
        except:
            if len(value) >= 4 and value[:4].isdigit():
                return value[:4]
    return "???"

def cagr(start, end, periods):
    if start <= 0 or periods <= 0:
        return 0.0
    return (end / start) ** (1 / periods) - 1

# ====================== MAIN ANALYSIS ======================
def analyze_company(excel_file):
    df = pd.read_excel(excel_file, sheet_name="Data Sheet", header=None)

    company_name = str(df.iloc[0, 1]).strip() if pd.notna(df.iloc[0, 1]) else "Unknown Company"

    # Current stats
    current_price = float(df.iloc[7, 1]) if pd.notna(df.iloc[7, 1]) else np.nan
    mcap_latest   = float(df.iloc[8, 1]) if pd.notna(df.iloc[8, 1]) else np.nan

    # Latest shares
    shares_cr_latest = None
    for r in [92, 70, 6]:
        if pd.notna(df.iloc[r, -1]):
            try:
                shares_cr_latest = float(df.iloc[r, -1])
                break
            except:
                pass
    if shares_cr_latest is None or shares_cr_latest <= 0:
        shares_cr_latest = mcap_latest / current_price if current_price and mcap_latest and current_price > 0 else 100.0

    # Find Report Date row
    date_row_idx = None
    for i in range(5, 40):
        cell = str(df.iloc[i, 0]).strip().lower()
        if "report date" in cell or "date" in cell:
            date_row_idx = i
            break
    if date_row_idx is None:
        date_row_idx = 15  # default fallback

    years_raw = df.iloc[date_row_idx, 1:11].values
    years = [safe_year(y) for y in years_raw]

    # Safe data extraction
    def safe_float_row(row_idx, col_slice=slice(1,11)):
        try:
            vals = df.iloc[row_idx, col_slice].values
            return np.array([float(v) if pd.notna(v) else np.nan for v in vals])
        except:
            return np.full(10, np.nan)

    sales        = safe_float_row(date_row_idx + 1)
    pat          = safe_float_row(date_row_idx + 14)
    cfo          = safe_float_row(date_row_idx + 66)
    debt         = safe_float_row(date_row_idx + 43)
    equity_cap   = safe_float_row(date_row_idx + 41)
    reserves     = safe_float_row(date_row_idx + 42)
    total_equity = equity_cap + reserves
    div_paid     = safe_float_row(date_row_idx + 15)
    interest     = safe_float_row(date_row_idx + 11)
    nfa          = safe_float_row(date_row_idx + 46)
    cwip         = safe_float_row(date_row_idx + 47)
    cwip         = np.nan_to_num(cwip, nan=0.0)
    receivables  = safe_float_row(date_row_idx + 51)
    inventory    = safe_float_row(date_row_idx + 52)
    inventory    = np.nan_to_num(inventory, nan=0.0)
    dep          = safe_float_row(date_row_idx + 10)
    other_income = safe_float_row(date_row_idx + 9)

    # Fallback PAT for some companies
    if np.all(np.isnan(pat)) and date_row_idx == 15:
        pat = safe_float_row(29)

    # Calculations
    capex = np.full(len(sales), np.nan)
    for i in range(1, len(sales)):
        change = (nfa[i] + cwip[i]) - (nfa[i-1] + cwip[i-1])
        capex[i] = change + dep[i]
    capex[0] = dep[0] if not np.isnan(dep[0]) else 0

    fcf = cfo - capex
    de_ratio     = np.divide(debt, total_equity, where=total_equity!=0, out=np.full_like(debt, np.nan))
    roe          = np.divide(pat * 100, total_equity, where=total_equity!=0, out=np.full_like(pat, np.nan))
    roce         = np.divide((pat + interest) * 100, (total_equity + debt), where=(total_equity + debt)!=0, out=np.full_like(pat, np.nan))
    int_coverage = np.divide(pat + interest, interest, where=interest!=0, out=np.full_like(pat, np.inf))
    rec_days     = np.divide(receivables * 365, sales, where=sales!=0, out=np.full_like(sales, np.nan))
    inv_days     = np.divide(inventory * 365, sales, where=sales!=0, out=np.full_like(sales, 0))
    wc_cycle     = rec_days + inv_days
    fcfe         = fcf - interest
    net_cash_gen = fcf + other_income - interest - div_paid

    total_re_10y = np.nansum(pat - div_paid)
    old_price    = float(df.iloc[89, 1]) if pd.notna(df.iloc[89, 1]) else np.nan
    old_shares   = float(df.iloc[69, 1]) if pd.notna(df.iloc[69, 1]) else np.nan
    old_mcap     = old_price * old_shares / 1e7 if old_price and old_shares else 0
    mcap_increase = mcap_latest - old_mcap if not np.isnan(mcap_latest) else 0
    value_per_re  = mcap_increase / total_re_10y if total_re_10y != 0 else 0
    mcap_cagr_10y = cagr(old_mcap, mcap_latest, 10) * 100

    sales_gr = np.diff(sales) / sales[:-1] * 100
    sales_gr = np.nan_to_num(sales_gr, nan=0.0, posinf=0.0, neginf=0.0)
    sales_vol = np.nanstd(sales_gr)
    avg_sales_gr_5y = np.nanmean(sales_gr[-5:]) if len(sales_gr) >= 5 else 0

    # TTM PE
    q_pat_row = 48 if 48 < len(df) else None
    q_pat = safe_float_row(q_pat_row) if q_pat_row else np.zeros(10)
    ttm_pat = np.nansum(q_pat[-4:]) if len(q_pat) >= 4 else pat[-1] if len(pat)>0 else 0
    ttm_pe = mcap_latest / ttm_pat if ttm_pat > 0 else np.nan

    # Scores
    moat = 0
    if not np.isnan(roce[-1]): moat += 3 if roce[-1] > 25 else (1 if roce[-1] > 15 else 0)
    if not np.isnan(wc_cycle[-1]): moat += 2 if wc_cycle[-1] < 90 else 0
    moat += 2 if np.nanmean(fcf / np.where(cfo == 0, 1, cfo)) > 0.6 else 0
    if len(roe) >= 5: moat += 3 if np.nanmean(roe[-5:]) > 18 else 0
    moat = min(10, max(0, moat))

    mgmt = 0
    if value_per_re > 8: mgmt += 4
    elif value_per_re > 3: mgmt += 2
    if not np.isnan(de_ratio[-1]): mgmt += 3 if de_ratio[-1] < 0.3 else 0
    mgmt += 3 if mcap_cagr_10y > 18 else 0
    mgmt = min(10, max(0, mgmt))

    cyclical_score = 10 if sales_vol < 18 else (6 if sales_vol < 30 else 2)

    red_flags = []
    if not np.isnan(de_ratio[-1]) and de_ratio[-1] > 0.6: red_flags.append("Significant Debt")
    if np.sum(fcf[-3:] < 0) >= 2: red_flags.append("Recent negative FCF")
    recent_cov = int_coverage[-3:]
    if np.any(recent_cov < 4) and not np.isinf(recent_cov).all(): red_flags.append("Weak interest coverage recent")

    # DCF
    last_fcf = fcf[-1] if not np.isnan(fcf[-1]) else 0
    g = min(max(avg_sales_gr_5y / 100, 0.07), 0.18)
    r = 0.135
    tg = 0.06
    proj = [last_fcf * (1 + g)**i for i in range(1, 6)]
    tv = proj[-1] * (1 + tg) / (r - tg) if r > tg else 0
    pv = sum(p / (1 + r)**i for i, p in enumerate(proj, 1)) + tv / (1 + r)**5
    net_cash = float(df.iloc[68, -1]) if pd.notna(df.iloc[68, -1]) else 0
    ev = pv + net_cash - (debt[-1] if not np.isnan(debt[-1]) else 0)
    intrinsic_ps = ev / shares_cr_latest if shares_cr_latest > 0 else 0

    # ====================== PDF GENERATION ======================
    pdf_name = f"{company_name.replace(' ', '_')}_Malik_Report.pdf"
    pdf = MalikReportPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 15, company_name, 0, 1, 'C')
    pdf.set_font('Arial', '', 11)

    # Fixed formatting
    price_display = f"{current_price:.1f}" if not np.isnan(current_price) else "N/A"
    mcap_display  = f"{mcap_latest:.0f}"  if not np.isnan(mcap_latest)  else "N/A"
    pdf.cell(0, 10, f"Price: Rs. {price_display} | Mcap: Rs. {mcap_display} Cr", 0, 1, 'C')
    pdf.ln(8)

    pdf.chapter_title("1. Debt & Safety", (0,100,0) if (not np.isnan(de_ratio[-1]) and de_ratio[-1] < 0.3) else (180,0,0))
    pdf.key_line("Debt/Equity latest:", f"{de_ratio[-1]:.2f}" if not np.isnan(de_ratio[-1]) else "N/A")
    pdf.key_line("Interest Coverage latest:", f"{int_coverage[-1]:.1f}x" if not np.isinf(int_coverage[-1]) else ">50x")

    pdf.chapter_title("2. Growth & Returns")
    pdf.key_line("Sales CAGR ~10Y:", f"{cagr(sales[0], sales[-1], 10)*100:.1f}%")
    pdf.key_line("ROE latest:", f"{roe[-1]:.1f}%" if not np.isnan(roe[-1]) else "N/A")
    pdf.key_line("ROCE latest:", f"{roce[-1]:.1f}%" if not np.isnan(roce[-1]) else "N/A")

    pdf.chapter_title("3. Cash Flow Quality", (0,100,0))
    pdf.key_line("Latest FCF:", f"Rs. {fcf[-1]:.1f} Cr" if not np.isnan(fcf[-1]) else "N/A")
    pdf.key_line("Net Cash Gen latest:", f"Rs. {net_cash_gen[-1]:.1f} Cr" if not np.isnan(net_cash_gen[-1]) else "N/A")
    pdf.key_line("Value per Rs. 1 Retained:", f"Rs. {value_per_re:.1f}")

    pdf.chapter_title("4. Efficiency")
    pdf.key_line("WC Cycle latest:", f"{wc_cycle[-1]:.0f} days" if not np.isnan(wc_cycle[-1]) else "N/A")

    pdf.chapter_title("5. Scores")
    pdf.key_line("Moat Score:", f"{moat}/10", (0,128,0) if moat >= 7 else (200,100,0))
    pdf.key_line("Management Score:", f"{mgmt}/10", (0,128,0) if mgmt >= 7 else (200,100,0))
    pdf.key_line("Cyclicality:", "Low" if cyclical_score >= 8 else "Medium/High")

    pdf.chapter_title("6. Intrinsic Value (DCF)")
    pdf.key_line("Growth used:", f"{g*100:.1f}%")
    pdf.key_line("Intrinsic value/share:", f"Rs. {intrinsic_ps:.1f}")
    pdf.key_line("vs Current:", "Undervalued" if current_price < intrinsic_ps * 0.9 else "Fair/Priced high" if not np.isnan(current_price) else "N/A")

    pdf.chapter_title("7. Red Flags")
    if red_flags:
        pdf.set_text_color(200, 0, 0)
        for f in red_flags:
            pdf.cell(0, 8, f"⚠ {f}", 0, 1)
    else:
        pdf.set_text_color(0, 128, 0)
        pdf.cell(0, 8, "No major red flags detected", 0, 1)

    pdf.add_page()
    pdf.chapter_title("FINAL VERDICT", (0,100,0))
    pdf.set_font('Arial', 'B', 14)
    verdict = "WORTH WATCHING"
    if moat >= 7 and mgmt >= 6 and not red_flags:
        verdict = "STRONG LONG-TERM CANDIDATE"
    if red_flags:
        verdict = "CAUTION – Review Red Flags"
    pdf.multi_cell(0, 10, verdict)
    pdf.ln(5)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 8, "Based on Dr. Vijay Malik philosophy.\nDebt-free + high & sustained ROCE + strong FCF + shareholder value creation are key.\nAlways cross-check & do your own research.")

    pdf.output(pdf_name)
    print(f"Report generated: {pdf_name}")
    print(f"Company: {company_name} | Moat: {moat}/10 | Mgmt: {mgmt}/10 | Verdict: {verdict}")

# ====================== COMMAND LINE ======================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dr Vijay Malik Analyzer – Robust Version")
    parser.add_argument('--excel', required=True, help="Path to Screener.in Excel file")
    args = parser.parse_args()
    analyze_company(args.excel)