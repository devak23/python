#!/usr/bin/env python3
"""
Long-Term Investor Dashboard Generator  v3
Usage: python analyze_company.py <excel.xlsx> <holdings.csv> <screener_url> [--output out.html]
"""
import sys, argparse, json, re
from pathlib import Path
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import os
import webbrowser

# ─────────────────────── helpers ───────────────────────
def sf(v):
    try:
        if v is None: return None
        s = str(v).strip().replace(',','')
        return None if s in ('','None','nan','-') else float(s)
    except: return None

def nz(lst): return [v for v in lst if v is not None]

def latest(lst):
    for v in reversed(lst):
        if v is not None: return v
    return None

def avg(lst):
    v = nz(lst); return sum(v)/len(v) if v else None

def cagr(s, e, y):
    if not s or not e or s<=0 or e<=0 or y<=0: return None
    return (e/s)**(1/y)-1

def pct(v, d=1): return f"{v*100:.{d}f}%" if v is not None else "N/A"
def cr(v):
    if v is None: return "N/A"
    return f"₹{v/1000:,.1f}K Cr" if abs(v)>=1000 else f"₹{v:,.0f} Cr"
def fmt(v, d=1): return f"{v:,.{d}f}" if v is not None else "N/A"

def trend(lst):
    """Return 'improving','declining','stable','volatile' for a series."""
    v = [x for x in lst if x is not None]
    if len(v)<3: return "insufficient data"
    half = len(v)//2
    early = sum(v[:half])/half; late = sum(v[half:])/half
    diff = (late-early)/abs(early) if early else 0
    swings = sum(1 for i in range(1,len(v)) if (v[i]-v[i-1])*(v[i-1]-v[i-2] if i>1 else 0)<0)
    if swings > len(v)//2: return "volatile"
    if diff > 0.15: return "improving"
    if diff < -0.15: return "declining"
    return "stable"

def color_class(v, good_above=None, bad_below=None, good_below=None, bad_above=None):
    if v is None: return ""
    if good_above and v >= good_above: return "good"
    if bad_above  and v >  bad_above:  return "bad"
    if bad_below  and v <  bad_below:  return "bad"
    if good_below and v <= good_below: return "good"
    return "warn"

def jsa(lst):
    out=[]
    for v in lst:
        out.append(round(v,2) if isinstance(v,float) else (v if isinstance(v,int) else None))
    return json.dumps(out)

def jsl(lst): return json.dumps([str(v) if v is not None else "" for v in lst])


# ─────────────────────── excel extraction ───────────────────────
def extract_excel(path):
    wb  = load_workbook(path, data_only=True)
    wsd = wb[wb.sheetnames[3]]   # Data Sheet

    def R(r,c): return sf(wsd.cell(r,c).value)
    def arr(row): return [R(row,c) for c in range(2,12)]
    def yr(v):
        """Convert cell value to 4-digit year int, safely handling None/NaT/NaN."""
        if v is None: return None
        try:
            ts = pd.Timestamp(v)
            if ts is pd.NaT: return None
            y = ts.year
            if y != y: return None   # float NaN check (NaN != NaN is True)
            return int(y)
        except: return None

    d = {}
    d['company_name']  = str(wsd.cell(1,2).value or '').strip()
    d['current_price'] = R(8,2)
    d['market_cap']    = R(9,2)

    d['years']     = [yr(wsd.cell(16,c).value) for c in range(2,12)]
    d['fy_labels'] = [f"FY{y%100:02d}" if y is not None else '' for y in d['years']]

    d['sales']    = arr(17); d['rm']    = arr(18); d['ci']   = arr(19)
    d['pf']       = arr(20); d['omfr']  = arr(21); d['emp']  = arr(22)
    d['sa']       = arr(23); d['oe']    = arr(24); d['oi']   = arr(25)
    d['dep']      = arr(26); d['int']   = arr(27); d['pbt']  = arr(28)
    d['tax']      = arr(29); d['pat']   = arr(30); d['div']  = arr(31)

    d['eq_cap']   = arr(57); d['res']   = arr(58); d['borrow']= arr(59)
    d['nb']       = arr(62); d['cwip']  = arr(63); d['recv'] = arr(67)
    d['inv_bs']   = arr(68); d['cash']  = arr(69); d['adj_sh']= arr(93)

    d['cfo'] = arr(82); d['cfi'] = arr(83); d['cff'] = arr(84)
    d['hp']  = arr(90)   # historical year-end prices

    def ql(v):
        try:
            dt=pd.Timestamp(v); m=dt.month
            q={6:'Q1',9:'Q2',12:'Q3',3:'Q4'}.get(m,f"M{m}")
            fy=(dt.year+1)%100 if m>=4 else dt.year%100
            return f"{q} FY{fy:02d}"
        except: return ''

    d['q_dates']   = [ql(wsd.cell(41,c).value) for c in range(2,12)]
    d['q_sales']   = [sf(wsd.cell(42,c).value) for c in range(2,12)]  # Revenue
    d['q_exp']     = [sf(wsd.cell(43,c).value) for c in range(2,12)]  # Total Expenses
    d['q_oi']      = [sf(wsd.cell(44,c).value) for c in range(2,12)]  # Other Income
    d['q_dep']     = [sf(wsd.cell(45,c).value) for c in range(2,12)]  # Depreciation
    d['q_int']     = [sf(wsd.cell(46,c).value) for c in range(2,12)]  # Interest
    d['q_pbt']     = [sf(wsd.cell(47,c).value) for c in range(2,12)]  # PBT
    d['q_tax']     = [sf(wsd.cell(48,c).value) for c in range(2,12)]  # Tax
    d['q_pat']     = [sf(wsd.cell(49,c).value) for c in range(2,12)]  # Net Profit
    d['q_op']      = [sf(wsd.cell(50,c).value) for c in range(2,12)]  # Operating Profit

    # Derived quarterly metrics
    d['q_opm'] = [round(o/s*100,1) if s and o else None
                  for o,s in zip(d['q_op'], d['q_sales'])]
    d['q_npm'] = [round(p/s*100,1) if s and p else None
                  for p,s in zip(d['q_pat'], d['q_sales'])]

    # YoY growth — same quarter vs one year prior (i-4)
    d['q_sales_yoy'] = [None]*4 + [
        round((d['q_sales'][i]/d['q_sales'][i-4]-1)*100, 1)
        if d['q_sales'][i] and d['q_sales'][i-4] else None
        for i in range(4, 10)
    ]
    d['q_pat_yoy'] = [None]*4 + [
        round((d['q_pat'][i]/d['q_pat'][i-4]-1)*100, 1)
        if d['q_pat'][i] and d['q_pat'][i-4] else None
        for i in range(4, 10)
    ]
    d['q_op_yoy'] = [None]*4 + [
        round((d['q_op'][i]/d['q_op'][i-4]-1)*100, 1)
        if d['q_op'][i] and d['q_op'][i-4] else None
        for i in range(4, 10)
    ]

    # ── derived metrics ──────────────────────────────────────────
    n=10
    d['equity'] = [(d['eq_cap'][i] or 0)+(d['res'][i] or 0) for i in range(n)]

    # Operating Profit (excl dep, int, other income)
    d['op'] = []
    for i in range(n):
        s=d['sales'][i]
        if s:
            d['op'].append(round(s-(d['rm'][i] or 0)-(d['ci'][i] or 0)-(d['pf'][i] or 0)
                                   -(d['omfr'][i] or 0)-(d['emp'][i] or 0)-(d['sa'][i] or 0)-(d['oe'][i] or 0),2))
        else: d['op'].append(None)

    d['opm']    = [round(o/s*100,2) if s and o else None for o,s in zip(d['op'],d['sales'])]
    d['npm']    = [round(p/s*100,2) if s and p else None for p,s in zip(d['pat'],d['sales'])]

    # helper: safe average of two values that may be None
    def savg(a, b):
        if a is not None and b is not None: return (a + b) / 2
        return a if a is not None else b   # fall back to whichever is available

    # ROE = PAT / avg equity
    d['roe'] = []
    for i in range(n):
        e1=d['equity'][i]; e0=d['equity'][i-1] if i>0 else e1
        ae=savg(e1, e0)
        d['roe'].append(round(d['pat'][i]/ae*100,2) if ae and d['pat'][i] else None)

    # ROCE = EBIT (PBT+Int) / avg capital employed (equity+debt)
    d['roce'] = []
    for i in range(n):
        ebit=(d['pbt'][i] or 0)+(d['int'][i] or 0)
        ce1=(d['equity'][i] or 0)+(d['borrow'][i] or 0)
        ce0=((d['equity'][i-1] or 0)+(d['borrow'][i-1] or 0)) if i>0 else ce1
        ace=savg(ce1, ce0)
        d['roce'].append(round(ebit/ace*100,2) if ace else None)

    # PBT/avg NFA  (Dr VM benchmark: <10% bad, >25% excellent)
    d['pbt_nfa'] = []
    for i in range(n):
        n1=d['nb'][i]; n0=d['nb'][i-1] if i>0 else n1
        an=savg(n1, n0)
        d['pbt_nfa'].append(round((d['pbt'][i] or 0)/an*100,2) if an else None)

    # SSGR = NPM x NFA_turnover x (1 - dividend_payout)   [Dr VM definition]
    # It is the maximum growth rate achievable without additional debt
    d['ssgr'] = []
    for i in range(n):
        s=d['sales'][i]; p=d['pat'][i]; dv=(d['div'][i] or 0); nfa=d['nb'][i]
        if s and p and nfa and p>0:
            d['ssgr'].append(round((p/s)*(s/nfa)*(1-dv/p)*100,1))
        else: d['ssgr'].append(None)

    # NFA Turnover
    d['nfat'] = []
    for i in range(n):
        n1=d['nb'][i]; n0=d['nb'][i-1] if i>0 else n1
        an=savg(n1, n0)
        d['nfat'].append(round(d['sales'][i]/an,2) if an and d['sales'][i] else None)

    # Receivables days  (Dr VM: lower = better)
    d['rec_days'] = []
    for i in range(n):
        r1=d['recv'][i]; r0=d['recv'][i-1] if i>0 else r1
        ar=savg(r1, r0)
        d['rec_days'].append(round(365/(d['sales'][i]/ar),1) if d['sales'][i] and ar else None)

    # Inventory turnover
    d['inv_turn'] = []
    for i in range(n):
        i1=d['inv_bs'][i]; i0=d['inv_bs'][i-1] if i>0 else i1
        ai=savg(i1, i0)
        d['inv_turn'].append(round(d['sales'][i]/ai,2) if ai and d['sales'][i] else None)

    # Months of RM held as inventory
    d['rm_months'] = []
    for i in range(n):
        i1=d['inv_bs'][i]; i0=d['inv_bs'][i-1] if i>0 else i1
        ai=savg(i1, i0)
        rmc=(d['rm'][i] or 0)+(d['ci'][i] or 0)
        d['rm_months'].append(round((ai/rmc)*12,1) if rmc and ai else None)

    d['inv_days'] = [round(365/it,1) if it else None for it in d['inv_turn']]
    d['wc_days']  = [round((r or 0)+(i or 0),1) for r,i in zip(d['rec_days'],d['inv_days'])]

    # Capex
    d['capex']=[None]
    for i in range(1,n):
        nb1=d['nb'][i]; nb0=d['nb'][i-1]
        cw1=d['cwip'][i] or 0; cw0=d['cwip'][i-1] or 0
        dep=d['dep'][i] or 0
        if nb1 is not None and nb0 is not None:
            d['capex'].append(round((nb1-nb0)+(cw1-cw0)+dep, 2))
        else:
            d['capex'].append(None)

    d['fcf']=[round(c-(k or 0),2) if c else None for c,k in zip(d['cfo'],d['capex'])]

    # D/E
    d['de']=[round(b/e,2) if e>0 and b is not None else None for b,e in zip(d['borrow'],d['equity'])]

    # Interest coverage: Dr VM uses OP / (cost_of_funds x avg_debt)  at 12%
    COF=0.12
    d['ic_dvm']=[]
    for i in range(n):
        b1=d['borrow'][i]; b0=d['borrow'][i-1] if i>0 else b1
        ab=savg(b1, b0)
        outgo=COF*ab if ab is not None else None
        d['ic_dvm'].append(round(d['op'][i]/outgo,2) if outgo and d['op'][i] else None)

    # EPS & PE history
    d['eps']=[round(p/s,2) if s and s>0 and p else None for p,s in zip(d['pat'],d['adj_sh'])]
    d['pe_h']=[round(h/e,1) if h and e and e>0 else None for h,e in zip(d['hp'],d['eps'])]

    # Dividend payout %
    d['dpay']=[round((d['div'][i] or 0)/d['pat'][i]*100,1) if d['pat'][i] and d['pat'][i]>0 else None for i in range(n)]

    # Retained earnings
    d['retained']=[(d['pat'][i] or 0)-(d['div'][i] or 0) for i in range(n)]

    # Value per ₹1 retained (Mcap increase / total RE)
    total_re=sum(x for x in d['retained'] if x)
    oldest_sh=latest(d['adj_sh'])
    oldest_mcap=(d['hp'][0]*oldest_sh) if d['hp'][0] and oldest_sh else None
    d['oldest_mcap']  = oldest_mcap
    d['mcap_increase']= round(d['market_cap']-oldest_mcap,2) if oldest_mcap else None
    d['vpr']  = round(d['mcap_increase']/total_re,2) if total_re and d['mcap_increase'] and total_re>0 else None
    d['total_re'] = total_re

    # MCap CAGR
    yspan=len([y for y in d['years'] if y])-1
    d['mcap_cagr']=cagr(oldest_mcap,d['market_cap'],yspan) if oldest_mcap else None

    # FCF/CFO (10yr)
    tot_cfo=sum(c for c in d['cfo'] if c)
    tot_fcf=sum(f for f in d['fcf'][1:] if f)
    d['fcf_cfo']=round(tot_fcf/tot_cfo*100,1) if tot_cfo else None

    # Incremental ROE 3yr rolling
    d['inc_roe']=[]
    for i in range(n):
        if i<3: d['inc_roe'].append(None); continue
        cum_re=sum(d['retained'][i-3:i])
        dpat=(d['pat'][i] or 0)-(d['pat'][i-3] or 0)
        d['inc_roe'].append(round(dpat/cum_re*100,1) if cum_re else None)

    # Cost % of sales (latest year)
    i=n-1; s=d['sales'][i] or 1
    d['costs_pct']={
        'Raw Material': round(((d['rm'][i] or 0)+(d['ci'][i] or 0))/s*100,1),
        'Power & Fuel':  round((d['pf'][i] or 0)/s*100,1),
        'Employee':      round((d['emp'][i] or 0)/s*100,1),
        'Selling & Admin':round((d['sa'][i] or 0)/s*100,1),
        'Other Mfr':     round((d['omfr'][i] or 0)/s*100,1),
    }

    # Sales/PAT CAGR
    def gcagr(series):
        s=[v for v in series if v is not None]
        r={}
        if len(s)>=10: r['10y']=cagr(s[0],s[-1],9)
        if len(s)>=8:  r['7y'] =cagr(s[-8],s[-1],7)
        if len(s)>=6:  r['5y'] =cagr(s[-6],s[-1],5)
        if len(s)>=4:  r['3y'] =cagr(s[-4],s[-1],3)
        if len(s)>=2:  r['ttm']=cagr(s[-2],s[-1],1)
        return r
    d['sales_cagr']=gcagr(d['sales']); d['pat_cagr']=gcagr(d['pat'])
    d['bv_cagr']   =gcagr(d['equity']); d['eps_cagr']=gcagr(d['eps'])
    d['div_cagr']  =gcagr([x for x in d['div'] if x])

    # Current PE/PB
    cur_eps=latest(d['eps'])
    d['pe']=round(d['current_price']/cur_eps,2) if cur_eps and cur_eps>0 else None
    d['avg_pe']=avg(d['pe_h'])
    d['pe_min']=round(min(v for v in d['pe_h'] if v),1) if any(d['pe_h']) else None
    d['pe_max']=round(max(v for v in d['pe_h'] if v),1) if any(d['pe_h']) else None
    le=latest(d['equity']); ls=latest(d['adj_sh'])
    bvps=round(le/ls,2) if le and ls else None
    d['pb']=round(d['current_price']/bvps,2) if bvps and bvps>0 else None
    d['pe_pb']=round(d['pe']*d['pb'],1) if d['pe'] and d['pb'] else None

    # TTM figures from quarterly
    d['ttm_sales']=sum(v for v in d['q_sales'][-4:] if v)
    d['ttm_pat']  =sum(v for v in d['q_pat'][-4:]  if v)
    lsh=latest(d['adj_sh'])
    d['ttm_eps']=round(d['ttm_pat']/lsh,2) if lsh and d['ttm_pat'] else cur_eps
    d['pe_ttm']=round(d['current_price']/d['ttm_eps'],2) if d['ttm_eps'] and d['ttm_eps']>0 else d['pe']

    # Div yield
    ld=latest(d['div']); lsh2=latest(d['adj_sh'])
    dps=round(ld/lsh2,2) if ld and lsh2 and lsh2>0 else None
    d['div_yield']=round(dps/d['current_price'],4) if dps and d['current_price'] else None

    # ── COMPLETE METRIC SET — all remaining Sheet 2 metrics ────────────────

    # Tax rate % = Tax / PBT  (spikes indicate deferred tax / one-offs)
    d['tax_pct'] = [round(d['tax'][i]/d['pbt'][i]*100,1)
                    if d['pbt'][i] and d['pbt'][i]!=0 and d['tax'][i] is not None
                    else None for i in range(n)]

    # EBITDA = Operating Profit + Other Income  (Dr VM definition)
    d['ebitda'] = [round((d['op'][i] or 0)+(d['oi'][i] or 0),2)
                   if d['op'][i] is not None else None for i in range(n)]
    d['ebitda_margin'] = [round(e/s*100,1) if s and e else None
                          for e,s in zip(d['ebitda'],d['sales'])]

    # Depreciation % of NFA  (proxy for asset age / useful life remaining)
    d['dep_pct_nfa'] = [round(d['dep'][i]/(d['nb'][i] or 1)*100,1)
                        if d['nb'][i] and d['dep'][i] is not None else None for i in range(n)]

    # Interest Outgo at Dr VM's conservative 12% cost of funds on avg debt
    d['int_outgo'] = []
    for i in range(n):
        b1=d['borrow'][i]; b0=d['borrow'][i-1] if i>0 else b1
        ab=savg(b1,b0)
        d['int_outgo'].append(round(0.12*ab,2) if ab is not None else None)

    # FCFE1 = FCF - Interest expense from P&L
    d['fcfe1'] = [round((d['fcf'][i] or 0)-(d['int'][i] or 0),2)
                  if d['fcf'][i] is not None else None for i in range(n)]

    # FCFE2 = FCFE1 + Other Income  (total free cash to equity holders)
    d['fcfe2'] = [round((d['fcfe1'][i] or 0)+(d['oi'][i] or 0),2)
                  if d['fcfe1'][i] is not None else None for i in range(n)]

    # Net Cash Generation = FCF + OI + delta_Debt - Interest - Dividends
    # Answers: is the company self-funding or does cash keep draining?
    d['net_cash_gen'] = []
    for i in range(1,n):
        delta_debt = (d['borrow'][i] or 0) - (d['borrow'][i-1] or 0)
        ncg = ((d['fcf'][i] or 0) + (d['oi'][i] or 0)
               + delta_debt - (d['int'][i] or 0) - (d['div'][i] or 0))
        d['net_cash_gen'].append(round(ncg,2) if d['fcf'][i] is not None else None)
    d['net_cash_gen'].insert(0, None)   # no value for year 0

    # Surplus funds (cumulative net cash generation)
    d['surplus_funds'] = []
    cumulative = 0
    for v in d['net_cash_gen']:
        if v is not None:
            cumulative += v
            d['surplus_funds'].append(round(cumulative,2))
        else:
            d['surplus_funds'].append(None)

    # Cash + Investments (current + non-current investments + cash & bank)
    inv_arr = [sf(wsd.cell(64,c).value) for c in range(2,12)]  # Investments
    d['cash_invest'] = [round((d['cash'][i] or 0)+(inv_arr[i] or 0),2) for i in range(n)]

    # Other income vs cash+investments health check
    # If OI < 5% × cash_invest, OI is suspiciously low (or cash is idle)
    d['oi_yield_on_cash'] = [round((d['oi'][i] or 0)/(d['cash_invest'][i] or 1)*100,1)
                              if d['cash_invest'][i] else None for i in range(n)]

    # Market cap history = hist_price × adj_shares
    d['mcap_hist'] = [round(d['hp'][i]*d['adj_sh'][i],1)
                      if d['hp'][i] and d['adj_sh'][i] else None for i in range(n)]

    # Share dilution — explicit shares added / (bonus / rights / ESOP)
    sh_start = d['adj_sh'][0]; sh_end = latest(d['adj_sh'])
    d['share_dilution_pct'] = round((sh_end-sh_start)/sh_start*100,2) if sh_start and sh_end else None
    d['adj_sh_series'] = d['adj_sh']   # for chart

    # Reinvestment rate = Capex / (Depreciation + FCF)
    # > 1 = spending more than steady-state; < 0.5 = harvesting the business
    d['reinvestment_rate'] = []
    for i in range(n):
        cap = d['capex'][i]; dep = d['dep'][i] or 0; fcf_v = d['fcf'][i]
        denom = dep + (fcf_v or 0)
        d['reinvestment_rate'].append(round(cap/denom,2) if cap and denom and denom!=0 else None)

    # Debt change 10 years
    d['debt_change_10y'] = round((d['borrow'][-1] or 0)-(d['borrow'][0] or 0),2)                            if d['borrow'][0] is not None else None

    # Total dividends paid 10 years vs total FCFE2
    d['total_div_10y'] = sum(v for v in d['div'] if v)
    d['total_fcfe2_10y'] = sum(v for v in d['fcfe2'] if v)
    d['div_vs_fcfe2']  = round(d['total_div_10y']/d['total_fcfe2_10y']*100,1)                          if d['total_fcfe2_10y'] and d['total_fcfe2_10y']>0 else None

    # Cyclicality score — how many years did PAT decline?
    pats_valid = [v for v in d['pat'] if v is not None]
    d['pat_down_years']  = sum(1 for i in range(1,len(pats_valid)) if pats_valid[i] < pats_valid[i-1])
    d['sales_down_years']= sum(1 for i in range(1,len([v for v in d['sales'] if v])) if
                                [v for v in d['sales'] if v][i] < [v for v in d['sales'] if v][i-1])

    # Cost trend analysis — are costs as % of sales improving or worsening?
    def cost_series(cost_arr):
        return [round((c or 0)/(s or 1)*100,1) if s else None
                for c,s in zip(cost_arr, d['sales'])]

    d['rm_pct_series']   = cost_series([(d['rm'][i] or 0)+(d['ci'][i] or 0) for i in range(n)])
    d['emp_pct_series']  = cost_series(d['emp'])
    d['sa_pct_series']   = cost_series(d['sa'])
    d['pf_pct_series']   = cost_series(d['pf'])
    d['oe_pct_series']   = cost_series(d['oe'])
    d['omfr_pct_series'] = cost_series(d['omfr'])

    # Absolute NFA + CWIP (capacity expansion signal)
    d['nfa_plus_cwip'] = [round((d['nb'][i] or 0)+(d['cwip'][i] or 0),2) for i in range(n)]

    return d


# ─────────────────────── holdings ───────────────────────
def extract_holdings(path):
    df=pd.read_csv(path); df.columns=[c.strip() for c in df.columns]
    recs=[]; ti=tv=0
    for _,row in df.iterrows():
        inv=sf(row.get('Invested',0)) or 0; val=sf(row.get('Cur. val',inv)) or inv
        ti+=inv; tv+=val
        recs.append({'name':str(row.get('Instrument','')).strip(),
                     'qty':sf(row.get('Qty.',0)),'avg_cost':sf(row.get('Avg. cost',0)),
                     'ltp':sf(row.get('LTP',0)),'invested':inv,'cur_val':val,
                     'pnl':sf(row.get('P&L',0)) or (val-inv),'net_chg':sf(row.get('Net chg.',0)) or 0})
    return recs,ti,tv


# ─────────────────────── screener scrape ───────────────────────
def scrape_screener(url):
    """
    Scrapes screener.in company page.
    Captures the full About + Key Points content (including the hidden 'Read More' section
    which is server-rendered in the DOM under div.about-section > div.expanded).
    """
    info = {'about': '', 'key_points': [], 'pros': [], 'cons': [],
            'sector': '', 'industry': '', 'peers': []}
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'}
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            return info
        soup = BeautifulSoup(r.text, 'html.parser')

        # ── About + Key Points ───────────────────────────────────────────────
        # Screener structure inside div.about-section:
        #   <p>Short visible summary</p>
        #   <div class="expanded">          ← hidden by CSS but fully in the DOM
        #     <h2>Key Points</h2>
        #     <ul><li>Segments & Presence: ...</li>
        #         <li>Digital Services: ...</li> ...
        #     </ul>
        #     ... more sub-sections (Market Leadership, Revenue Split, etc.) ...
        #   </div>
        #   <a class="read-more">Read More</a>
        # We extract everything — the visible paragraph AND all key-point sections.

        about_div = soup.find('div', class_='about-section')
        if about_div:
            # 1. Opening paragraph = the always-visible company description
            first_p = about_div.find('p')
            if first_p:
                info['about'] = first_p.get_text(separator=' ', strip=True)

            # 2. Walk sub-sections: each has a heading (h2/h3/strong) + list items / paragraphs
            SKIP_LABELS = {'about', 'key points', 'read more', 'edit',
                           '[edit]', 'about [edit]', 'key points [edit]'}
            sections = []
            cur_heading = None
            cur_lines   = []

            def flush_section():
                lines = [l for l in cur_lines if l.strip()]
                if cur_heading and lines:
                    sections.append({'heading': cur_heading, 'lines': lines})
                elif lines and not cur_heading:
                    # Headingless content — append to about paragraph
                    extra = ' '.join(lines)
                    if extra and extra not in info['about']:
                        info['about'] = (info['about'] + ' ' + extra).strip()

            for el in about_div.descendants:
                if not hasattr(el, 'name') or el.name is None:
                    continue
                if el.name in ('h2', 'h3', 'h4', 'strong'):
                    txt = el.get_text(strip=True)
                    if txt.lower() in SKIP_LABELS or not txt:
                        continue
                    flush_section()
                    cur_heading = txt
                    cur_lines   = []
                elif el.name == 'li':
                    # Only grab direct text; avoid double-counting nested elements
                    line = el.get_text(separator=' ', strip=True)
                    if line:
                        cur_lines.append(line)
                elif el.name == 'p' and el is not first_p:
                    line = el.get_text(separator=' ', strip=True)
                    if line:
                        cur_lines.append(line)

            flush_section()
            info['key_points'] = sections

        # ── Pros / Cons ──────────────────────────────────────────────────────
        pros = soup.find('div', class_='pros')
        cons = soup.find('div', class_='cons')
        if pros:
            info['pros'] = [li.get_text(strip=True) for li in pros.find_all('li')]
        if cons:
            info['cons'] = [li.get_text(strip=True) for li in cons.find_all('li')]

        # ── Sector / Industry ────────────────────────────────────────────────
        for a_tag in soup.find_all('a', href=True):
            h = a_tag['href']
            if 'sector=' in h and not info['sector']:
                info['sector']   = a_tag.get_text(strip=True)
            if 'industry=' in h and not info['industry']:
                info['industry'] = a_tag.get_text(strip=True)

        # ── Peers ────────────────────────────────────────────────────────────
        ps = soup.find('section', id='peers')
        if ps:
            info['peers'] = [a_tag.get_text(strip=True) for a_tag in ps.select('td a')][:8]

    except Exception as e:
        info['error'] = str(e)
    return info


# ═══════════════════════════════════════════════════════════════════
# ANALYTICAL ENGINE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

# Sector benchmarks — NSE/BSE sectoral averages for context
SECTOR_BENCHMARKS = {
    'Auto Components': {'pe':18,'pb':3.0,'opm':10,'roe':15,'de':0.5,'sales_cagr_pct':12,'desc':'Cyclical. Tied to vehicle production. OEM concentration risk.'},
    'FMCG':            {'pe':45,'pb':12, 'opm':20,'roe':35,'de':0.1,'sales_cagr_pct':8, 'desc':'Defensive. Strong brands. Pricing power. Slow but steady.'},
    'IT Services':     {'pe':28,'pb':8,  'opm':22,'roe':28,'de':0.0,'sales_cagr_pct':15,'desc':'Asset-light. USD revenue. Global macro sensitive.'},
    'Banking':         {'pe':15,'pb':2.0,'opm':None,'roe':12,'de':None,'sales_cagr_pct':15,'desc':'Regulated. NIM sensitive. Credit cycle risk.'},
    'Pharma':          {'pe':30,'pb':4.0,'opm':18,'roe':15,'de':0.3,'sales_cagr_pct':12,'desc':'R&D driven. US FDA risk. Domestic stable.'},
    'Capital Goods':   {'pe':35,'pb':6.0,'opm':12,'roe':18,'de':0.4,'sales_cagr_pct':15,'desc':'Govt capex dependent. Order book visibility. Long cycles.'},
    'Power':           {'pe':20,'pb':3.0,'opm':25,'roe':14,'de':1.5,'sales_cagr_pct':10,'desc':'Regulated returns. High capex. Secular tailwind from energy transition.'},
    'Cement':          {'pe':25,'pb':4.0,'opm':18,'roe':14,'de':0.5,'sales_cagr_pct':10,'desc':'Infra & housing dependent. Regional pricing power.'},
    'Metals & Steel':  {'pe':12,'pb':1.5,'opm':12,'roe':12,'de':0.8,'sales_cagr_pct':8, 'desc':'Global commodity prices. Highly cyclical. China exposed.'},
    'Chemicals':       {'pe':30,'pb':5.0,'opm':15,'roe':18,'de':0.3,'sales_cagr_pct':15,'desc':'China+1 beneficiary. Specialty > commodity. Import substitution.'},
    'AMC & Wealth':    {'pe':35,'pb':10, 'opm':35,'roe':30,'de':0.0,'sales_cagr_pct':18,'desc':'Asset-light. AUM drives revenue. Secular India financialisation story.'},
    'Telecom':         {'pe':22,'pb':3.0,'opm':35,'roe':8, 'de':2.0,'sales_cagr_pct':10,'desc':'Duopoly. High capex (5G). ARPU expansion story.'},
    'Real Estate':     {'pe':20,'pb':3.0,'opm':25,'roe':12,'de':1.0,'sales_cagr_pct':12,'desc':'Inventory-heavy. Interest rate sensitive. Geography specific.'},
    'Consumer Durables':{'pe':40,'pb':8, 'opm':12,'roe':22,'de':0.2,'sales_cagr_pct':12,'desc':'Premium + mass segments. Seasonal demand. Brand matters.'},
    'Insurance':       {'pe':25,'pb':4.0,'opm':None,'roe':15,'de':None,'sales_cagr_pct':15,'desc':'AUM + float. Regulatory risk. Penetration story.'},
    'Retail':          {'pe':50,'pb':10, 'opm':8, 'roe':15,'de':0.5,'sales_cagr_pct':20,'desc':'Same-store growth metric. Working capital intensive.'},
}

def detect_sector(company_name, screener_sector, screener_industry):
    """Map company to a sector benchmark.
    Priority: (1) exact screener sector/industry match, (2) keyword scan of combined string.
    More specific keywords are checked before generic ones to avoid false matches.
    """
    # Priority 1 — use screener's own sector/industry label if it maps cleanly
    combined_meta = (screener_sector + ' ' + screener_industry).lower()
    meta_map = [
        (['auto component','wheel','two wheeler','auto ancil'],               'Auto Components'),
        (['fmcg','consumer food','consumer staple'],                          'FMCG'),
        (['software','it service','information tech'],                        'IT Services'),
        (['bank','nbfc','microfinance'],                                      'Banking'),
        (['pharma','drug','biotech','healthcare'],                            'Pharma'),
        (['cement'],                                                          'Cement'),
        (['metal','steel','aluminium','copper','zinc'],                       'Metals & Steel'),
        (['chemical','specialty chem','agrochemical'],                        'Chemicals'),
        (['capital good','engineering','defence','aerospace'],                'Capital Goods'),
        (['power','energy','renewable'],                                      'Power'),
        (['telecom'],                                                         'Telecom'),
        (['asset management','amc','mutual fund','wealth'],                   'AMC & Wealth'),
        (['real estate','realty','housing','reit'],                           'Real Estate'),
        (['insurance'],                                                       'Insurance'),
        (['retail','e-commerce','quick commerce'],                            'Retail'),
        (['consumer durable','appliance','electric'],                         'Consumer Durables'),
    ]
    for keywords, sector in meta_map:
        if any(k in combined_meta for k in keywords):
            return sector

    # Priority 2 — scan company name + all metadata together
    # NOTE: more specific / longer keywords are listed BEFORE generic ones
    # e.g. 'wheel' before 'steel' so SSWL maps to Auto Components not Metals
    cn = (company_name + ' ' + screener_sector + ' ' + screener_industry).lower()
    name_map = [
        # Specific company/product keywords first
        (['wheel','auto comp','bosch','minda','motherson','sswl','varroc',
          'tyre','bearing','clutch','brake','auto ancill'],                   'Auto Components'),
        (['fmcg','biscuit','dairy','beverage','soap','shampoo','toothpaste',
          'britannia','nestle','hul','itc','marico','dabur','godrej consumer'], 'FMCG'),
        (['infosy','tcs','wipro','hcl tech','tech mahindra','mphasis','ltim',
          'persistent','coforge','software','it service'],                    'IT Services'),
        (['hdfc bank','icici bank','kotak bank','axis bank','sbi','indusind',
          'yes bank','federal bank','idfc','rbl bank','au small',
          'nbfc','microfinance',' bank ','first bank'],                       'Banking'),
        (['cipla','sun pharma','divi','dr reddy','biocon','lupin','torrent pharma',
          'alkem','ajanta','pharma','drug','biotech'],                        'Pharma'),
        (['ultratech','ambuja','shree cement','acc','jk cement','cement'],    'Cement'),
        (['pidilite','aarti','deepak nitrite','navin fluorine','chemical',
          'specialty chem'],                                                   'Chemicals'),
        (['bhel','l&t','siemens','abb','cg power','cgpower','thermax','voltas',
          'capital good','engineering'],                                       'Capital Goods'),
        (['ntpc','adani power','tata power','cesc','torrent power','power',
          'renewable','solar'],                                                'Power'),
        (['airtel','reliance jio','vodafone','telecom'],                      'Telecom'),
        (['nippon','hdfc amc','uti','mirae','asset management','amc','mutual fund'], 'AMC & Wealth'),
        (['tata steel','jsw','sail','hindalco','vedanta','metal','steel','alumin'], 'Metals & Steel'),
        (['dlf','godrej prop','prestige','brigade','oberoi','real estate'],   'Real Estate'),
        (['lic','sbi life','hdfc life','icici pru','insurance'],              'Insurance'),
        (['dmart','trent','avenue','reliance retail','retail'],               'Retail'),
        (['havells','blue star','lloyd','dixon','amber','voltas','consumer durable'], 'Consumer Durables'),
    ]
    for keywords, sector in name_map:
        if any(k in cn for k in keywords):
            return sector
    return None


def compute_wacc(borrow_latest, equity_mkt, interest_latest, tax_rate, beta_sector=1.2):
    """
    WACC = Ke * E/(D+E)  +  Kd*(1-t) * D/(D+E)
    Ke = Rf + beta * ERP   (Rf=7.5% India 10Y Gsec, ERP=7% India equity risk premium)
    Kd = actual interest rate on debt
    """
    rf  = 0.075   # India 10-yr G-sec yield
    erp = 0.070   # India equity risk premium
    ke  = rf + beta_sector * erp
    
    d   = borrow_latest or 0
    e   = equity_mkt or 1
    total = d + e
    
    kd  = (interest_latest / d) if d > 0 else 0.12
    kd  = min(max(kd, 0.08), 0.18)  # clamp to 8-18%
    
    wacc = ke * (e/total) + kd * (1 - (tax_rate or 0.25)) * (d/total)
    return round(wacc, 4)


def run_dcf(owner_earnings, wacc, growth_high, growth_mid, terminal_g=0.05,
            net_debt=0, shares=1, yrs_high=5, yrs_fade=5):
    """3-stage DCF: high growth → fade → terminal value."""
    if not owner_earnings or owner_earnings <= 0 or wacc <= terminal_g:
        return None
    pv = 0; cf = owner_earnings
    # Stage 1 — high growth
    for y in range(1, yrs_high+1):
        cf *= (1 + growth_high)
        pv += cf / (1+wacc)**y
    # Stage 2 — linear fade to terminal
    fade = (growth_high - terminal_g) / yrs_fade
    for y in range(1, yrs_fade+1):
        cf *= (1 + growth_high - fade*y)
        pv += cf / (1+wacc)**(yrs_high+y)
    # Stage 3 — terminal
    tv = cf * (1+terminal_g) / (wacc - terminal_g)
    pv += tv / (1+wacc)**(yrs_high+yrs_fade)
    equity_val = pv - net_debt
    return round(equity_val / shares, 2) if shares > 0 else None


def compute_dcf_analysis(d):
    """Full DCF with 3 scenarios (Bull/Base/Bear) + sensitivity table."""
    pat    = d['pat'];   dep   = d['dep'];   capex = d['capex']
    cfo    = d['cfo'];   borrow= d['borrow']
    adj_sh = d['adj_sh']; cash  = d['cash']
    interest=d['int'];   tax   = d['tax'];   pbt   = d['pbt']

    # Owner Earnings = PAT + Dep - Normalised Capex
    # Use avg of last 3 years to smooth lumpy capex
    capex_3y = [v for v in capex[-4:] if v is not None]
    avg_capex = sum(capex_3y)/len(capex_3y) if capex_3y else 0
    pat_latest = latest([v for v in pat if v]) or 0
    dep_latest = latest([v for v in dep if v]) or 0
    oe = pat_latest + dep_latest - avg_capex

    # Also compute CFO-based FCF as sanity check
    cfo_3y  = [v for v in cfo[-3:] if v]
    avg_cfo  = sum(cfo_3y)/len(cfo_3y) if cfo_3y else 0
    fcf_base = avg_cfo - avg_capex

    # Use higher of the two as base (conservative: use lower)
    base_earnings = min(oe, fcf_base) if fcf_base > 0 and oe > 0 else max(oe, fcf_base, 10)

    # WACC
    borrow_latest = latest([v for v in borrow if v is not None]) or 0
    mcap          = d['market_cap']
    int_latest    = latest([v for v in interest if v]) or 0
    tax_vals      = [t/p for t,p in zip(tax,pbt) if t and p and p>0 and t/p<1]
    avg_tax       = sum(tax_vals)/len(tax_vals) if tax_vals else 0.25
    wacc = compute_wacc(borrow_latest, mcap, int_latest, avg_tax)

    # Growth rate inputs
    g10 = d['pat_cagr'].get('10y') or 0
    g5  = d['pat_cagr'].get('5y')  or 0
    g3  = d['pat_cagr'].get('3y')  or 0
    # Sustainability cap: no company can grow forever at >20% in India
    g_high  = min(max(g5 or g3 or g10, 0), 0.25)
    g_mid   = min(max((g5+g10)/2 if g10 else g5 or g3, 0), 0.18)
    g_low   = min(max(min(g3 or g5 or g10, g10 or 0.07), 0), 0.12)
    tg      = 0.05   # India nominal terminal growth

    # Net debt
    cash_latest = latest([v for v in cash if v]) or 0
    inv_latest  = latest([v for v in d.get('cash_invest',[]) if v]) or cash_latest
    net_debt    = borrow_latest - inv_latest
    shares      = latest([v for v in adj_sh if v]) or 1

    cur_price   = d['current_price']

    # Three scenarios
    # Run DCF on CURRENT earnings (shows what market already prices in)
    bull_iv_raw = run_dcf(base_earnings, wacc, g_high,  g_mid,  tg, net_debt, shares)
    base_iv_raw = run_dcf(base_earnings, wacc, g_mid,   g_low,  tg, net_debt, shares)
    bear_iv_raw = run_dcf(base_earnings, wacc, g_low,   tg+0.01,tg, net_debt, shares)

    # Also run DCF on MID-CYCLE earnings (conservative view for cyclical companies)
    cyc_check_pats = [v for v in pat if v is not None]
    mid_cycle_pat  = sorted(cyc_check_pats)[len(cyc_check_pats)//2] if cyc_check_pats else pat_latest
    at_peak = pat_latest > 0 and mid_cycle_pat > 0 and pat_latest > mid_cycle_pat * 1.4
    if at_peak and mid_cycle_pat > 0:
        mid_adj = base_earnings * (mid_cycle_pat / pat_latest)
        base_iv_cycle = run_dcf(mid_adj, wacc, g_mid, g_low, tg, net_debt, shares)
        base_iv_cycle = round(max(base_iv_cycle, 0), 2) if base_iv_cycle else None
    else:
        base_iv_cycle = None
        at_peak = False

    # Floor at 0 — negative DCF means WACC exceeds growth: stock earns less than cost of capital
    # In that case IV is indeterminate; show "N/A (WACC exceeds growth)" rather than negative number
    def safe_iv(v): return round(max(v, 0), 2) if v is not None else None
    bull_iv = safe_iv(bull_iv_raw)
    base_iv = safe_iv(base_iv_raw)
    bear_iv = safe_iv(bear_iv_raw)

    # Mark if bear case showed negative equity (over-levered or poor growth)
    bear_negative = bear_iv_raw is not None and bear_iv_raw < 0

    # Margin of safety zones — only from base IV
    mos_buy   = round(base_iv * 0.70, 0) if base_iv and base_iv > 0 else None
    mos_great = round(base_iv * 0.60, 0) if base_iv and base_iv > 0 else None

    # Upside / downside
    def updown(iv):
        if not iv or not cur_price or iv <= 0: return None
        return round((iv/cur_price - 1)*100, 1)

    # Sensitivity table: wacc ± 1%, growth ± 2%
    sensitivity = {}
    for dg in (-0.04, -0.02, 0, +0.02, +0.04):
        row = {}
        for dw in (-0.01, 0, +0.01):
            iv = run_dcf(base_earnings, wacc+dw, g_mid+dg, g_low+dg/2, tg, net_debt, shares)
            row[f'{(wacc+dw)*100:.1f}%'] = round(iv,0) if iv else None
        sensitivity[f'{(g_mid+dg)*100:.0f}%'] = row

    return {
        'owner_earnings': round(base_earnings, 1),
        'avg_capex':      round(avg_capex, 1),
        'wacc':           wacc,
        'g_high':         g_high,  'g_mid': g_mid,  'g_low': g_low,
        'tg':             tg,
        'net_debt':       round(net_debt, 1),
        'shares':         shares,
        'bull_iv':        bull_iv,
        'base_iv':        base_iv,
        'bear_iv':        bear_iv,
        'mos_buy':        mos_buy,
        'mos_great':      mos_great,
        'bull_updown':    updown(bull_iv),
        'base_updown':    updown(base_iv),
        'bear_updown':    updown(bear_iv),
        'bear_negative':  bear_negative,
        'base_iv_cycle':  base_iv_cycle,
        'at_peak':        at_peak,
        'mid_cycle_pat':  round(mid_cycle_pat, 1) if mid_cycle_pat else None,
        'sensitivity':    sensitivity,
        'cur_price':      cur_price,
    }


def compute_moat_score(d):
    """Score 0-100 across 6 dimensions. Returns score, label, color, breakdown."""
    opm_s  = d['opm'];    roe_s = d['roe'];    roce_s= d['roce']
    nfat_s = d['nfat'];   sales = d['sales'];  pat   = d['pat']
    sc     = d['sales_cagr']; pc = d['pat_cagr']
    sg10   = sc.get('10y') or 0
    pg10   = pc.get('10y') or 0

    score=0; max_s=0; bd=[]

    # 1. Avg OPM (0-20) — absolute margin level
    opm_v=[v for v in opm_s if v]
    if opm_v:
        avg_opm=sum(opm_v)/len(opm_v)
        pts=min(20,max(0,(avg_opm-5)*2))
        score+=pts; max_s+=20
        bd.append(('Avg Operating Margin',f'{avg_opm:.1f}%',round(pts),20,
                   '>15%=strong moat, 10-15%=moderate, <8%=commodity/no moat'))

    # 2. Margin stability (0-15) — pricing power proxy
    if opm_v and len(opm_v)>=3:
        rng=max(opm_v)-min(opm_v)
        pts=max(0,15-rng)
        score+=pts; max_s+=15
        bd.append(('Margin Stability (range)',f'{min(opm_v):.1f}–{max(opm_v):.1f}%',round(pts),15,
                   'Narrow range = can defend prices; Wide = takes what market gives'))

    # 3. Avg ROCE (0-20) — capital efficiency moat
    roce_v=[v for v in roce_s if v]
    if roce_v:
        avg_roce=sum(roce_v)/len(roce_v)
        pts=min(20,max(0,(avg_roce-10)*0.8))
        score+=pts; max_s+=20
        bd.append(('Avg ROCE',f'{avg_roce:.1f}%',round(pts),20,
                   '>35%=exceptional moat, 20-35%=good, <10%=no advantage'))

    # 4. Revenue CAGR vs India nominal GDP (~12%) (0-15) — market share indicator
    if sg10:
        pts=min(15,max(0,(sg10*100-5)*0.75))
        score+=pts; max_s+=15
        bd.append(('Revenue CAGR vs GDP',f'{sg10*100:.1f}% (GDP~12%)',round(pts),15,
                   '>15% CAGR=gaining market share; <10%=losing relative position'))

    # 5. PAT CAGR 10Y (0-15) — earnings compounding
    if pg10:
        pts=min(15,max(0,(pg10*100-5)*0.75))
        score+=pts; max_s+=15
        bd.append(('Earnings CAGR 10Y',f'{pg10*100:.1f}%',round(pts),15,
                   '>15%=strong compounding; <5%=stagnant'))

    # 6. NFA Turnover improvement (0-15) — operational leverage
    nfat_v=[v for v in nfat_s if v]
    if len(nfat_v)>=4:
        trend=(nfat_v[-1]-nfat_v[0])/nfat_v[0]*100
        pts=min(15,max(0,(trend+30)*0.25))
        score+=pts; max_s+=15
        bd.append(('Asset Efficiency Trend',f'{trend:+.0f}% NFA turnover change',round(pts),15,
                   '+ve trend = more revenue per ₹ of plant = operational leverage'))

    pct=round(score/max_s*100) if max_s else 0
    if pct>=75:   label,color='Wide Moat',    '#059669'
    elif pct>=55: label,color='Narrow Moat',  '#84cc16'
    elif pct>=38: label,color='Weak Moat',    '#f97316'
    else:         label,color='No Moat / Commodity', '#dc2626'

    return {'score':round(score,1),'max':max_s,'pct':pct,
            'label':label,'color':color,'breakdown':bd}


def compute_mgmt_score(d):
    """Score management quality 0-100."""
    vpr     = d.get('vpr')
    cfo_pat = sum(1 for c,p in zip(d['cfo'],d['pat']) if c and p and c>p)
    div_yrs = sum(1 for v in d['div'] if v and v>0)
    dil     = d.get('share_dilution_pct') or 0
    inc_r   = latest([v for v in d['inc_roe'] if v])
    b0      = d['borrow'][0]; b1=latest([v for v in d['borrow'] if v is not None])
    debt_chg_pct = (b1-b0)/b0*100 if b0 and b0!=0 else 0
    fcf_cfo = d.get('fcf_cfo') or 0

    score=0; max_s=0; bd=[]

    # 1. Capital allocation quality — VPR (0-20)
    if vpr is not None:
        pts=min(20,max(0,(vpr-0.5)*8))
        lbl='Excellent' if vpr>2 else ('Good' if vpr>1 else 'Poor')
        bd.append(('Capital Allocation (VPR)',f'₹{vpr:.2f}',round(pts),20,
                   f'{lbl}. >₹2=excellent, ₹1-2=good, <₹1=destroying value'))
    else:
        pts=10; bd.append(('Capital Allocation (VPR)','Insufficient data',pts,20,''))
    score+=pts; max_s+=20

    # 2. Earnings quality — CFO>PAT years (0-20)
    pts=round(cfo_pat/10*20)
    bd.append(('Earnings Quality (CFO>PAT)',f'{cfo_pat}/10 years',pts,20,
               '10/10=profits are all real cash; <5=aggressive accounting risk'))
    score+=pts; max_s+=20

    # 3. Shareholder commitment — dividends (0-15)
    pts=round(div_yrs/10*15)
    bd.append(('Dividend Track Record',f'{div_yrs}/10 years',pts,15,
               'Consistent dividends = commitment to sharing profits'))
    score+=pts; max_s+=15

    # 4. Dilution discipline (0-15)
    if dil<=2:    pts=15
    elif dil<=10: pts=12
    elif dil<=25: pts=7
    elif dil<=50: pts=3
    else:         pts=0
    bd.append(('Share Dilution Control',f'{dil:+.1f}%',pts,15,
               '<2%=excellent, <10%=ok, >25%=significant dilution'))
    score+=pts; max_s+=15

    # 5. Reinvestment quality — incremental ROE (0-15)
    if inc_r is not None:
        pts=min(15,max(0,inc_r*0.5))
        bd.append(('Reinvestment Quality (Inc. ROE)',f'{inc_r:.0f}%',round(pts),15,
                   '>20%=excellent reinvestor, <5%=poor capital deployment'))
    else:
        pts=7; bd.append(('Reinvestment Quality','Insufficient data',pts,15,''))
    score+=pts; max_s+=15

    # 6. Debt discipline (0-15)
    if debt_chg_pct <= 0:     pts=15  # reduced debt
    elif debt_chg_pct <= 25:  pts=13
    elif debt_chg_pct <= 50:  pts=10
    elif debt_chg_pct <= 100: pts=6
    else:                     pts=2
    bd.append(('Debt Discipline',f'Debt {debt_chg_pct:+.0f}% over 10Y',pts,15,
               'Decreasing=excellent, <50% increase=ok, >100%=leveraging up heavily'))
    score+=pts; max_s+=15

    pct=round(score/max_s*100) if max_s else 0
    if pct>=78:   label,color='Exceptional Management','#059669'
    elif pct>=62: label,color='Good Management',       '#84cc16'
    elif pct>=45: label,color='Average Management',    '#d97706'
    else:         label,color='Weak Management',       '#dc2626'

    return {'score':round(score,1),'max':max_s,'pct':pct,
            'label':label,'color':color,'breakdown':bd}


def compute_cyclicality(d):
    """Classify business cycle sensitivity and give valuation guidance."""
    pat_s  = [v for v in d['pat']  if v is not None]
    sales_s= [v for v in d['sales'] if v is not None]
    opm_s  = [v for v in d['opm']  if v is not None]

    pat_down  = sum(1 for i in range(1,len(pat_s))   if pat_s[i]  < pat_s[i-1])
    sales_down= sum(1 for i in range(1,len(sales_s)) if sales_s[i]< sales_s[i-1])
    n         = len(pat_s)-1 or 1

    opm_range   = round(max(opm_s)-min(opm_s),1) if opm_s else 0
    max_drawdown= round(max(
        (pat_s[i]-min(pat_s[i:]))/pat_s[i]*100
        for i in range(len(pat_s)-1) if pat_s[i]>0
    ),1) if len(pat_s)>1 else 0

    # Score cyclicality (higher = more cyclical)
    cs=0
    if pat_down>=4:   cs+=3
    elif pat_down>=2: cs+=2
    else:             cs+=1
    if opm_range>10:  cs+=2
    elif opm_range>5: cs+=1
    if max_drawdown>60: cs+=3
    elif max_drawdown>40: cs+=2
    elif max_drawdown>25: cs+=1
    if sales_down>=3: cs+=1

    if cs>=8:    label,color,typ='Highly Cyclical',    '#dc2626','cyclical'
    elif cs>=5:  label,color,typ='Moderately Cyclical','#f97316','cyclical'
    elif cs>=3:  label,color,typ='Mildly Cyclical',    '#d97706','semi-cyclical'
    else:        label,color,typ='Defensive / Secular','#059669','secular'

    # Mid-cycle PAT for valuation normalisation
    mid_cycle_pat = round(sorted(pat_s)[len(pat_s)//2],1) if pat_s else None
    latest_pat    = latest(d['pat'])
    over_earning  = (latest_pat > mid_cycle_pat * 1.3) if (latest_pat and mid_cycle_pat) else False
    under_earning = (latest_pat < mid_cycle_pat * 0.7) if (latest_pat and mid_cycle_pat) else False

    advice_lines = []
    if over_earning:
        advice_lines.append(f'⚠ Currently OVER-earning vs mid-cycle. Current PE ({d.get("pe_ttm","?"):.1f}x) understates true valuation. Use mid-cycle PAT of ₹{mid_cycle_pat:.0f} Cr for fair valuation.')
    elif under_earning:
        advice_lines.append(f'💡 Currently UNDER-earning vs mid-cycle. Reported PE overstates valuation. Recovery to mid-cycle earnings (₹{mid_cycle_pat:.0f} Cr) could mean large PE compression + earnings growth.')
    else:
        advice_lines.append(f'Earnings appear to be near mid-cycle levels. Current PAT (₹{latest_pat:.0f} Cr) vs mid-cycle estimate (₹{mid_cycle_pat:.0f} Cr).')

    return {'score':cs,'label':label,'color':color,'type':typ,
            'pat_down':pat_down,'sales_down':sales_down,
            'opm_range':opm_range,'max_pat_drawdown':max_drawdown,
            'mid_cycle_pat':mid_cycle_pat,'over_earning':over_earning,
            'under_earning':under_earning,'advice':advice_lines}


def compute_red_flags(d):
    """Scan all metrics for warning signs. Returns flags by severity."""
    flags=[]
    pat=d['pat']; sales=d['sales']; cfo=d['cfo']; recv=d['recv']
    borrow=d['borrow']; oi=d['oi']; dep=d['dep']; pbt=d['pbt']
    tax=d['tax']; adj_sh=d['adj_sh']; nb=d['nb']
    equity=d['equity']; fcf=d['fcf']; capex=d['capex']
    opm=d['opm']; int_s=d['int']

    def F(sev, cat, desc, detail=''):
        flags.append({'sev':sev,'cat':cat,'desc':desc,'detail':detail})

    # ── EARNINGS QUALITY ──────────────────────────────────────────
    bad_cfo=[i for i in range(10) if cfo[i] and pat[i] and pat[i]>10 and cfo[i]<pat[i]*0.5]
    if len(bad_cfo)>=3:
        F('HIGH','Earnings Quality',
          f'CFO < 50% of PAT in {len(bad_cfo)}/10 years.',
          'Reported profits are not being collected as cash. Red flag for revenue recognition or receivables abuse.')

    recv_v=[v for v in recv if v]; sales_v=[v for v in sales if v]
    if len(recv_v)>=5 and len(sales_v)>=5:
        rg=(recv_v[-1]/recv_v[0]-1); sg=(sales_v[-1]/sales_v[0]-1)
        if rg>sg*1.6:
            F('MEDIUM','Receivables Growing Faster Than Sales',
              f'Receivables +{rg*100:.0f}% vs Sales +{sg*100:.0f}% over 10 years.',
              'Revenue may be booked before cash arrives. Investigate customer credit quality.')

    oi_dep=[i for i in range(10) if oi[i] and pat[i] and pat[i]>5 and oi[i]/pat[i]>0.3]
    if len(oi_dep)>=4:
        avg_oi_pct=sum((oi[i] or 0)/(pat[i] or 1)*100 for i in oi_dep)/len(oi_dep)
        F('MEDIUM','High Other Income Dependency',
          f'Other income > 30% of PAT in {len(oi_dep)}/10 years (avg {avg_oi_pct:.0f}%).',
          'Core business may be weaker than headline numbers suggest. Strip OI for true operating earnings.')

    tax_v=[t/p for t,p in zip(tax,pbt) if t and p and p>0 and 0<t/p<1]
    if tax_v:
        avg_t=sum(tax_v)/len(tax_v)
        very_low=[i for i in range(10) if tax[i] and pbt[i] and pbt[i]>10 and tax[i]/pbt[i]<0.08]
        if very_low:
            F('LOW','Unusually Low Tax Rate',
              f'Effective tax <8% in {len(very_low)} year(s) — years {[y+1 for y in very_low]}.',
              'Could be MAT credits, deferred tax reversals, or extraordinary tax exemptions boosting reported PAT.')

    # ── DEBT & LEVERAGE ──────────────────────────────────────────
    de=[b/e if e and e>0 and b is not None else None for b,e in zip(borrow,equity)]
    high_de=[i for i in range(10) if de[i] and de[i]>2.5]
    if high_de:
        F('HIGH','Dangerously High Leverage',
          f'D/E > 2.5x in years {[y+1 for y in high_de]}.',
          'At this leverage, a 20-25% revenue decline could trigger interest default risk.')

    b_valid=[v for v in borrow if v is not None]; e_valid=[v for v in equity if v]
    if len(b_valid)>=4 and len(e_valid)>=4:
        bg=(b_valid[-1]-b_valid[0])/(b_valid[0] or 1); eg=(e_valid[-1]-e_valid[0])/(e_valid[0] or 1)
        if b_valid[-1]>b_valid[0] and bg>eg*1.8:
            F('MEDIUM','Debt Accumulating Faster Than Equity',
              f'Debt grew {bg*100:.0f}% vs equity grew {eg*100:.0f}% over 10 years.',
              'Balance sheet leverage is structurally increasing. Watch WACC and interest coverage.')

    # Interest coverage below 1.5 in recent years
    ic_low=[i for i in range(7,10) if d['ic_dvm'][i] and d['ic_dvm'][i]<1.5]
    if ic_low:
        F('HIGH','Thin Interest Coverage',
          f'Interest coverage < 1.5x in recent years {[y+1 for y in ic_low]}.',
          'Operating profit barely covers interest. Any revenue dip could cause default risk.')

    # ── GROWTH QUALITY ───────────────────────────────────────────
    s_v=[v for v in sales if v]; p_v=[v for v in pat if v]
    if len(s_v)>=4 and len(p_v)>=4:
        s_recent=s_v[-1]/s_v[-4]-1; p_recent=p_v[-1]/p_v[-4]-1
        if s_recent>0.2 and p_recent<-0.1:
            F('MEDIUM','Revenue Growth Without Profit Growth',
              f'Sales +{s_recent*100:.0f}% but PAT {p_recent*100:.0f}% over last 3 years.',
              'Growing revenues are not translating to profits. Margin compression or cost escalation.')

    # FCF negative for 3+ consecutive years
    fcf_v=[(i,v) for i,v in enumerate(fcf) if v is not None]
    consec_neg=0; max_consec=0
    for _,v in fcf_v:
        if v<0: consec_neg+=1; max_consec=max(max_consec,consec_neg)
        else: consec_neg=0
    if max_consec>=3:
        F('MEDIUM','Extended Negative Free Cash Flow',
          f'FCF negative for {max_consec} consecutive years.',
          'Sustained negative FCF means the business cannot fund itself. Dependent on debt/equity. Acceptable if high-ROCE capex; concerning otherwise.')

    # ── CAPITAL ALLOCATION ────────────────────────────────────────
    vpr=d.get('vpr')
    if vpr is not None and vpr<0.7:
        F('MEDIUM','Value-Destructive Capital Retention',
          f'₹1 retained created only ₹{vpr:.2f} in market cap.',
          'Shareholders would have been better off receiving retained earnings as dividends.')

    # CWIP stuck > 30% of NFA for 3+ years
    cwip_high=[i for i in range(10) if d['cwip'][i] and nb[i] and d['cwip'][i]/nb[i]>0.3]
    if len(cwip_high)>=3:
        F('LOW','Persistent High CWIP',
          f'CWIP > 30% of NFA in {len(cwip_high)} years.',
          'Projects staying in work-in-progress for long = execution delays or cost overruns. Check annual report notes.')

    # ── DILUTION ─────────────────────────────────────────────────
    sh_v=[v for v in adj_sh if v]
    if len(sh_v)>=2:
        dil=(sh_v[-1]-sh_v[0])/sh_v[0]*100
        if dil>30:
            F('MEDIUM','Significant Share Dilution',
              f'Share count grew {dil:.0f}% over 10 years.',
              'EPS growth overstates economic value creation. Per-share metrics are flattering vs absolute profits.')

    # Classify
    high   = [f for f in flags if f['sev']=='HIGH']
    medium = [f for f in flags if f['sev']=='MEDIUM']
    low    = [f for f in flags if f['sev']=='LOW']

    if high:          overall,color='⛔ CONCERNING — Review Before Investing','#dc2626'
    elif len(medium)>=3: overall,color='🟠 WATCH — Multiple Concerns','#f97316'
    elif medium:      overall,color='🟡 CAUTION — Some Yellow Flags','#d97706'
    else:             overall,color='✅ CLEAN — No Significant Red Flags','#059669'

    return {'flags':flags,'high':high,'medium':medium,'low':low,
            'overall':overall,'color':color,'count':len(flags)}


def compute_sector_comparison(d, sector_label):
    """Compare company metrics against sector benchmarks."""
    if not sector_label or sector_label not in SECTOR_BENCHMARKS:
        return None
    bm = SECTOR_BENCHMARKS[sector_label]
    rows = []

    def cmp(metric, company_val, benchmark_val, higher_is_better=True, fmt_str='{:.1f}'):
        if company_val is None or benchmark_val is None:
            return None
        ratio = company_val / benchmark_val if benchmark_val else 1
        if higher_is_better:
            status = 'ABOVE' if ratio>1.1 else ('BELOW' if ratio<0.9 else 'INLINE')
        else:
            status = 'BELOW' if ratio<0.9 else ('ABOVE' if ratio>1.1 else 'INLINE')  # inverted
        color = '#059669' if status in ('ABOVE' if higher_is_better else ('BELOW',)) else                 ('#dc2626' if status in (('BELOW' if higher_is_better else 'ABOVE'),) else '#d97706')
        # Fix color logic cleanly
        if higher_is_better:
            color = '#059669' if status=='ABOVE' else ('#dc2626' if status=='BELOW' else '#d97706')
        else:
            color = '#059669' if status=='BELOW' else ('#dc2626' if status=='ABOVE' else '#d97706')

        return {'metric':metric,'company':company_val,'benchmark':benchmark_val,
                'status':status,'color':color,'fmt':fmt_str}

    opm_latest = latest([v for v in d['opm'] if v])
    roe_latest  = latest([v for v in d['roe'] if v])
    de_latest   = latest([v for v in d['de']  if v is not None])
    pe_use      = d.get('pe_ttm') or d.get('pe')
    pb_use      = d.get('pb')
    sg10        = (d['sales_cagr'].get('10y') or 0)*100

    rows = [
        cmp('P/E Ratio',       pe_use,    bm['pe'],    False, '{:.1f}x'),
        cmp('P/B Ratio',       pb_use,    bm['pb'],    False, '{:.1f}x'),
        cmp('Op. Margin %',    opm_latest,bm['opm'],   True,  '{:.1f}%'),
        cmp('ROE %',           roe_latest,bm['roe'],   True,  '{:.1f}%'),
        cmp('Debt/Equity',     de_latest, bm['de'],    False, '{:.2f}x'),
        cmp('Sales CAGR 10Y %',sg10,      bm['sales_cagr_pct'], True, '{:.1f}%'),
    ]
    rows = [r for r in rows if r]

    beats  = sum(1 for r in rows if r['status']=='ABOVE' and r['metric'] not in ('P/E Ratio','P/B Ratio','Debt/Equity'))
    beats += sum(1 for r in rows if r['status']=='BELOW' and r['metric'] in ('P/E Ratio','P/B Ratio','Debt/Equity'))
    lags   = len(rows) - beats
    pct_beat = round(beats/len(rows)*100) if rows else 0

    return {'sector':sector_label,'desc':bm.get('desc',''),
            'rows':rows,'beats':beats,'lags':lags,'pct_beat':pct_beat,
            'verdict': f'Beats sector on {beats}/{len(rows)} metrics',
            'color': '#059669' if pct_beat>=60 else ('#d97706' if pct_beat>=40 else '#dc2626')}


def compute_combined_verdict(moat, mgmt, dcf, cyc, rf, sc, valuation, current_price):
    """
    Synthesise all 6 engine outputs into a single weighted verdict.
    
    Weights reflect long-term investor priorities:
      Business quality (moat + mgmt): 35%
      Valuation safety (DCF + PE vs hist): 30%
      Risk flags (red flags + cyclicality): 20%
      Sector positioning: 15%
    """
    scores = {}
    reasons_buy   = []
    reasons_avoid = []

    # ── 1. Moat (0-35 scaled to 0-20 points) ────────────────────
    moat_pct = moat.get('pct', 50)
    moat_pts = moat_pct / 100 * 20
    scores['moat'] = moat_pts
    if moat_pct >= 70: reasons_buy.append(f"Wide/narrow moat ({moat['label']}) — sustainable competitive advantage")
    elif moat_pct < 40: reasons_avoid.append(f"Weak moat ({moat['label']}) — margins vulnerable to competition")

    # ── 2. Management quality (0-15 points) ─────────────────────
    mgmt_pct = mgmt.get('pct', 50)
    mgmt_pts = mgmt_pct / 100 * 15
    scores['mgmt'] = mgmt_pts
    if mgmt_pct >= 70: reasons_buy.append(f"Good management ({mgmt['label']}) — capital allocated well")
    elif mgmt_pct < 45: reasons_avoid.append(f"Management concerns ({mgmt['label']}) — capital allocation or dilution issues")

    # ── 3. DCF Valuation safety (0-20 points) ──────────────────
    base_iv   = dcf.get('base_iv') or 0
    bull_iv   = dcf.get('bull_iv') or 0
    cur       = current_price or 1
    at_peak   = dcf.get('at_peak', False)
    
    if base_iv > 0:
        discount = (base_iv - cur) / cur   # +ve = undervalued
        if at_peak:
            # Cyclical peak — penalise current-earnings DCF, use conservative IV
            discount = discount * 0.5     # halve the apparent upside
        
        if discount > 0.30:
            dcf_pts = 20
            reasons_buy.append(f"DCF shows stock at significant discount to intrinsic value (base IV ₹{base_iv:.0f})")
        elif discount > 0.10:
            dcf_pts = 16
            reasons_buy.append(f"DCF shows moderate margin of safety (base IV ₹{base_iv:.0f})")
        elif discount > -0.10:
            dcf_pts = 12   # fairly valued
        elif discount > -0.30:
            dcf_pts = 8
            reasons_avoid.append(f"DCF shows stock trading above intrinsic value (base IV ₹{base_iv:.0f})")
        else:
            dcf_pts = 3
            reasons_avoid.append(f"DCF shows significant overvaluation — even bull case ({bull_iv:.0f}) below current price")
    else:
        dcf_pts = 5    # insufficient data
    
    if at_peak:
        reasons_avoid.append("Earnings appear cyclically elevated — DCF may overstate intrinsic value at this point in the cycle")
    scores['dcf'] = dcf_pts

    # ── 4. PE vs history valuation (0-10 points) ────────────────
    vs_hist = valuation.get('vs_hist')   # % above/below hist avg PE
    peg     = valuation.get('peg')
    if vs_hist is not None:
        if vs_hist < -15:
            pe_pts = 10
            reasons_buy.append(f"Trading {abs(vs_hist):.0f}% below its own 10-year average PE — historically cheap")
        elif vs_hist < 0:
            pe_pts = 8
        elif vs_hist < 15:
            pe_pts = 6
        elif vs_hist < 30:
            pe_pts = 4
            reasons_avoid.append(f"Trading {vs_hist:.0f}% above historical average PE")
        else:
            pe_pts = 1
            reasons_avoid.append(f"Trading {vs_hist:.0f}% above historical average PE — expensive vs own history")
    else:
        pe_pts = 5
    scores['pe_hist'] = pe_pts

    # ── 5. Red flags penalty (0 to -15 points) ──────────────────
    high_flags   = len(rf.get('high', []))
    medium_flags = len(rf.get('medium', []))
    low_flags    = len(rf.get('low', []))
    rf_penalty   = high_flags * 8 + medium_flags * 3 + low_flags * 1
    rf_pts       = max(0, 15 - rf_penalty)
    scores['rf'] = rf_pts
    if rf.get('high'):
        reasons_avoid.append(f"{high_flags} HIGH-severity red flag(s): {', '.join(f['cat'] for f in rf['high'])}")
    elif not rf.get('medium') and not rf.get('high'):
        reasons_buy.append("Clean earnings quality — no significant red flags in 10-year data")

    # ── 6. Cyclicality (0-10 points — higher cyclicality = lower score) ─
    cyc_score = cyc.get('score', 5)
    cyc_pts   = max(0, 10 - cyc_score)
    scores['cyclicality'] = cyc_pts
    if cyc_score >= 7:
        reasons_avoid.append(f"Highly cyclical business — earnings can fall 60-70% in downturns; do not value at peak")
    elif cyc_score <= 2:
        reasons_buy.append("Defensive business profile — earnings are relatively recession-resistant")

    # ── 7. Sector positioning (0-10 points) ─────────────────────
    if sc:
        sect_pts = round(sc.get('pct_beat', 50) / 100 * 10)
        scores['sector'] = sect_pts
        if sc.get('pct_beat', 0) >= 70:
            reasons_buy.append(f"Outperforms sector ({sc['sector']}) on {sc['beats']}/{len(sc['rows'])} key metrics")
        elif sc.get('pct_beat', 0) <= 30:
            reasons_avoid.append(f"Underperforms sector ({sc['sector']}) on most metrics")
    else:
        scores['sector'] = 5

    # ── Composite score (0-100) ──────────────────────────────────
    total_pts = sum(scores.values())
    max_pts   = 20 + 15 + 20 + 10 + 15 + 10 + 10   # = 100
    composite = round(total_pts / max_pts * 100)

    # ── Final verdict ────────────────────────────────────────────
    if composite >= 72:
        verdict, color, emoji, action = "STRONG BUY",       "#059669", "✅", "High conviction — build a full position"
    elif composite >= 60:
        verdict, color, emoji, action = "BUY",              "#22c55e", "🟢", "Good risk/reward — start building a position"
    elif composite >= 50:
        verdict, color, emoji, action = "WATCH / ACCUMULATE","#84cc16", "🟡", "Watchlist — accumulate on dips or wait for better entry"
    elif composite >= 38:
        verdict, color, emoji, action = "HOLD / CAUTION",   "#f97316", "🟠", "Hold existing position — do not add at current levels"
    else:
        verdict, color, emoji, action = "AVOID",            "#dc2626", "❌", "Risk outweighs reward at current price"

    return {
        'verdict': verdict, 'color': color, 'emoji': emoji, 'action': action,
        'composite': composite, 'scores': scores, 'max_pts': max_pts,
        'reasons_buy': reasons_buy, 'reasons_avoid': reasons_avoid,
    }


# ─────────────────────── dot-joining narrative engine ───────────────────────
def build_narrative(d, si):
    """
    The heart of the dashboard. Reads ALL metrics and joins the dots
    to produce a coherent investment story rather than a dump of numbers.
    Returns a dict of narrative sections.
    """
    cn=d['company_name']
    g5=d['pat_cagr'].get('5y'); g3=d['pat_cagr'].get('3y'); g10=d['pat_cagr'].get('10y')
    sg5=d['sales_cagr'].get('5y'); sg10=d['sales_cagr'].get('10y')
    ssgr_latest=latest(d['ssgr']); ssgr_list=d['ssgr']
    roe_latest=latest(d['roe']); roce_latest=latest(d['roce'])
    de_latest=latest(d['de']); ic_latest=latest(d['ic_dvm'])
    opm_latest=latest(d['opm']); npm_latest=latest(d['npm'])
    vpr=d['vpr']; fcf_cfo=d['fcf_cfo']
    pe=d['pe_ttm']; avg_pe=d['avg_pe']
    wc_latest=latest(d['wc_days'])
    nfat_latest=latest(d['nfat']); pbt_nfa_latest=latest(d['pbt_nfa'])
    inc_roe_latest=latest([x for x in d['inc_roe'] if x])

    n = {}  # narrative dict

    # ── 1. BUSINESS QUALITY ──────────────────────────────────────
    quality_signals=[]; quality_warnings=[]

    # Growth consistency
    growth_years=[d['pat'][i] for i in range(1,10) if d['pat'][i] is not None and d['pat'][i-1] is not None and d['pat'][i]>d['pat'][i-1]]
    pct_growing=len(growth_years)/9*100
    if pct_growing>=80:
        quality_signals.append(f"Profits grew in {len(growth_years)} of the last 9 years — highly consistent earner.")
    elif pct_growing>=60:
        quality_signals.append(f"Profits grew in {len(growth_years)}/9 years — decent consistency but some cyclicality visible.")
    else:
        quality_warnings.append(f"Profits grew in only {len(growth_years)}/9 years — earnings are highly cyclical. Expect rough patches.")

    # ROE quality
    avg_roe=avg(d['roe'])
    if avg_roe:
        if avg_roe>20:
            quality_signals.append(f"10-year average ROE of {avg_roe:.1f}% — exceptional. The business generates strong returns on shareholder money without needing excessive debt.")
        elif avg_roe>12:
            quality_signals.append(f"Average ROE of {avg_roe:.1f}% — decent but not outstanding. The business earns above its cost of capital.")
        else:
            quality_warnings.append(f"Average ROE of only {avg_roe:.1f}% — the business earns below what most investors require. Wealth creation is limited.")

    # ROCE vs SSGR cross-check
    if ssgr_latest and sg5:
        if sg5*100 > ssgr_latest*1.5:
            quality_warnings.append(f"⚠ Sales grew at {sg5*100:.1f}%/yr but SSGR is only {ssgr_latest:.1f}% — the company is growing FASTER than its internal capacity allows. It needs external funding (debt or equity) to sustain this pace. Check if debt is rising.")
        elif sg5*100 <= ssgr_latest:
            quality_signals.append(f"Sales growth ({sg5*100:.1f}%/yr) is within SSGR ({ssgr_latest:.1f}%) — the company can self-fund its current growth rate without taking on more debt. Very healthy sign.")
        else:
            quality_signals.append(f"Sales growth ({sg5*100:.1f}%/yr) is slightly above SSGR ({ssgr_latest:.1f}%) — manageable but watch debt levels.")

    # FCF quality
    if fcf_cfo is not None:
        if fcf_cfo>25:
            quality_signals.append(f"Strong FCF/CFO ratio of {fcf_cfo:.0f}% — over 10 years, {fcf_cfo:.0f}% of operating cash became free cash. Business generates genuine surplus beyond its capex needs.")
        elif fcf_cfo>0:
            quality_signals.append(f"FCF/CFO of {fcf_cfo:.0f}% over 10 years — the company generates free cash, but most operating cash flows back into capex. Capital-intensive nature limits free cash.")
        else:
            quality_warnings.append(f"Negative FCF/CFO — over 10 years, the company has consumed MORE in capex than it generated in operations. Growth is being funded by debt/equity, not internal cash. Risky.")

    # Incremental ROE
    if inc_roe_latest is not None:
        if inc_roe_latest>15:
            quality_signals.append(f"Incremental ROE of {inc_roe_latest:.0f}% — each incremental rupee of retained earnings is generating strong new profits. Management is deploying reinvested capital well.")
        elif inc_roe_latest>5:
            quality_signals.append(f"Incremental ROE of {inc_roe_latest:.0f}% — retained earnings are creating new profits, but at a moderate rate.")
        else:
            quality_warnings.append(f"Incremental ROE of {inc_roe_latest:.0f}% — recent retained earnings are barely generating new profits. The latest round of capital reinvestment is underperforming.")

    # VPR
    if vpr:
        if vpr>2:
            quality_signals.append(f"Value creation: ₹1 retained → ₹{vpr:.2f} market cap gain. Management is an excellent allocator of capital — retained earnings compound strongly.")
        elif vpr>1:
            quality_signals.append(f"₹1 retained → ₹{vpr:.2f} market cap. Capital allocation is positive — shareholders get more than they put in.")
        else:
            quality_warnings.append(f"₹1 retained → only ₹{vpr:.2f} market cap. Retained earnings are destroying value. Shareholders would have been better off receiving dividends.")

    n['business_quality'] = {'signals': quality_signals, 'warnings': quality_warnings}

    # ── 2. FINANCIAL HEALTH (balance sheet + debt) ──────────────
    health_signals=[]; health_warnings=[]

    # Debt trajectory
    de_early=avg(d['de'][:3]); de_recent=avg(d['de'][-3:])
    if de_early and de_recent:
        if de_recent<de_early*0.7:
            health_signals.append(f"Debt/Equity fell from ~{de_early:.1f}x (early) to ~{de_recent:.1f}x (recent) — balance sheet is being cleaned up actively. This deleveraging expands future borrowing capacity and reduces financial risk.")
        elif de_recent>de_early*1.3:
            health_warnings.append(f"Debt/Equity rose from ~{de_early:.1f}x to ~{de_recent:.1f}x — the company is taking on more leverage. This amplifies both profits and losses.")

    if de_latest is not None:
        if de_latest<0.5:
            health_signals.append(f"Current D/E of {de_latest:.2f}x is very conservative. Plenty of balance sheet capacity to fund future growth if needed.")
        elif de_latest<1.0:
            health_signals.append(f"D/E of {de_latest:.2f}x — moderate leverage. Interest burden is manageable given current profitability.")
        else:
            health_warnings.append(f"D/E of {de_latest:.2f}x is elevated. In a downturn, interest payments could become a serious burden.")

    # Interest coverage
    if ic_latest:
        if ic_latest>4:
            health_signals.append(f"Interest coverage of {ic_latest:.1f}x (Dr VM method at 12% cost of funds) — operating profit covers interest 4+ times. Very safe from a debt-service perspective.")
        elif ic_latest>2:
            health_signals.append(f"Interest coverage of {ic_latest:.1f}x — adequate buffer but not generous. A 40% profit drop would put interest payments at risk.")
        else:
            health_warnings.append(f"Interest coverage of only {ic_latest:.1f}x — dangerously thin. A moderate revenue decline could make it hard to service debt.")

    # CFO quality
    cfo_pat_pairs=[(d['cfo'][i],d['pat'][i]) for i in range(10) if d['cfo'][i] and d['pat'][i]]
    green_years=sum(1 for c,p in cfo_pat_pairs if c>p)
    if green_years>=7:
        health_signals.append(f"CFO > PAT in {green_years}/10 years — the company consistently generates MORE real cash than reported profits. Profits are not being dressed up.")
    elif green_years>=4:
        health_signals.append(f"CFO > PAT in {green_years}/10 years — cash conversion is reasonable but not stellar.")
    else:
        health_warnings.append(f"CFO > PAT in only {green_years}/10 years — profits are frequently higher than actual cash received. Check for aggressive revenue recognition or bloating receivables.")

    # Cash drain
    cash_trend=trend(d['cash'])
    if cash_trend=='declining':
        health_warnings.append(f"Cash on balance sheet is declining (₹{d['cash'][-1]:.0f} Cr latest vs ₹{d['cash'][0]:.0f} Cr 10 years ago). The business is consuming its cash reserves — watch for upcoming fundraise or cash crunch.")

    n['financial_health'] = {'signals': health_signals, 'warnings': health_warnings}

    # ── 3. OPERATIONAL EFFICIENCY ────────────────────────────────
    ops_signals=[]; ops_warnings=[]

    # NFAT trend
    nfat_t=trend(d['nfat'])
    nfat_early=avg(d['nfat'][:3]); nfat_recent=avg(d['nfat'][-3:])
    if nfat_early and nfat_recent:
        if nfat_recent>nfat_early*1.2:
            ops_signals.append(f"Asset sweating is improving: NFA Turnover rose from {nfat_early:.1f}x to {nfat_recent:.1f}x — the company is generating more revenue per rupee of fixed assets. Existing capacity is being utilised better.")
        elif nfat_recent<nfat_early*0.85:
            ops_warnings.append(f"NFA Turnover fell from {nfat_early:.1f}x to {nfat_recent:.1f}x — either new capacity was added (and not yet fully utilised) or the business is becoming less efficient with its assets.")

    # PBT/NFA signal
    if pbt_nfa_latest:
        if pbt_nfa_latest>25:
            ops_signals.append(f"PBT/NFA of {pbt_nfa_latest:.1f}% (>25% threshold) — excellent returns on fixed assets. Suggests good pricing power or efficient use of physical assets.")
        elif pbt_nfa_latest>10:
            ops_signals.append(f"PBT/NFA of {pbt_nfa_latest:.1f}% — in acceptable zone (10–25%). The asset base is generating reasonable pre-tax profits.")
        else:
            ops_warnings.append(f"PBT/NFA of only {pbt_nfa_latest:.1f}% (<10% danger zone) — fixed assets are barely contributing to profits. Could signal overcapacity, poor pricing, or assets acquired at inflated prices.")

    # Working capital
    wc_early=avg(d['wc_days'][:3]); wc_recent=avg(d['wc_days'][-3:])
    if wc_early and wc_recent:
        if wc_recent<wc_early*0.85:
            ops_signals.append(f"Working capital cycle improved: {wc_early:.0f} days → {wc_recent:.0f} days. Cash is being recovered faster from operations. This reduces funding pressure.")
        elif wc_recent>wc_early*1.2:
            ops_warnings.append(f"Working capital cycle expanded: {wc_early:.0f}d → {wc_recent:.0f}d. Cash is getting stuck longer — in receivables, inventory, or both. This is a silent cash drain.")

    # Receivables
    rd_t=trend(d['rec_days'])
    if rd_t=='declining':
        ops_signals.append(f"Receivable days trending down — customers are paying faster. Reduced credit risk and better cash inflow.")
    elif rd_t=='improving':
        ops_signals.append(f"Receivable days improving — good collection efficiency.")
    elif rd_t in ('volatile','declining'):
        pass
    else:
        rd_late=avg(d['rec_days'][-3:])
        if rd_late and rd_late<40:
            ops_signals.append(f"Receivable days of ~{rd_late:.0f} — very short collection period. Likely OEM customers pay within 30-45 days.")

    # RM months
    rm_early=avg(d['rm_months'][:3]); rm_recent=avg(d['rm_months'][-3:])
    if rm_early and rm_recent and rm_recent>rm_early*1.3:
        ops_warnings.append(f"Raw material stock held has risen from ~{rm_early:.1f} months to ~{rm_recent:.1f} months. Either supply anxiety (fear of shortage) or inefficiency. Ties up more working capital.")

    n['operational'] = {'signals': ops_signals, 'warnings': ops_warnings}

    # ── 4. MOAT ANALYSIS ─────────────────────────────────────────
    moat_signals=[]; moat_warnings=[]

    # Pricing power proxy: OPM stability or improvement despite revenue swings
    opm_v=trend(d['opm'])
    opm_stable_years=sum(1 for i in range(1,10) if d['opm'][i] and d['opm'][i-1] and abs(d['opm'][i]-d['opm'][i-1])<2)
    if opm_stable_years>=6:
        moat_signals.append(f"Operating margins have been relatively stable over 10 years ({opm_stable_years}/9 years within ±2%). This suggests some ability to maintain pricing — a weak moat signal in an otherwise competitive sector.")
    else:
        moat_warnings.append(f"Operating margins fluctuate significantly (stable in only {opm_stable_years}/9 years). This is a sign of limited pricing power — input cost spikes cannot easily be passed on to customers.")

    # Margin level check
    if opm_latest and opm_latest<12:
        moat_warnings.append(f"Operating margins of {opm_latest:.1f}% are thin for a manufacturer. In a commodity/auto-component business, thin margins indicate you are a price-taker, not a price-setter.")
    elif opm_latest and opm_latest>20:
        moat_signals.append(f"Operating margins of {opm_latest:.1f}% are high — suggests either strong brand, proprietary technology, or dominant market position.")

    # Revenue CAGR vs peers proxy
    if sg10:
        if sg10*100>15:
            moat_signals.append(f"10-year revenue CAGR of {sg10*100:.1f}% significantly exceeds India's nominal GDP growth (~10-12%). The company has been gaining market share — a moat signal.")
        else:
            moat_warnings.append(f"10-year revenue CAGR of {sg10*100:.1f}% is close to or below nominal GDP growth. The company may just be growing with the market rather than outgrowing it.")

    # NFA Turnover vs PBT/NFA as quality of assets
    if nfat_latest and pbt_nfa_latest:
        if nfat_latest>2.5 and pbt_nfa_latest>20:
            moat_signals.append(f"High NFA Turnover ({nfat_latest:.1f}x) + strong PBT/NFA ({pbt_nfa_latest:.1f}%) — assets are both well-utilised and highly profitable. This combination suggests scale advantages or operational excellence that is hard for new entrants to replicate.")

    # Competitive moat type detection (qualitative from company name + sector)
    cn_l=cn.lower()
    si_sector=si.get('sector','').lower(); si_ind=si.get('industry','').lower()
    combined=cn_l+si_sector+si_ind

    moat_type=[]
    if any(x in combined for x in ['wheel','auto component','tyre','seal','gasket','bearing']):
        moat_type.append(("Switching Cost Moat (Partial)", "OEM auto-component suppliers enjoy sticky relationships — changing suppliers mid-model cycle is disruptive and costly for OEMs. However, this moat is weak at contract renewal time when OEMs can re-tender. It protects near-term revenue but does not guarantee long-term pricing power."))
        moat_type.append(("Scale + Certification Moat", "Auto-component manufacturers need OEM quality certifications (IATF 16949, etc.) that take years to obtain. New entrants face high certification barriers — but established competitors already have these. Protects against new entrants, not existing competitors."))
        moat_type.append(("No Brand Moat", "End-consumer does not choose auto components by brand. Price and OEM approval are the only selection criteria. No consumer brand moat exists."))
        moat_type.append(("No Pricing Power in Commodities", "With steel as a key input (65% of cost), and no consumer-facing brand, the company cannot easily pass cost increases to customers. OEMs negotiate hard on price. This is a structural margin ceiling."))

    n['moat'] = {'signals': moat_signals, 'warnings': moat_warnings, 'moat_type': moat_type}

    # ── 5. GROWTH SUSTAINABILITY (SSGR framework) ────────────────
    ssgr_signals=[]; ssgr_warnings=[]

    if ssgr_latest:
        if ssgr_latest>20:
            ssgr_signals.append(f"SSGR of {ssgr_latest:.1f}%: The company can sustain >20% annual growth without taking on additional debt. This is exceptional — self-funding growth is the holy grail.")
        elif ssgr_latest>12:
            ssgr_signals.append(f"SSGR of {ssgr_latest:.1f}%: The company can self-fund ~{ssgr_latest:.0f}% annual growth. If the market grows faster than this, expect some debt addition — but it's manageable.")
        elif ssgr_latest>6:
            ssgr_warnings.append(f"SSGR of {ssgr_latest:.1f}%: The self-sustainable growth rate is modest. Growing faster than this requires debt. Check if actual growth rate exceeds SSGR — if so, debt will accumulate.")
        else:
            ssgr_warnings.append(f"SSGR of only {ssgr_latest:.1f}%: Very low internal funding capacity. Almost any meaningful growth will require external capital. High capital intensity + low margins = debt trap risk.")

    # SSGR trend
    ssgr_vals=[v for v in ssgr_list if v is not None]
    if len(ssgr_vals)>=6:
        ssgr_early=avg(ssgr_vals[:3]); ssgr_recent=avg(ssgr_vals[-3:])
        if ssgr_recent>ssgr_early*1.5:
            ssgr_signals.append(f"SSGR has improved dramatically: from ~{ssgr_early:.1f}% to ~{ssgr_recent:.1f}%. The business is becoming more self-sufficient — better margins + better asset turns = less debt dependency.")
        elif ssgr_recent<ssgr_early*0.7:
            ssgr_warnings.append(f"SSGR has fallen from ~{ssgr_early:.1f}% to ~{ssgr_recent:.1f}%. The business is becoming more capital-hungry relative to its profits. Structural concern.")

    n['growth_sustainability'] = {'signals': ssgr_signals, 'warnings': ssgr_warnings, 'ssgr': ssgr_list}

    # ── 6. OVERALL VERDICT ───────────────────────────────────────
    # (Verdict computed in metric interpreter engine below, after all 8 dimensions)

    # ── 7. VALUATION ANALYSIS ───────────────────────────────────
    g_use=g5 or g3 or g10 or 0.10
    fair_pe_graham=8.5+2*(g_use*100)
    fair_pe_lynch=g_use*100
    fair_pe=(fair_pe_graham+fair_pe_lynch)/2
    pe_use=d['pe_ttm'] or d['pe'] or 0
    vs_hist=((pe_use/avg_pe)-1)*100 if avg_pe else None
    peg=round(pe_use/(g_use*100),2) if g_use>0 and pe_use else None
    gpi=((pe_use-8.5)/2) if pe_use else None
    premium=((pe_use/fair_pe)-1)*100 if fair_pe else None

    # Buy/sell signal
    if vs_hist is not None:
        if vs_hist<-10 and (peg or 99)<1.0:
            buy=("#059669","Strong Buy Zone",f"Trading {abs(vs_hist):.0f}% below historical avg PE. PEG of {peg:.2f}x is attractive.")
        elif vs_hist<5 and (peg or 99)<1.5:
            buy=("#22c55e","Reasonable Entry","Near historical avg PE. Not cheap, not expensive. Start a position.")
        elif vs_hist>30:
            buy=("#dc2626","Expensive — Wait",f"{vs_hist:.0f}% above historical avg PE. Let earnings grow into this price.")
        else:
            buy=("#d97706","Accumulate in Tranches","Slight premium. Invest in 3-4 installments over 6-12 months.")
    else:
        buy=("#6b7280","Insufficient Data","Not enough PE history.")

    # 5x scenarios
    cur_eps_v=d['ttm_eps'] or latest(d['eps']) or 1
    bull_g=g5 or 0; base_g=((g5 or 0)+(g10 or g5 or 0))/2; bear_g=min(g10 or 0.10,0.12)
    pe_c=pe_use or avg_pe or 15; pe_a=avg_pe or pe_c; pe_l=d['pe_min'] or pe_c*0.6

    def scen(eg,pend,y=10):
        if not cur_eps_v or not d['current_price']: return None
        return round(cur_eps_v*(1+eg)**y*pend/d['current_price'],2)

    bull_ret=scen(bull_g,pe_c); base_ret=scen(base_g,pe_a); bear_ret=scen(bear_g,pe_l)
    prob5x="High (75%)" if base_ret and base_ret>=5 else ("Moderate (40%)" if base_ret and base_ret>=3 else "Low (<20%)")
    prob5x_color="#059669" if "High" in prob5x else ("#d97706" if "Moderate" in prob5x else "#dc2626")

    n['valuation']={
        'pe':pe_use,'avg_pe':avg_pe,'pe_min':d['pe_min'],'pe_max':d['pe_max'],
        'pb':d['pb'],'pe_pb':d['pe_pb'],'peg':peg,'fair_pe':fair_pe,
        'vs_hist':vs_hist,'premium':premium,'gpi':gpi,'buy':buy,
        'bull_ret':bull_ret,'base_ret':base_ret,'bear_ret':bear_ret,
        'bull_g':bull_g,'base_g':base_g,'bear_g':bear_g,'pe_l':pe_l,
        'prob5x':prob5x,'prob5x_color':prob5x_color,
    }

    # ── 8. RISKS ────────────────────────────────────────────────
    risks=[]
    pats=[v for v in d['pat'] if v is not None]
    down_yrs=sum(1 for i in range(1,len(pats)) if pats[i] is not None and pats[i-1] is not None and pats[i]<pats[i-1])
    if down_yrs>=2:
        risks.append(("Cyclicality",f"Profits fell in {down_yrs}/9 years. This is a cyclical business. Recessions in auto/industrial will periodically compress earnings."))
    if de_latest and de_latest>0.8:
        risks.append(("Leverage",f"D/E of {de_latest:.2f}x. Rising rates or a revenue dip directly hurt net profit. Track quarterly debt levels."))
    if opm_latest and opm_latest<12:
        risks.append(("Thin Margins",f"OPM of {opm_latest:.1f}%. Every Rs.10 rise in raw material costs wipes out a disproportionate share of profit."))
    if g3 and g5 and g3<g5*0.4:
        risks.append(("Decelerating Growth",f"3Y PAT CAGR ({g3*100:.1f}%) is far below 5Y CAGR ({g5*100:.1f}%). Peak growth may be behind the company."))
    if fcf_cfo and fcf_cfo<15:
        risks.append(("Low Free Cash",f"FCF/CFO of {fcf_cfo:.0f}% means very little cash is left after reinvestment. Dividends and debt repayment depend on debt or equity — not free cash."))
    cn_l=cn.lower()
    if any(x in cn_l for x in ['steel','wheel','auto','strip','component']):
        risks.append(("Auto Sector Cyclicality","Auto production is highly cyclical. Festival demand, OEM production schedules, and economic slowdowns create regular boom-bust cycles."))
        risks.append(("Raw Material Price Risk","~65% of revenue goes to raw materials (steel, etc.). A 10% steel price spike can compress OPM by 6-7 percentage points since price pass-through to OEMs is limited."))
        risks.append(("EV Transition","Over the next decade, EVs will change wheel/component requirements. While wheels are still needed for EVs, tyre/rim design is evolving. Monitor management commentary on EV preparedness."))
        risks.append(("OEM Concentration","A small number of OEM customers typically account for 70-80% of revenue. Losing one or a production cut by Maruti/Tata/Hero could materially impact quarterly results."))
    risks.append(("Governance","Not visible in numbers: check promoter pledging, related-party transactions, management guidance vs outcomes."))

    n['risks']=risks

    # ══════════════════════════════════════════════════════════════
    # METRIC INTERPRETER ENGINE — analyses all 80 Sheet-2 metrics
    # across 8 analytical dimensions, joining dots into verdicts
    # ══════════════════════════════════════════════════════════════

    # ── A. ROCE TREND ─────────────────────────────────────────────
    roce_list   = d['roce']
    roce_early  = avg([v for v in roce_list[:3] if v])
    roce_recent = avg([v for v in roce_list[-3:] if v])
    roce_int    = {'signals':[], 'warnings':[], 'data': roce_list}

    if roce_recent and roce_early:
        if roce_recent > roce_early * 1.3:
            roce_int['signals'].append(
                f"ROCE has expanded from ~{roce_early:.1f}% to ~{roce_recent:.1f}% — "
                f"the company is earning significantly more on every rupee of capital deployed. "
                f"This could signal pricing power, operational leverage, or debt reduction.")
        elif roce_recent < roce_early * 0.75:
            roce_int['warnings'].append(
                f"ROCE has deteriorated from ~{roce_early:.1f}% to ~{roce_recent:.1f}%. "
                f"Capital is becoming less productive. Could mean overcapacity, margin compression, "
                f"or acquisitions that have not yet earned their keep.")
        else:
            roce_int['signals'].append(
                f"ROCE is broadly stable (~{roce_early:.1f}% → ~{roce_recent:.1f}%). "
                f"Capital efficiency is consistent.")

    if roce_recent:
        if roce_recent > 35:
            roce_int['signals'].append(f"ROCE of {roce_recent:.1f}% is excellent (Dr VM threshold: >35%). Minimal competition eroding returns.")
        elif roce_recent < 10:
            roce_int['warnings'].append(f"ROCE of {roce_recent:.1f}% is below Dr VM's 10% minimum. Business is barely covering its cost of capital.")

    n['roce_analysis'] = roce_int

    # ── B. ASSET TURNOVER (NFA & WC) ──────────────────────────────
    nfat_list    = d['nfat']
    nfat_early   = avg([v for v in nfat_list[:3] if v])
    nfat_recent  = avg([v for v in nfat_list[-3:] if v])
    at_int       = {'signals':[], 'warnings':[], 'nfat_data': nfat_list}

    if nfat_recent and nfat_early:
        change = (nfat_recent - nfat_early) / nfat_early * 100
        if change > 20:
            at_int['signals'].append(
                f"Asset sweating improved: NFA Turnover {nfat_early:.1f}x → {nfat_recent:.1f}x (+{change:.0f}%). "
                f"Same fixed assets now generating more revenue — either better capacity utilisation or "
                f"growth without proportional capex (asset-light momentum).")
        elif change < -20:
            at_int['warnings'].append(
                f"Asset utilisation fell: NFA Turnover {nfat_early:.1f}x → {nfat_recent:.1f}x ({change:.0f}%). "
                f"Possible causes: large capex not yet generating revenue (CWIP converting), "
                f"revenue slowdown on same asset base, or recent acquisitions at premium.")

    # Dep % of NFA — asset age proxy
    dep_nfa_latest = latest([v for v in d['dep_pct_nfa'] if v])
    dep_nfa_early  = avg([v for v in d['dep_pct_nfa'][:3] if v])
    if dep_nfa_latest and dep_nfa_early:
        if dep_nfa_latest > dep_nfa_early * 1.3:
            at_int['warnings'].append(
                f"Depreciation % of NFA rising ({dep_nfa_early:.1f}% → {dep_nfa_latest:.1f}%). "
                f"Asset base is ageing faster than it is being renewed. Capex needed soon to maintain capacity.")
        elif dep_nfa_latest < dep_nfa_early * 0.8:
            at_int['signals'].append(
                f"Depreciation % of NFA falling — new, longer-lived assets being added. "
                f"Recent capex has extended the useful life of the asset base.")

    # NFA + CWIP — capacity pipeline
    nfa_cwip = d['nfa_plus_cwip']
    nfc_early  = avg([v for v in nfa_cwip[:3] if v])
    nfc_recent = avg([v for v in nfa_cwip[-3:] if v])
    if nfc_early and nfc_recent and nfc_recent > nfc_early * 1.5:
        cwip_latest = latest([v for v in d['cwip'] if v])
        at_int['signals'].append(
            f"NFA+CWIP has grown {nfc_early:.0f}→{nfc_recent:.0f} Cr — significant capacity expansion underway. "
            + (f"CWIP of ₹{cwip_latest:.0f} Cr suggests projects still in pipeline." if cwip_latest else ""))

    n['asset_turnover_analysis'] = at_int

    # ── C. WORKING CAPITAL CYCLE ──────────────────────────────────
    wc_int = {'signals':[], 'warnings':[],
              'rec_days': d['rec_days'], 'inv_days': d['inv_days'], 'wc_days': d['wc_days']}

    wc_early  = avg([v for v in d['wc_days'][:3] if v])
    wc_recent = avg([v for v in d['wc_days'][-3:] if v])
    rd_recent = avg([v for v in d['rec_days'][-3:] if v])
    id_recent = avg([v for v in d['inv_days'][-3:] if v])
    rm_m      = latest([v for v in d['rm_months'] if v])

    if wc_early and wc_recent:
        delta = wc_recent - wc_early
        if delta < -15:
            wc_int['signals'].append(
                f"WC cycle compressed by {abs(delta):.0f} days ({wc_early:.0f}d → {wc_recent:.0f}d). "
                f"Cash moves through the business faster — lower funding need, less interest cost.")
        elif delta > 15:
            wc_int['warnings'].append(
                f"WC cycle expanded by {delta:.0f} days ({wc_early:.0f}d → {wc_recent:.0f}d). "
                f"Cash is getting trapped longer. At current sales, this additional {delta:.0f} days "
                f"ties up an extra ₹{latest(d['sales']) * delta / 365:.0f} Cr of working capital.")

    if rd_recent and rd_recent < 35:
        wc_int['signals'].append(
            f"Receivable days of ~{rd_recent:.0f} days — very fast collection. "
            f"Likely OEM-style advance or near-cash payment terms. Low credit risk.")
    elif rd_recent and rd_recent > 75:
        wc_int['warnings'].append(
            f"Receivable days of ~{rd_recent:.0f} days — customers are slow to pay. "
            f"Track if this is rising: bloating receivables is an early sign of channel stuffing or bad debt.")

    if rm_m and rm_m > 4:
        wc_int['warnings'].append(
            f"Holding {rm_m:.1f} months of raw material as inventory — well above the 2-3 month norm. "
            f"Either supply anxiety, commodity hoarding, or operational inefficiency.")
    elif rm_m and rm_m < 2:
        wc_int['signals'].append(
            f"Only {rm_m:.1f} months of RM in stock — lean, just-in-time operations. "
            f"Low holding cost, but supply disruption risk if vendor issues arise.")

    n['wc_analysis'] = wc_int

    # ── D. REINVESTMENT RATE ──────────────────────────────────────
    ri_int = {'signals':[], 'warnings':[], 'data': d['reinvestment_rate']}

    ri_recent = avg([v for v in d['reinvestment_rate'][-3:] if v is not None])
    fcf_cfo   = d['fcf_cfo']
    tot_capex = sum(v for v in d['capex'] if v)
    tot_dep   = sum(v for v in d['dep'] if v)

    if ri_recent is not None:
        if ri_recent > 2.0:
            ri_int['signals'].append(
                f"Reinvestment rate of {ri_recent:.1f}x — company is investing aggressively (capex >> depreciation + FCF). "
                f"High growth mode. Expect future capacity to drive revenue; short-term FCF will be suppressed.")
        elif ri_recent > 1.0:
            ri_int['signals'].append(
                f"Reinvestment rate of {ri_recent:.1f}x — investing moderately above maintenance level. "
                f"Balanced approach: growing capacity while still generating some free cash.")
        elif ri_recent > 0:
            ri_int['warnings'].append(
                f"Reinvestment rate of {ri_recent:.1f}x — investing below its own depreciation + FCF. "
                f"The company may be harvesting the business rather than growing it. "
                f"Fine if sector is mature; concerning if growth is expected.")

    if fcf_cfo is not None:
        if fcf_cfo > 40:
            ri_int['signals'].append(
                f"FCF/CFO ratio of {fcf_cfo:.0f}% — large portion of operating cash converts to free cash. "
                f"Low maintenance capex; business funds itself and has capacity to return capital or grow.")
        elif fcf_cfo < 0:
            ri_int['warnings'].append(
                f"Negative FCF/CFO — over 10 years total capex exceeded operating cash. "
                f"Growth has been funded externally. Sustainable only if ROCE on new assets is high.")

    if tot_capex and tot_dep:
        capex_to_dep = tot_capex / tot_dep
        if capex_to_dep > 2.5:
            ri_int['signals'].append(
                f"10-year capex is {capex_to_dep:.1f}× depreciation — significantly expanding asset base, not just maintaining it.")
        elif capex_to_dep < 1.2:
            ri_int['warnings'].append(
                f"10-year capex is only {capex_to_dep:.1f}× depreciation — barely above maintenance. "
                f"Limited capacity expansion; growth must come from efficiency or pricing, not volume.")

    n['reinvestment_analysis'] = ri_int

    # ── E. SHAREHOLDER DILUTION ────────────────────────────────────
    dil_int = {'signals':[], 'warnings':[], 'data': d['adj_sh_series']}

    dil_pct = d['share_dilution_pct']
    if dil_pct is not None:
        if dil_pct > 20:
            dil_int['warnings'].append(
                f"Share count grew {dil_pct:.1f}% over 10 years — significant dilution. "
                f"Existing shareholders now own a smaller slice. EPS growth is overstated vs profit growth. "
                f"Check: was dilution for acquisitions (acceptable), ESOP (moderate), or cash raises (red flag)?")
        elif dil_pct > 5:
            dil_int['warnings'].append(
                f"Mild dilution of {dil_pct:.1f}% — likely ESOP or small equity raises. "
                f"Monitor trend; dilution compounds like interest in reverse.")
        elif abs(dil_pct) <= 5:
            dil_int['signals'].append(
                f"Share count almost unchanged ({dil_pct:+.1f}% over 10 years). "
                f"Management has not diluted shareholders. EPS growth is genuine profit growth.")
        else:
            dil_int['signals'].append(
                f"Share count reduced {abs(dil_pct):.1f}% — possible buybacks. "
                f"Management returning capital to shareholders; EPS boosted even without profit growth.")

    # Bonus shares check — large step changes in share count
    sh_series = [v for v in d['adj_sh'] if v]
    if len(sh_series) > 2:
        for i in range(1, len(sh_series)):
            ratio = sh_series[i] / sh_series[i-1] if sh_series[i-1] else 1
            if ratio > 1.8:
                dil_int['signals'].append(
                    f"Large stock split or bonus issue detected (~{ratio:.1f}x share count jump). "
                    f"Adjusted EPS accounts for this; it is not economic dilution.")
                break

    n['dilution_analysis'] = dil_int

    # ── F. CYCLICALITY ─────────────────────────────────────────────
    cyc_int = {'signals':[], 'warnings':[]}

    pat_down  = d['pat_down_years']
    sales_down= d['sales_down_years']
    pat_valid = [v for v in d['pat'] if v is not None]
    n_yrs     = len(pat_valid) - 1 if pat_valid else 1

    if pat_down >= 4:
        cyc_int['warnings'].append(
            f"Profits fell in {pat_down}/{n_yrs} years — highly cyclical business. "
            f"Expect regular multi-year down cycles. Do not value at peak earnings; "
            f"use normalised/mid-cycle PAT for fair value calculations.")
    elif pat_down >= 2:
        cyc_int['warnings'].append(
            f"Profits fell in {pat_down}/{n_yrs} years — moderate cyclicality. "
            f"The business has economic sensitivity; budget for occasional bad years.")
    else:
        cyc_int['signals'].append(
            f"Profits grew or held steady in {n_yrs - pat_down}/{n_yrs} years — low cyclicality. "
            f"Relatively defensive earnings profile.")

    # Tax rate volatility — detects one-offs
    tax_vals = [v for v in d['tax_pct'] if v is not None]
    if tax_vals:
        tax_avg = sum(tax_vals)/len(tax_vals)
        tax_volatile = sum(1 for v in tax_vals if abs(v - tax_avg) > 10)
        if tax_volatile >= 3:
            cyc_int['warnings'].append(
                f"Tax rate is volatile (avg {tax_avg:.0f}%, deviates >10pp in {tax_volatile} years). "
                f"Suggests deferred tax adjustments, MAT credits, or one-time items distorting reported PAT. "
                f"Strip these out before comparing year-to-year earnings.")
        else:
            cyc_int['signals'].append(
                f"Tax rate is stable around {tax_avg:.0f}% — reported PAT is not distorted by tax one-offs.")

    # EBITDA margin stability
    ebitda_margins = [v for v in d['ebitda_margin'] if v is not None]
    if ebitda_margins:
        em_min = min(ebitda_margins); em_max = max(ebitda_margins)
        em_avg = sum(ebitda_margins)/len(ebitda_margins)
        if em_max - em_min > 10:
            cyc_int['warnings'].append(
                f"EBITDA margin swings from {em_min:.1f}% to {em_max:.1f}% (range {em_max-em_min:.0f}pp). "
                f"Margins are highly sensitive to volumes or input costs. Fixed cost leverage works both ways.")
        else:
            cyc_int['signals'].append(
                f"EBITDA margin is relatively stable ({em_min:.1f}%–{em_max:.1f}%), avg {em_avg:.1f}%. "
                f"The business absorbs revenue swings without dramatic margin collapse.")

    n['cyclicality_analysis'] = cyc_int

    # ── G. CAPITAL ALLOCATION ─────────────────────────────────────
    ca_int = {'signals':[], 'warnings':[]}

    vpr   = d['vpr']
    inc_r = latest([v for v in d['inc_roe'] if v])
    div_fcfe = d['div_vs_fcfe2']
    surplus_latest = latest([v for v in d['surplus_funds'] if v])
    total_div_10y  = d['total_div_10y']
    total_fcfe2    = d['total_fcfe2_10y']
    debt_chg       = d['debt_change_10y']

    if vpr is not None:
        if vpr > 2:
            ca_int['signals'].append(
                f"₹1 retained → ₹{vpr:.2f} market cap: exceptional capital allocation. "
                f"Retained earnings are being reinvested at above-market returns.")
        elif vpr > 1:
            ca_int['signals'].append(
                f"₹1 retained → ₹{vpr:.2f} market cap: positive but not outstanding. "
                f"Management creates more value than it consumes through retention.")
        else:
            ca_int['warnings'].append(
                f"₹1 retained → only ₹{vpr:.2f} market cap: value destruction. "
                f"Shareholders would have been better off receiving this as dividends and reinvesting themselves.")

    if inc_r is not None:
        if inc_r > 20:
            ca_int['signals'].append(
                f"Incremental ROE (3Y rolling) of {inc_r:.0f}% — each new rupee reinvested "
                f"is generating exceptional new profits. Management is finding high-return opportunities.")
        elif inc_r < 5:
            ca_int['warnings'].append(
                f"Incremental ROE of {inc_r:.0f}% — recent reinvestment is barely creating new profits. "
                f"The marginal project quality is deteriorating; returns are being diluted by low-return capex.")

    if div_fcfe is not None:
        if div_fcfe > 80:
            ca_int['warnings'].append(
                f"Paying out {div_fcfe:.0f}% of FCFE2 as dividends — very high payout. "
                f"Little retained for reinvestment. Fine if sector is mature; limits growth potential.")
        elif div_fcfe < 15:
            ca_int['signals'].append(
                f"Only {div_fcfe:.0f}% of FCFE2 paid as dividends — retaining most free cash for reinvestment. "
                f"Bet on management to deploy it well (check VPR and incremental ROE above).")

    if surplus_latest is not None:
        if surplus_latest > 0:
            ca_int['signals'].append(
                f"Cumulative net cash generation is positive (₹{surplus_latest:.0f} Cr surplus). "
                f"Over 10 years, the business generated more cash than it consumed. Self-funding company.")
        else:
            ca_int['warnings'].append(
                f"Cumulative net cash generation is negative (₹{abs(surplus_latest):.0f} Cr deficit). "
                f"Over 10 years, total consumption (capex + interest + dividends) exceeded free cash generated. "
                f"Gap funded by debt or equity. Check if new capacity justifies the funding cost.")

    if debt_chg is not None:
        if debt_chg < 0:
            ca_int['signals'].append(
                f"Total debt reduced by ₹{abs(debt_chg):.0f} Cr over 10 years — deleveraging while growing. "
                f"Ideal capital allocation: growing sales without needing more debt.")
        elif debt_chg > 0:
            pct_chg = debt_chg / (d['borrow'][0] or 1) * 100 if d['borrow'][0] else 0
            if pct_chg > 100:
                ca_int['warnings'].append(
                    f"Debt grew ₹{debt_chg:.0f} Cr (+{pct_chg:.0f}%) over 10 years. "
                    f"Significant leverage buildup. Acceptable only if ROCE on new investments > cost of debt.")
            else:
                ca_int['signals'].append(
                    f"Debt grew modestly ₹{debt_chg:.0f} Cr (+{pct_chg:.0f}%) over 10 years — manageable.")

    n['capital_allocation_analysis'] = ca_int

    # ── H. GROWTH SUSTAINABILITY (extended SSGR + net cash gen) ───
    gs_int = {'signals':[], 'warnings':[], 'ssgr': d['ssgr'],
              'net_cash_gen': d['net_cash_gen'], 'surplus': d['surplus_funds']}

    ssgr_latest = latest([v for v in d['ssgr'] if v])
    sg5 = d['sales_cagr'].get('5y')

    if ssgr_latest:
        if ssgr_latest > 20:
            gs_int['signals'].append(
                f"SSGR of {ssgr_latest:.1f}%: company can self-fund >20%/yr growth debt-free. Exceptional.")
        elif ssgr_latest > 12:
            gs_int['signals'].append(
                f"SSGR of {ssgr_latest:.1f}%: self-funding capacity is healthy. "
                f"Growth up to {ssgr_latest:.0f}%/yr requires no new debt.")
        elif ssgr_latest > 6:
            gs_int['warnings'].append(
                f"SSGR of {ssgr_latest:.1f}%: modest self-funding capacity. "
                f"If actual growth exceeds {ssgr_latest:.0f}%/yr, debt or equity will be needed.")
        else:
            gs_int['warnings'].append(
                f"SSGR of only {ssgr_latest:.1f}%: very limited internal funding. "
                f"Almost any growth scenario requires external capital. High debt risk if growth is forced.")

    if sg5 and ssgr_latest:
        gap = sg5*100 - ssgr_latest
        if gap > 8:
            gs_int['warnings'].append(
                f"Growth gap: actual sales CAGR ({sg5*100:.1f}%) exceeds SSGR ({ssgr_latest:.1f}%) by {gap:.1f}pp. "
                f"This {gap:.1f}pp gap has been funded by debt or equity each year. "
                f"If the company wants to sustain this growth, the balance sheet will keep stretching.")
        elif gap < 0:
            gs_int['signals'].append(
                f"Sales growth ({sg5*100:.1f}%/yr) is below SSGR ({ssgr_latest:.1f}%). "
                f"The company is growing within its internal funding capacity — balance sheet is self-healing.")

    # Net cash gen trend — ultimate sustainability check
    ncg = [v for v in d['net_cash_gen'] if v is not None]
    if ncg:
        pos_years = sum(1 for v in ncg if v > 0)
        if pos_years >= len(ncg) * 0.7:
            gs_int['signals'].append(
                f"Net cash generation positive in {pos_years}/{len(ncg)} years — "
                f"business consistently creates more cash than it consumes in total (capex+debt+div).")
        else:
            gs_int['warnings'].append(
                f"Net cash generation negative in {len(ncg)-pos_years}/{len(ncg)} years — "
                f"regularly consumes more than it generates. Long-term funding gap requires monitoring.")

    n['growth_sustainability_ext'] = gs_int

    # ── FINAL VERDICT — incorporate all 8 dimensions ───────────────
    all_signals = (quality_signals + health_signals + ops_signals + moat_signals + ssgr_signals
                   + roce_int['signals'] + at_int['signals'] + wc_int['signals']
                   + ri_int['signals'] + dil_int['signals'] + cyc_int['signals']
                   + ca_int['signals'] + gs_int['signals'])
    all_warnings= (quality_warnings + health_warnings + ops_warnings + moat_warnings + ssgr_warnings
                   + roce_int['warnings'] + at_int['warnings'] + wc_int['warnings']
                   + ri_int['warnings'] + dil_int['warnings'] + cyc_int['warnings']
                   + ca_int['warnings'] + gs_int['warnings'])

    green=len(all_signals); red=len(all_warnings)
    score=round(green/(green+red)*100) if (green+red) else 50

    if score>=70:   verdict,vcol,vemoji="BUY — Strong fundamentals with manageable risks","#059669","✅"
    elif score>=55: verdict,vcol,vemoji="WATCH — Good business but monitor key risks","#d97706","🟡"
    elif score>=40: verdict,vcol,vemoji="CAUTIOUS — Mixed signals, needs improvement","#f97316","⚠️"
    else:           verdict,vcol,vemoji="AVOID — Too many structural concerns","#dc2626","❌"

    n['verdict']={'text':verdict,'color':vcol,'emoji':vemoji,'score':score,'green':green,'red':red}

    # ── 9. PORTFOLIO ALLOCATION ──────────────────────────────────
    checks=[(roe_latest or 0)>15,(de_latest or 99)<0.75,(opm_latest or 0)>10,
            (fcf_cfo or 0)>15,(g5 or 0)>0.12,(peg or 99)<1.5,
            (vpr or 0)>1,(ic_latest or 0)>3]
    green_c=sum(1 for c in checks if c)
    base_alloc=2+green_c/len(checks)*6
    if premium and premium>40: base_alloc*=0.6
    if de_latest and de_latest>1.5: base_alloc*=0.7
    n['alloc']=round(min(base_alloc,8),1)
    n['alloc_green']=green_c; n['alloc_total']=len(checks)

    # ── 10. RUN ALL 6 ADVANCED ENGINES ───────────────────────────
    n['dcf']        = compute_dcf_analysis(d)
    n['moat_score'] = compute_moat_score(d)
    n['mgmt_score'] = compute_mgmt_score(d)
    n['cyclicality']= compute_cyclicality(d)
    n['red_flags']  = compute_red_flags(d)
    sector_label    = detect_sector(d['company_name'],
                                    si.get('sector',''), si.get('industry',''))
    n['sector_label']= sector_label
    n['sector_cmp']  = compute_sector_comparison(d, sector_label)

    # ── 11. COMBINED VERDICT — synthesises all 6 engines ──────────
    n['combined'] = compute_combined_verdict(
        n['moat_score'], n['mgmt_score'], n['dcf'],
        n['cyclicality'], n['red_flags'], n['sector_cmp'],
        n['valuation'], d['current_price']
    )

    return n


# ─────────────────────── HTML render ───────────────────────
def render(d, si, n, holdings, total_inv, total_val, url, now):
    cn=d['company_name']
    val=n['valuation']; buy=val['buy']

    pe_v   = f"{val['pe']:.1f}x"  if val['pe']  else "N/A"
    avgpe_v= f"{val['avg_pe']:.1f}x" if val['avg_pe'] else "N/A"
    pb_v   = f"{val['pb']:.1f}x"  if val['pb']  else "N/A"
    peg_v  = f"{val['peg']:.2f}"  if val['peg'] else "N/A"
    pepb_v = f"{val['pe_pb']:.1f}" if val['pe_pb'] else "N/A"
    gpi_v  = f"{val['gpi']:.1f}%" if val['gpi'] else "N/A"

    g5=d['pat_cagr'].get('5y'); g3=d['pat_cagr'].get('3y'); g10=d['pat_cagr'].get('10y')
    sg5=d['sales_cagr'].get('5y'); sg10=d['sales_cagr'].get('10y')

    # Cagr table row helper
    def crow(label,dc,good=0.12,warn=0.06):
        def cell(k):
            v=dc.get(k)
            if v is None: return '<td style="color:#9ca3af">—</td>'
            pv=v*100
            c='good' if pv>=good*100 else ('bad' if pv<warn*100 else 'warn')
            return f'<td class="{c}">{pv:.1f}%</td>'
        return f'<tr><td>{label}</td>'+cell('10y')+cell('5y')+cell('3y')+cell('ttm')+'</tr>'

    # Narrative signal cards
    def sig_block(signals,warnings,show_title=True):
        h=""
        for s in signals:
            h+=f'<div class="sig-card sig-green">✅ {s}</div>'
        for w in warnings:
            h+=f'<div class="sig-card sig-red">⚠ {w}</div>'
        return h or '<div class="sig-card sig-neutral">No significant signals detected.</div>'

    # Metrics table row
    def mrow(label, val_str, cls='', tooltip=''):
        tt = f'title="{tooltip}"' if tooltip else ''
        return f'<tr {tt}><td class="qlbl">{label}</td><td class="qval {cls}">{val_str}</td></tr>\n'

    ssgr_latest=latest(d['ssgr']); nfat_latest=latest(d['nfat'])
    pbt_nfa_latest=latest(d['pbt_nfa']); ic_latest=latest(d['ic_dvm'])
    inc_roe_latest=latest([x for x in d['inc_roe'] if x])
    wc_latest=latest(d['wc_days']); rd_latest=latest(d['rec_days'])
    rm_months_latest=latest(d['rm_months']); de_latest=latest(d['de'])
    roe_latest=latest(d['roe']); roce_latest=latest(d['roce'])
    opm_latest=latest(d['opm']); npm_latest=latest(d['npm'])
    fcf_latest=latest(d['fcf']); cfo_latest=latest(d['cfo'])
    dpay_latest=latest(d['dpay'])

    # Scorecard rows
    sc = ""
    sc += mrow("Revenue (Latest FY)", cr(latest(d['sales'])))
    sc += mrow("Revenue TTM (Last 4Q)", cr(d['ttm_sales']))
    sc += mrow("Net Profit (Latest FY)", cr(latest(d['pat'])))
    sc += mrow("Net Profit TTM", cr(d['ttm_pat']))
    sc += mrow("EPS TTM", f"₹{d['ttm_eps']:.2f}" if d['ttm_eps'] else "N/A")
    sc += mrow("P/E (TTM)", pe_v,
               'good' if val['pe'] and val['avg_pe'] and val['pe']<val['avg_pe'] else ('bad' if val['pe'] and val['pe']>30 else 'warn'),
               "Price / TTM Earnings. Lower vs historical avg = cheaper")
    sc += mrow("Hist. Avg P/E (10Y)", avgpe_v, tooltip="Avg PE over 10 years. Benchmark for current valuation")
    sc += mrow("P/E Range (10Y)", f"{fmt(val['pe_min'])}x — {fmt(val['pe_max'])}x", tooltip="Min/Max PE seen over last 10 years")
    sc += mrow("P/B Ratio", pb_v,
               'good' if val['pb'] and val['pb']<2 else ('bad' if val['pb'] and val['pb']>5 else 'warn'),
               "Price / Book Value. Below 2 = reasonable")
    sc += mrow("P/E × P/B", pepb_v,
               'bad' if val['pe_pb'] and val['pe_pb']>22.5 else 'good',
               "Graham's composite. Above 22.5 = expensive by his rule")
    sc += mrow("PEG Ratio", peg_v,
               'good' if val['peg'] and val['peg']<1 else ('bad' if val['peg'] and val['peg']>2 else 'warn'),
               "PE / Growth rate. <1 = paying less than growth justifies. >2 = expensive")
    sc += mrow("Growth Priced In (Graham)", gpi_v, tooltip="Market implicitly expects this much annual profit growth")
    sc += mrow("ROE (Latest)", f"{fmt(roe_latest)}%",
               'good' if roe_latest and roe_latest>20 else ('bad' if roe_latest and roe_latest<10 else 'warn'),
               "Return on Equity. Dr VM: <7%=bad, >25%=excellent")
    sc += mrow("ROCE (Latest)", f"{fmt(roce_latest)}%",
               'good' if roce_latest and roce_latest>25 else ('bad' if roce_latest and roce_latest<10 else 'warn'),
               "Return on Capital Employed. Dr VM: <10%=bad, >35%=excellent")
    sc += mrow("PBT/Avg NFA", f"{fmt(pbt_nfa_latest)}%",
               'good' if pbt_nfa_latest and pbt_nfa_latest>25 else ('bad' if pbt_nfa_latest and pbt_nfa_latest<10 else 'warn'),
               "Pre-tax profit per ₹100 of fixed assets. Dr VM: <10%=bad, >25%=good")
    sc += mrow("NFA Turnover", f"{fmt(nfat_latest)}x",
               'good' if nfat_latest and nfat_latest>3 else ('warn' if nfat_latest and nfat_latest>1.5 else 'bad'),
               "Sales per ₹1 of fixed assets. Higher = better asset utilisation")
    sc += mrow("SSGR (Latest)", f"{fmt(ssgr_latest)}%",
               'good' if ssgr_latest and ssgr_latest>15 else ('warn' if ssgr_latest and ssgr_latest>8 else 'bad'),
               "Self-Sustainable Growth Rate: max growth without new debt. NPM × NFA_Turnover × (1-payout)")
    sc += mrow("Operating Margin", f"{fmt(opm_latest)}%",
               'good' if opm_latest and opm_latest>20 else ('bad' if opm_latest and opm_latest<8 else 'warn'),
               "Operating Profit / Sales. Measures core business profitability before interest & tax")
    sc += mrow("Net Profit Margin", f"{fmt(npm_latest)}%",
               'good' if npm_latest and npm_latest>10 else ('bad' if npm_latest and npm_latest<4 else 'warn'),
               "PAT / Sales. What % of every ₹100 revenue ends up as profit")
    sc += mrow("Debt / Equity", f"{fmt(de_latest)}x",
               'good' if de_latest is not None and de_latest<0.5 else ('bad' if de_latest and de_latest>1.5 else 'warn'),
               "Total Debt / Equity. Lower = safer. >1.5 = high risk territory")
    sc += mrow("Interest Coverage (Dr VM)", f"{fmt(ic_latest)}x",
               'good' if ic_latest and ic_latest>4 else ('bad' if ic_latest and ic_latest<2 else 'warn'),
               "OP / (12% × avg debt). Conservative measure: can company cover ALL interest if cost = 12%?")
    sc += mrow("CFO > PAT (years / 10)", f"{sum(1 for c,p in zip(d['cfo'],d['pat']) if c and p and c>p)}/10",
               tooltip="How often real cash > reported profit. Higher = more trustworthy earnings")
    sc += mrow("FCF/CFO (10yr)", f"{fmt(d['fcf_cfo'])}%",
               'good' if d['fcf_cfo'] and d['fcf_cfo']>25 else ('bad' if d['fcf_cfo'] and d['fcf_cfo']<0 else 'warn'),
               "What % of operating cash becomes Free Cash after capex. Dr VM: >25% = healthy. <0% = consuming cash")
    sc += mrow("Incremental ROE (3Y Rolling)", f"{fmt(inc_roe_latest)}%",
               'good' if inc_roe_latest and inc_roe_latest>15 else ('bad' if inc_roe_latest and inc_roe_latest<5 else 'warn'),
               "New profits generated per ₹1 of retained earnings over any 3-year window. Measures quality of reinvestment")
    sc += mrow("Value per ₹1 Retained", f"₹{fmt(d['vpr'])}" if d['vpr'] else "N/A",
               'good' if d['vpr'] and d['vpr']>2 else ('bad' if d['vpr'] and d['vpr']<1 else 'warn'),
               "MCap gain / total retained earnings. >₹1 = management creates value. <₹1 = destroying value")
    sc += mrow("Working Capital Cycle", f"{fmt(wc_latest)} days",
               'good' if wc_latest and wc_latest<60 else ('bad' if wc_latest and wc_latest>120 else 'warn'),
               "Receivable days + Inventory days. How long cash is stuck. Lower = better")
    sc += mrow("Receivable Days", f"{fmt(rd_latest)} days",
               'good' if rd_latest and rd_latest<40 else ('bad' if rd_latest and rd_latest>75 else 'warn'),
               "How long customers take to pay. Lower = better. OEMs typically 30-45 days")
    sc += mrow("RM Months in Stock", f"{fmt(rm_months_latest)} months",
               'good' if rm_months_latest and rm_months_latest<2 else ('bad' if rm_months_latest and rm_months_latest>4 else 'warn'),
               "Raw material inventory held as months of requirement. Lower = leaner operations")
    sc += mrow("Dividend Payout", f"{fmt(dpay_latest)}%", tooltip="Div/PAT. % of profit returned as dividend. Rest is retained for growth")
    sc += mrow("Div Yield", pct(d['div_yield']) if d['div_yield'] else "N/A", tooltip="Annual dividend / current market price")
    sc += mrow("MCap CAGR (10Y)", pct(d['mcap_cagr']) if d['mcap_cagr'] else "N/A", tooltip="How fast market cap compounded over 10 years. Should track earnings CAGR")

    # Cost structure HTML
    cost_rows=""
    for k,v in d['costs_pct'].items():
        bar_w=min(v,80)
        cost_rows+=f'<tr><td style="width:150px;font-size:12px;color:#6b7280">{k}</td><td><div style="background:#e5e7eb;border-radius:3px;height:14px;width:100%;max-width:300px"><div style="background:#6366f1;height:14px;border-radius:3px;width:{bar_w/80*100:.0f}%"></div></div></td><td style="font-size:12px;font-weight:600;padding-left:8px">{v:.1f}%</td></tr>'

    # Moat section HTML
    moat_type_html=""
    for title,desc in n['moat'].get('moat_type',[]):
        icon="✅" if "Moat" in title and "No " not in title and "Partial" not in title else ("⚠" if "Partial" in title or "weak" in desc.lower() else "❌")
        moat_type_html+=f'<div class="sig-card {"sig-green" if "✅"==icon else "sig-red" if "❌"==icon else "sig-amber"}"><strong>{icon} {title}</strong><br><span style="font-size:12px">{desc}</span></div>'

    # SSGR chart data
    ssgr_data=jsa(d['ssgr']); ssgr_labels=jsl(d['fy_labels'])

    # About text
    # ── About / Key Points / Pros / Cons ─────────────────────────────────
    about    = si.get('about', '')
    kp       = si.get('key_points', [])   # list of {heading, lines}
    sector   = si.get('sector',   '')
    industry = si.get('industry', '')
    peers    = ', '.join(si.get('peers', [])[:8]) or 'See Screener.in'

    # Fallback: if scraping was blocked (sandbox / login wall), show a neutral prompt
    if not about:
        about = (f"Company description could not be fetched automatically. "
                 f"Visit <a href='{url}' target='_blank'>Screener.in ↗</a> "
                 f"for the full About and Key Points sections.")

    # Build Key Points HTML — each section gets a bold heading + bullet list
    kp_html = ''
    for sec in kp:
        kp_html += f'<div style="margin-top:12px">'
        kp_html += f'<strong style="font-size:12px;color:#1e293b">{sec["heading"]}</strong>'
        kp_html += '<ul style="list-style:disc;padding-left:18px;margin-top:4px">'
        for line in sec['lines']:
            kp_html += f'<li style="font-size:12px;color:#4b5563;padding:2px 0;line-height:1.5">{line}</li>'
        kp_html += '</ul></div>'

    # Pros / Cons from Screener's own analysis
    pros_html = ''.join(
        f'<li style="padding:4px 0;font-size:13px;color:#374151">✅ {p}</li>'
        for p in si.get('pros', []))
    cons_html = ''.join(
        f'<li style="padding:4px 0;font-size:13px;color:#374151">❌ {c}</li>'
        for c in si.get('cons', []))

    pros_cons = ''
    if pros_html or cons_html:
        pros_part  = (f'<div><strong style="font-size:12px;color:#059669">Screener Positives</strong>'
                      f'<ul style="list-style:none;padding:0;margin-top:6px">{pros_html}</ul></div>'
                      if pros_html else '')
        cons_part  = (f'<div><strong style="font-size:12px;color:#dc2626">Screener Concerns</strong>'
                      f'<ul style="list-style:none;padding:0;margin-top:6px">{cons_html}</ul></div>'
                      if cons_html else '')
        pros_cons  = (f'<div style="display:grid;grid-template-columns:1fr 1fr;'
                      f'gap:16px;margin-top:14px">{pros_part}{cons_part}</div>')

    # Portfolio table
    port_rows=""
    for h in holdings:
        pnl=h.get('pnl') or 0; pc='#059669' if pnl>=0 else '#dc2626'
        port_rows+=f'<tr><td style="font-weight:600">{h["name"]}</td><td>₹{(h["avg_cost"] or 0):,.2f}</td><td>₹{(h["ltp"] or 0):,.2f}</td><td>₹{h["invested"]:,.0f}</td><td>₹{h["cur_val"]:,.0f}</td><td style="color:{pc};font-weight:600">₹{pnl:,.0f} ({h.get("net_chg",0):.1f}%)</td></tr>'
    pnl_tot=total_val-total_inv; pnl_pct=pnl_tot/total_inv*100 if total_inv else 0
    pnl_col='#059669' if pnl_tot>=0 else '#dc2626'

    # alloc bar — extract ticker directly from screener URL
    # handles: /company/CGPOWER/, /company/CGPOWER/consolidated/, /company/CGPOWER
    ticker = re.search(r'/company/([^/?#]+)', url)
    ticker = ticker.group(1).upper().strip('/') if ticker else ''

    held_pct = 0
    for h in holdings:
        if h['name'].upper() == ticker:
            held_pct = h['cur_val'] / total_val * 100 if total_val else 0
            break
    alloc=n['alloc']; fill=min(held_pct/alloc*100,100) if alloc else 0
    add_more=max(0,alloc-held_pct)
    alloc_msg=("Already at recommended level." if held_pct>=alloc*0.9
               else f"Consider adding ~{add_more:.1f}% more." if held_pct>0
               else f"Start with {alloc}% if conviction is high.")

    # risks HTML
    risks_html=''.join(
        f'<li style="margin:8px 0;font-size:13px;color:#374151;line-height:1.6"><strong>{t}:</strong> {desc}</li>'
        for t,desc in n['risks'])

    # 5x
    bull_d=f"₹{val['bull_ret']:.1f} lakhs" if val['bull_ret'] else 'N/A'
    base_d=f"₹{val['base_ret']:.1f} lakhs" if val['base_ret'] else 'N/A'
    bear_d=f"₹{val['bear_ret']:.1f} lakhs" if val['bear_ret'] else 'N/A'

    # ── Build HTML for all 6 advanced engines ────────────────────

    def _iv(v): return f"\u20b9{v:.0f}" if v else "N/A"
    def _ud(v):
        if v is None: return "N/A"
        col = '#059669' if v < 0 else '#dc2626'
        return f'<span style="color:{col};font-weight:700">{v:+.0f}%</span>'

    # 1. DCF HTML
    dcf = n.get('dcf') or {}

    sens_tbl = ''
    if dcf.get('sensitivity'):
        sens = dcf['sensitivity']
        wacc_rates = list(list(sens.values())[0].keys()) if sens else []
        sens_tbl = '<div style="margin-top:14px"><div style="font-size:12px;color:#6b7280;margin-bottom:6px"><strong>Sensitivity Table</strong> - Intrinsic Value/share across WACC and growth assumptions<br><span style="font-size:11px">Rows = growth rate assumed; Columns = WACC (cost of capital)</span></div><table style="width:100%;border-collapse:collapse;font-size:12px"><tr><th style="background:#f9fafb;padding:6px 10px;border:1px solid #e5e7eb">Growth / WACC</th>'
        for w in wacc_rates:
            sens_tbl += f'<th style="background:#f9fafb;padding:6px 10px;border:1px solid #e5e7eb;text-align:right">{w}</th>'
        sens_tbl += '</tr>'
        cur = dcf.get('cur_price', 0)
        for g, row in sens.items():
            sens_tbl += f'<tr><td style="padding:6px 10px;border:1px solid #e5e7eb;font-weight:600">{g}</td>'
            for w in wacc_rates:
                iv = row.get(w)
                bg = '#d1fae5' if (iv and cur and iv > cur * 1.3) else ('#fee2e2' if (iv and cur and iv < cur * 0.7) else '#fef9c3')
                sens_tbl += f'<td style="padding:6px 10px;border:1px solid #e5e7eb;text-align:right;background:{bg}">{_iv(iv)}</td>'
            sens_tbl += '</tr>'
        sens_tbl += '</table><div style="font-size:11px;color:#9ca3af;margin-top:4px">Green = stock undervalued vs scenario &nbsp; Red = overvalued &nbsp; Yellow = near fair value</div></div>'

    dcf_html = f'''<div class="sig-card sig-neutral" style="margin-bottom:12px">
      <strong>Method:</strong> 3-Stage DCF. Stage 1 high growth ({pct(dcf.get("g_high"))}/yr, 5Y)
      then fade to {pct(dcf.get("g_mid"))}/yr, terminal at {pct(dcf.get("tg"))} (India nominal GDP).
      Owner Earnings (PAT + Dep - avg 3Y Capex) = <strong>\u20b9{fmt(dcf.get("owner_earnings"))} Cr</strong>
      &nbsp;|&nbsp; WACC = <strong>{pct(dcf.get("wacc"))}</strong>
      &nbsp;|&nbsp; Net Debt = <strong>\u20b9{fmt(dcf.get("net_debt"))} Cr</strong>
    </div>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px">
      <tr style="background:#f9fafb">
        <th style="padding:10px 12px;border:1px solid #e5e7eb;text-align:left">Scenario</th>
        <th style="padding:10px 12px;border:1px solid #e5e7eb;text-align:left">Growth (Stage 1)</th>
        <th style="padding:10px 12px;border:1px solid #e5e7eb;text-align:right">Intrinsic Value/Share</th>
        <th style="padding:10px 12px;border:1px solid #e5e7eb;text-align:right">Current \u20b9{fmt(dcf.get("cur_price"))} is...</th>
      </tr>
      <tr>
        <td style="padding:10px 12px;border:1px solid #e5e7eb">Bull</td>
        <td style="padding:10px 12px;border:1px solid #e5e7eb">{pct(dcf.get("g_high"))}/yr</td>
        <td style="padding:10px 12px;border:1px solid #e5e7eb;text-align:right;font-weight:700">{_iv(dcf.get("bull_iv"))}</td>
        <td style="padding:10px 12px;border:1px solid #e5e7eb;text-align:right">{_ud(dcf.get("bull_updown"))}</td>
      </tr>
      <tr style="background:#f9fafb">
        <td style="padding:10px 12px;border:1px solid #e5e7eb"><strong>Base</strong></td>
        <td style="padding:10px 12px;border:1px solid #e5e7eb">{pct(dcf.get("g_mid"))}/yr</td>
        <td style="padding:10px 12px;border:1px solid #e5e7eb;text-align:right;font-weight:700">{_iv(dcf.get("base_iv"))}</td>
        <td style="padding:10px 12px;border:1px solid #e5e7eb;text-align:right">{_ud(dcf.get("base_updown"))}</td>
      </tr>
      <tr>
        <td style="padding:10px 12px;border:1px solid #e5e7eb">Bear</td>
        <td style="padding:10px 12px;border:1px solid #e5e7eb">{pct(dcf.get("g_low"))}/yr</td>
        <td style="padding:10px 12px;border:1px solid #e5e7eb;text-align:right;font-weight:700">{"&#8804;&#x20b9;0 (net debt > equity value)" if dcf.get("bear_negative") else _iv(dcf.get("bear_iv"))}</td>
        <td style="padding:10px 12px;border:1px solid #e5e7eb;text-align:right">{"<span style=\"color:#dc2626;font-weight:700\">Deeply Overvalued</span>" if dcf.get("bear_negative") else _ud(dcf.get("bear_updown"))}</td>
      </tr>
    </table>
    <div style="display:flex;gap:14px;margin-bottom:12px;flex-wrap:wrap">
      <div style="background:#f0fdf4;border-radius:8px;padding:10px 16px;flex:1;min-width:140px">
        <div style="font-size:11px;color:#6b7280;text-transform:uppercase">Buy Zone (30% MoS)</div>
        <div style="font-size:20px;font-weight:800;color:#059669">{_iv(dcf.get("mos_buy"))}</div>
      </div>
      <div style="background:#fef2f2;border-radius:8px;padding:10px 16px;flex:1;min-width:140px">
        <div style="font-size:11px;color:#6b7280;text-transform:uppercase">Great Buy (40% MoS)</div>
        <div style="font-size:20px;font-weight:800;color:#dc2626">{_iv(dcf.get("mos_great"))}</div>
      </div>
    </div>
    {"<div class=\"sig-card sig-amber\" style=\"font-size:12px;margin-bottom:8px\"><strong>⚠ Cyclicality Warning:</strong> Current earnings (&#x20b9;"+ fmt(dcf.get("cur_price","?"))+" share) appear to be above mid-cycle levels. Mid-cycle PAT estimate: &#x20b9;"+fmt(dcf.get("mid_cycle_pat"))+" Cr. The cycle-adjusted base IV is <strong>&#x20b9;"+(_iv(dcf.get("base_iv_cycle")) if dcf.get("base_iv_cycle") else "very low")+"</strong> — suggesting the stock is more expensive than current-earnings DCF implies. Use the cycle-adjusted IV for conservative valuation of cyclical businesses.</div>" if dcf.get("at_peak") else ""}
    <div class="sig-card sig-neutral" style="font-size:12px;margin-bottom:8px">
      DCF is sensitive to assumptions. A 2% change in WACC or growth moves IV by 30-50%.
      Use this as a <strong>range and direction</strong>, not a precise target.
      The sensitivity table shows how IV changes across scenarios.
    </div>
    {sens_tbl}'''

    # 2. Moat Score HTML
    ms = n.get('moat_score') or {}
    moat_rows = ''
    for b in ms.get('breakdown', []):
        bar_w = round(b[2]/b[3]*100) if b[3] else 0
        moat_rows += f'<tr><td style="padding:8px 12px;border-bottom:1px solid #f3f4f6;font-size:13px">{b[0]}</td><td style="padding:8px 12px;border-bottom:1px solid #f3f4f6;font-size:12px;color:#6b7280">{b[1]}</td><td style="padding:8px 12px;border-bottom:1px solid #f3f4f6;width:100px"><div style="background:#e5e7eb;border-radius:4px;height:8px"><div style="background:#6366f1;height:8px;border-radius:4px;width:{bar_w}%"></div></div></td><td style="padding:8px 12px;border-bottom:1px solid #f3f4f6;font-size:12px;text-align:right;font-weight:600">{b[2]}/{b[3]}</td><td style="padding:8px 12px;border-bottom:1px solid #f3f4f6;font-size:11px;color:#9ca3af">{b[4]}</td></tr>'
    ms_pct = ms.get('pct', 0)
    moat_html = f'''<div style="display:flex;align-items:center;gap:16px;margin-bottom:16px;padding:16px;background:#f9fafb;border-radius:10px">
      <div style="text-align:center;min-width:80px"><div style="font-size:36px;font-weight:900;color:{ms.get("color","#6b7280")}">{ms_pct}%</div>
      <div style="font-size:11px;color:#6b7280">Moat Score</div></div>
      <div><div style="font-size:18px;font-weight:700;color:{ms.get("color","#6b7280")}">{ms.get("label","N/A")}</div>
      <div style="background:#e5e7eb;border-radius:6px;height:10px;width:200px;margin-top:6px">
        <div style="background:{ms.get("color","#6b7280")};height:10px;border-radius:6px;width:{ms_pct}%"></div>
      </div>
      <div style="font-size:12px;color:#6b7280;margin-top:4px">{ms.get("score",0):.0f} / {ms.get("max",100)} pts</div></div>
    </div>
    <table style="width:100%;border-collapse:collapse"><tr style="background:#f9fafb">
      <th style="padding:8px 12px;text-align:left;font-size:11px;color:#6b7280;text-transform:uppercase">Dimension</th>
      <th style="padding:8px 12px;text-align:left;font-size:11px;color:#6b7280;text-transform:uppercase">Value</th>
      <th style="padding:8px 12px;font-size:11px;color:#6b7280;text-transform:uppercase">Bar</th>
      <th style="padding:8px 12px;text-align:right;font-size:11px;color:#6b7280;text-transform:uppercase">Pts</th>
      <th style="padding:8px 12px;font-size:11px;color:#6b7280;text-transform:uppercase">What it measures</th>
    </tr>{moat_rows}</table>'''

    # 3. Management Score HTML
    mgs = n.get('mgmt_score') or {}
    mgmt_rows = ''
    for b in mgs.get('breakdown', []):
        bar_w = round(b[2]/b[3]*100) if b[3] else 0
        mgmt_rows += f'<tr><td style="padding:8px 12px;border-bottom:1px solid #f3f4f6;font-size:13px">{b[0]}</td><td style="padding:8px 12px;border-bottom:1px solid #f3f4f6;font-size:12px;color:#6b7280">{b[1]}</td><td style="padding:8px 12px;border-bottom:1px solid #f3f4f6;width:100px"><div style="background:#e5e7eb;border-radius:4px;height:8px"><div style="background:#10b981;height:8px;border-radius:4px;width:{bar_w}%"></div></div></td><td style="padding:8px 12px;border-bottom:1px solid #f3f4f6;font-size:12px;text-align:right;font-weight:600">{b[2]}/{b[3]}</td><td style="padding:8px 12px;border-bottom:1px solid #f3f4f6;font-size:11px;color:#9ca3af">{b[4]}</td></tr>'
    mgs_pct = mgs.get('pct', 0)
    mgmt_score_html = f'''<div style="display:flex;align-items:center;gap:16px;margin-bottom:16px;padding:16px;background:#f9fafb;border-radius:10px">
      <div style="text-align:center;min-width:80px"><div style="font-size:36px;font-weight:900;color:{mgs.get("color","#6b7280")}">{mgs_pct}%</div>
      <div style="font-size:11px;color:#6b7280">Mgmt Score</div></div>
      <div><div style="font-size:18px;font-weight:700;color:{mgs.get("color","#6b7280")}">{mgs.get("label","N/A")}</div>
      <div style="background:#e5e7eb;border-radius:6px;height:10px;width:200px;margin-top:6px">
        <div style="background:{mgs.get("color","#6b7280")};height:10px;border-radius:6px;width:{mgs_pct}%"></div>
      </div>
      <div style="font-size:12px;color:#6b7280;margin-top:4px">{mgs.get("score",0):.0f} / {mgs.get("max",100)} pts</div></div>
    </div>
    <table style="width:100%;border-collapse:collapse"><tr style="background:#f9fafb">
      <th style="padding:8px 12px;text-align:left;font-size:11px;color:#6b7280;text-transform:uppercase">Dimension</th>
      <th style="padding:8px 12px;text-align:left;font-size:11px;color:#6b7280;text-transform:uppercase">Value</th>
      <th style="padding:8px 12px;font-size:11px;color:#6b7280;text-transform:uppercase">Bar</th>
      <th style="padding:8px 12px;text-align:right;font-size:11px;color:#6b7280;text-transform:uppercase">Pts</th>
      <th style="padding:8px 12px;font-size:11px;color:#6b7280;text-transform:uppercase">What it measures</th>
    </tr>{mgmt_rows}</table>'''

    # 4. Cyclicality HTML
    cyc = n.get('cyclicality') or {}
    cyc_adv = '<br>'.join(cyc.get('advice', []))
    mid_pat = cyc.get('mid_cycle_pat')
    cyc_icon = {'Highly Cyclical':'cyclone','Moderately Cyclical':'wave','Mildly Cyclical':'tilde','Defensive / Secular':'mountain'}.get(cyc.get('label',''), 'wave')
    over_txt = "<strong style='color:#dc2626'>overstates</strong>" if cyc.get('over_earning') else ("<strong style='color:#059669'>understates</strong>" if cyc.get('under_earning') else "<strong style='color:#059669'>fairly reflects</strong>")
    cyc_sc_cls = 'sig-amber' if cyc.get('over_earning') else ('sig-green' if cyc.get('under_earning') else 'sig-neutral')
    cyc_html = f'''<div style="display:flex;align-items:center;gap:16px;margin-bottom:14px;padding:16px;background:#f9fafb;border-radius:10px">
      <div style="font-size:32px">{"🌪️" if "Highly" in cyc.get("label","") else "🌊" if "Moderately" in cyc.get("label","") else "〰️" if "Mildly" in cyc.get("label","") else "🏔️"}</div>
      <div><div style="font-size:18px;font-weight:700;color:{cyc.get("color","#d97706")}">{cyc.get("label","N/A")}</div>
      <div style="font-size:12px;color:#6b7280">Cyclicality score: {cyc.get("score",0)} / 10 (higher = more cyclical)</div></div>
    </div>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:12px">
      <tr><td style="padding:8px 12px;border-bottom:1px solid #f3f4f6;color:#6b7280">Profit decline years</td><td style="padding:8px 12px;border-bottom:1px solid #f3f4f6;font-weight:600">{cyc.get("pat_down",0)} / {len([v for v in d["pat"] if v is not None])-1} years</td></tr>
      <tr><td style="padding:8px 12px;border-bottom:1px solid #f3f4f6;color:#6b7280">Operating margin range</td><td style="padding:8px 12px;border-bottom:1px solid #f3f4f6;font-weight:600">{cyc.get("opm_range",0):.1f} percentage points</td></tr>
      <tr><td style="padding:8px 12px;border-bottom:1px solid #f3f4f6;color:#6b7280">Max PAT drawdown (peak-to-trough)</td><td style="padding:8px 12px;border-bottom:1px solid #f3f4f6;font-weight:600">{cyc.get("max_pat_drawdown",0):.0f}%</td></tr>
      <tr><td style="padding:8px 12px;border-bottom:1px solid #f3f4f6;color:#6b7280">Mid-cycle PAT estimate (median)</td><td style="padding:8px 12px;border-bottom:1px solid #f3f4f6;font-weight:600">\u20b9{fmt(mid_pat)} Cr</td></tr>
    </table>
    <div class="sig-card {cyc_sc_cls}" style="font-size:13px">{cyc_adv}</div>
    <div class="sig-card sig-neutral" style="font-size:12px;margin-top:8px">
      <strong>Valuation note:</strong> For cyclical businesses, never value at peak earnings.
      Use mid-cycle PAT (\u20b9{fmt(mid_pat)} Cr) as the denominator.
      Current-year PAT {over_txt} the normalised earnings power of this business.
    </div>'''

    # 5. Sector Comparison HTML
    scmp = n.get('sector_cmp')
    if scmp:
        sec_rows = ''
        for r in scmp.get('rows', []):
            arrow = 'Above' if r['status']=='ABOVE' else ('Below' if r['status']=='BELOW' else 'Inline')
            arrow_sym = '&#8593;' if r['status']=='ABOVE' else ('&#8595;' if r['status']=='BELOW' else '&#8596;')
            sec_rows += f'<tr><td style="padding:10px 12px;border-bottom:1px solid #f3f4f6;font-size:13px">{r["metric"]}</td><td style="padding:10px 12px;border-bottom:1px solid #f3f4f6;font-size:13px;font-weight:700">{r["fmt"].format(r["company"]) if r["company"] else "N/A"}</td><td style="padding:10px 12px;border-bottom:1px solid #f3f4f6;font-size:13px;color:#6b7280">{r["fmt"].format(r["benchmark"]) if r["benchmark"] else "N/A"}</td><td style="padding:10px 12px;border-bottom:1px solid #f3f4f6;font-size:13px;font-weight:700;color:{r["color"]}">{arrow_sym} {arrow}</td></tr>'
        sector_html = f'''<div style="margin-bottom:12px;padding:14px;background:#f9fafb;border-radius:10px">
          <div style="font-size:16px;font-weight:700;color:{scmp.get("color","#6b7280")}">{scmp.get("verdict","")}</div>
          <div style="font-size:12px;color:#6b7280;margin-top:4px">Sector: <strong>{scmp.get("sector","")}</strong> &nbsp;|&nbsp; {scmp.get("desc","")}</div>
        </div>
        <table style="width:100%;border-collapse:collapse"><tr style="background:#f9fafb">
          <th style="padding:10px 12px;text-align:left;font-size:11px;color:#6b7280;text-transform:uppercase">Metric</th>
          <th style="padding:10px 12px;text-align:left;font-size:11px;color:#6b7280;text-transform:uppercase">This Company</th>
          <th style="padding:10px 12px;text-align:left;font-size:11px;color:#6b7280;text-transform:uppercase">Sector Average</th>
          <th style="padding:10px 12px;text-align:left;font-size:11px;color:#6b7280;text-transform:uppercase">vs Sector</th>
        </tr>{sec_rows}</table>
        <div class="sig-card sig-neutral" style="font-size:12px;margin-top:10px">Sector benchmarks are approximate NSE/BSE averages. Use for directional comparison only.</div>'''
    elif not scmp:
        sector_html = f'<div class="sig-card sig-neutral">Sector auto-detection returned: <strong>{n.get("sector_label") or "None detected"}</strong>. When Screener.in is scraped successfully, sector and industry fields will improve detection accuracy.</div>'

    # Pre-compute sector tile HTML for scorecard grid (avoids dict leakage in f-string)
    _sc = n.get('sector_cmp')
    if _sc:
        _sc_beats   = _sc.get('beats', 0)
        _sc_total   = len(_sc.get('rows', []))
        _sc_color   = _sc.get('color', '#6b7280')
        _sc_verdict = _sc.get('verdict', '')
        _sc_sector  = _sc.get('sector', '')
        sect_tile_html = (
            f'<div style="font-size:1.4rem;font-weight:800;color:{_sc_color}">{_sc_beats}/{_sc_total}</div>'
            f'<div style="font-size:12px;font-weight:600;color:{_sc_color};margin-top:2px">{_sc_verdict}</div>'
            f'<div style="font-size:11px;color:#9ca3af;margin-top:8px">vs {_sc_sector} benchmarks</div>'
        )
    else:
        sect_tile_html = '<div style="font-size:12px;color:#9ca3af">Sector not detected</div>'

    # 6. Red Flags HTML
    rf = n.get('red_flags') or {}
    rf_items = ''
    sev_col = {'HIGH':'#dc2626','MEDIUM':'#f97316','LOW':'#d97706'}
    sev_bg2 = {'HIGH':'#fee2e2','MEDIUM':'#fff7ed','LOW':'#fffbeb'}
    sev_ico = {'HIGH':'&#x1F534;','MEDIUM':'&#x1F7E0;','LOW':'&#x1F7E1;'}
    for flag in rf.get('flags', []):
        c = sev_col.get(flag['sev'], '#6b7280')
        bg = sev_bg2.get(flag['sev'], '#f9fafb')
        ic = sev_ico.get(flag['sev'], '')
        rf_items += f'<div style="background:{bg};border-left:4px solid {c};border-radius:0 8px 8px 0;padding:12px 16px;margin-bottom:8px"><div style="font-size:13px;font-weight:700;color:{c}">{ic} [{flag["sev"]}] {flag["cat"]}</div><div style="font-size:13px;color:#374151;margin-top:3px">{flag["desc"]}</div><div style="font-size:12px;color:#6b7280;margin-top:3px">{flag["detail"]}</div></div>'
    if not rf_items:
        rf_items = '<div class="sig-card sig-green">No significant quantitative red flags detected. Always check promoter pledging, auditor notes, and related-party transactions in annual reports.</div>'
    rf_icon = '&#9940;' if rf.get('high') else ('&#128308;' if rf.get('medium') else '&#9989;')
    rf_html = f'''<div style="padding:14px;border-radius:10px;background:#f9fafb;margin-bottom:14px;display:flex;align-items:center;gap:12px">
      <div style="font-size:28px">{rf_icon}</div>
      <div><div style="font-size:16px;font-weight:700;color:{rf.get("color","#6b7280")}">{rf.get("overall","N/A")}</div>
      <div style="font-size:12px;color:#6b7280">{rf.get("count",0)} flag(s): {len(rf.get("high",[]))} high &nbsp; {len(rf.get("medium",[]))} medium &nbsp; {len(rf.get("low",[]))} low severity</div></div>
    </div>
    {rf_items}
    <div class="sig-card sig-neutral" style="font-size:12px;margin-top:10px">Quantitative flags only. Always verify: promoter pledging %, auditor qualifications, contingent liabilities, and related-party transactions in annual reports.</div>'''

    verd=n['verdict']
    comb=n['combined']   # 6-engine combined verdict
    bv_color,buy_label,buy_desc=buy

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{cn} — Investor Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f4f5f7;color:#1a1a2e;font-size:15px;line-height:1.6}}
a{{color:#3b82f6;text-decoration:none}}
.hdr{{background:linear-gradient(135deg,#1a1a2e 0%,#16213e 60%,#0f3460 100%);color:#fff;padding:2rem 2.5rem}}
.hdr h1{{font-size:2rem;font-weight:700}}.hdr .sub{{opacity:.7;font-size:.9rem;margin-top:4px}}
.hdr-meta{{display:flex;gap:1rem;margin-top:1.2rem;flex-wrap:wrap}}
.mi{{background:rgba(255,255,255,.1);border-radius:8px;padding:10px 18px}}
.mi .ml{{font-size:11px;opacity:.65;text-transform:uppercase;letter-spacing:.05em}}
.mi .mv{{font-size:1.4rem;font-weight:600;margin-top:2px}}
.wrap{{max-width:1200px;margin:0 auto;padding:2rem 1.5rem}}
.stitle{{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#6b7280;margin:2.5rem 0 1rem;display:flex;align-items:center;gap:8px}}
.stitle::after{{content:'';flex:1;height:1px;background:#e5e7eb}}
.xbar{{background:#eff6ff;border-left:4px solid #3b82f6;border-radius:0 8px 8px 0;padding:10px 16px;font-size:13px;color:#1d4ed8;margin-bottom:1.5rem}}
.mg{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}}
.mc{{background:#fff;border-radius:12px;padding:18px 16px;box-shadow:0 1px 3px rgba(0,0,0,.06);border:1px solid #f1f5f9}}
.mc .ml{{font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:.05em;font-weight:600}}
.mc .mv{{font-size:1.8rem;font-weight:700;margin:6px 0 2px;color:#111827}}
.mc .ms{{font-size:12px;color:#6b7280}}
.mc .mv.good{{color:#059669}}.mc .mv.warn{{color:#d97706}}.mc .mv.bad{{color:#dc2626}}
.cg{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
@media(max-width:700px){{.cg{{grid-template-columns:1fr}}}}
.cc{{background:#fff;border-radius:12px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.06);border:1px solid #f1f5f9}}
.cc.full{{grid-column:1/-1}}
.ct{{font-size:14px;font-weight:600;color:#374151;margin-bottom:4px}}
.ce{{font-size:12px;color:#6b7280;margin-bottom:14px;line-height:1.5}}
.cw{{position:relative;width:100%}}
.gt{{width:100%;border-collapse:collapse;font-size:14px}}
.gt th{{text-align:left;padding:10px 12px;background:#f9fafb;color:#6b7280;font-size:11px;text-transform:uppercase;letter-spacing:.05em;border-bottom:1px solid #e5e7eb}}
.gt td{{padding:10px 12px;border-bottom:1px solid #f3f4f6}}
.gt td.good{{color:#059669;font-weight:600}}.gt td.warn{{color:#d97706;font-weight:600}}.gt td.bad{{color:#dc2626;font-weight:600}}
.qt{{width:100%;border-collapse:collapse;font-size:13px}}
.qt tr:hover td{{background:#f9fafb}}
.qt td{{padding:9px 12px;border-bottom:1px solid #f3f4f6}}
.qt td.qlbl{{color:#4b5563;font-size:13px;cursor:default}}
.qt td.qval{{font-weight:700;text-align:right}}
.qt td.qval.good{{color:#059669}}.qt td.qval.warn{{color:#d97706}}.qt td.qval.bad{{color:#dc2626}}
.sig-card{{border-radius:8px;padding:12px 14px;margin-bottom:8px;font-size:13px;line-height:1.6;border-left:4px solid transparent}}
.sig-green{{background:#f0fdf4;border-color:#22c55e;color:#166534}}
.sig-red{{background:#fef2f2;border-color:#ef4444;color:#991b1b}}
.sig-amber{{background:#fffbeb;border-color:#f59e0b;color:#78350f}}
.sig-neutral{{background:#f8fafc;border-color:#cbd5e1;color:#475569}}
.verdict-box{{border-radius:14px;padding:24px;text-align:center;border:2px solid;margin-bottom:1.5rem}}
.deep-card{{background:#fff;border-radius:12px;margin-bottom:10px;box-shadow:0 1px 3px rgba(0,0,0,.07);border:1px solid #e5e7eb;overflow:hidden}}
.deep-hdr{{display:flex;align-items:center;gap:14px;padding:18px 20px;cursor:pointer;background:#f9fafb;transition:background .15s}}
.deep-hdr:hover{{background:#f1f5f9}}
.deep-em{{font-size:22px;flex-shrink:0}}
.deep-q{{font-size:14px;font-weight:600;color:#1e293b;flex:1;line-height:1.4}}
.deep-chev{{font-size:18px;color:#94a3b8;flex-shrink:0}}
.deep-body{{padding:20px 24px;border-top:1px solid #f1f5f9}}
.deep-intro{{background:linear-gradient(135deg,#1e293b,#0f3460);color:#fff;border-radius:14px;padding:24px 28px;margin-bottom:1.5rem}}
.deep-intro h2{{font-size:1.3rem;font-weight:700;margin-bottom:8px}}
.deep-intro p{{font-size:13px;opacity:.8;line-height:1.6}}
.badge{{border-radius:20px;font-size:10px;font-weight:700;padding:2px 8px;text-transform:uppercase;letter-spacing:.05em}}
.badge-green{{background:#d1fae5;color:#065f46}}.badge-amber{{background:#fef3c7;color:#92400e}}.badge-red{{background:#fee2e2;color:#991b1b}}
.leg{{display:flex;gap:16px;flex-wrap:wrap;margin-top:10px;font-size:12px;color:#6b7280}}
.leg span{{display:flex;align-items:center;gap:5px}}
.ld{{width:10px;height:10px;border-radius:2px;display:inline-block}}
.disc{{background:#fffbeb;border:1px solid #fde68a;border-radius:10px;padding:14px 20px;font-size:12px;color:#92400e;margin-top:2rem;line-height:1.6}}
.foot{{text-align:center;padding:2rem;color:#9ca3af;font-size:12px}}
.score-bar{{height:10px;background:#e5e7eb;border-radius:5px;overflow:hidden;margin:8px 0}}
.score-fill{{height:100%;border-radius:5px;transition:width .5s}}
</style>
</head>
<body>

<div class="hdr">
  <h1>₹ {cn}</h1>
  <div class="sub">Long-Term Investor Dashboard · Dr Vijay Malik Framework · Screener.in Data{'  ·  '+sector if sector else ''}{'  /  '+industry if industry else ''}</div>
  <div class="hdr-meta">
    <div class="mi"><div class="ml">Price</div><div class="mv">₹{fmt(d['current_price'],1)}</div></div>
    <div class="mi"><div class="ml">Market Cap</div><div class="mv">{cr(d['market_cap'])}</div></div>
    <div class="mi"><div class="ml">P/E (TTM)</div><div class="mv">{pe_v}</div></div>
    <div class="mi"><div class="ml">Hist Avg P/E</div><div class="mv">{avgpe_v}</div></div>
    <div class="mi"><div class="ml">TTM Net Profit</div><div class="mv">{cr(d['ttm_pat'])}</div></div>
    <div class="mi"><div class="ml">SSGR</div><div class="mv">{fmt(ssgr_latest)}%</div></div>
    <div class="mi" style="border-left:3px solid rgba(255,255,255,0.4)">
      <div class="ml">Moat Score</div>
      <div class="mv" style="font-size:1.1rem;color:{'#6ee7b7' if n['moat_score']['pct']>=75 else '#fde68a' if n['moat_score']['pct']>=55 else '#fca5a5'}">{n['moat_score']['pct']}% — {n['moat_score']['label']}</div>
    </div>
    <div class="mi">
      <div class="ml">Mgmt Score</div>
      <div class="mv" style="font-size:1.1rem;color:{'#6ee7b7' if n['mgmt_score']['pct']>=75 else '#fde68a' if n['mgmt_score']['pct']>=62 else '#fca5a5'}">{n['mgmt_score']['pct']}% — {n['mgmt_score']['label']}</div>
    </div>
    <div class="mi">
      <div class="ml">DCF Base IV</div>
      <div class="mv" style="font-size:1.1rem;color:{'#6ee7b7' if (n['dcf'].get('base_iv') or 0) > d['current_price'] else '#fca5a5'}">{'₹'+fmt(n['dcf'].get('base_iv') or 0,0) if n['dcf'].get('base_iv') else 'N/A'}</div>
    </div>
    <div class="mi">
      <div class="ml">Red Flags</div>
      <div class="mv" style="font-size:1.1rem;color:{'#fca5a5' if n['red_flags']['high'] else '#fde68a' if n['red_flags']['medium'] else '#6ee7b7'}">{n['red_flags']['count']} flag{'s' if n['red_flags']['count']!=1 else ''} {'⛔' if n['red_flags']['high'] else '🟡' if n['red_flags']['medium'] else '✅'}</div>
    </div>
  </div>
</div>

<div class="wrap">

<div class="xbar">
  <strong>How to read this dashboard:</strong> Every metric is explained in plain English. Hover any scorecard row for a tooltip.
  The <strong>dot-joining narrative</strong> connects metrics into a coherent story. Scroll down for the 11 deep investor questions.
</div>

<!-- UNIFIED INVESTMENT SCORECARD -->
<div class="stitle">Unified Investment Scorecard</div>
<div style="background:#fff;border-radius:14px;border:1px solid #e5e7eb;padding:24px;box-shadow:0 1px 3px rgba(0,0,0,.07);margin-bottom:1rem">

  <!-- Top verdict row -->
  <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;padding-bottom:18px;border-bottom:1px solid #f3f4f6;margin-bottom:18px">
    <div style="flex:1;min-width:280px">
      <div style="font-size:2rem;font-weight:900;color:{n['combined']['color']}">{n['combined']['emoji']} {n['combined']['verdict']}</div>
      <div style="font-size:13px;color:#374151;font-weight:600;margin-top:6px">{n['combined']['action']}</div>
      <div style="font-size:12px;color:#6b7280;margin-top:4px">Based on moat · management · DCF · cyclicality · red flags · sector — {verd['green']} signals vs {verd['red']} concerns</div>
    </div>
    <div style="text-align:right">
      <div style="font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:.05em">Composite Score</div>
      <div style="font-size:2.5rem;font-weight:900;color:{n['combined']['color']}">{n['combined']['composite']}%</div>
      <div style="background:#e5e7eb;border-radius:6px;height:8px;width:140px;margin-top:4px;margin-left:auto">
        <div style="background:{n['combined']['color']};height:8px;border-radius:6px;width:{n['combined']['composite']}%"></div>
      </div>
    </div>
  </div>

  <!-- 6 engine scores grid -->
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px">

    <!-- Moat -->
    <div style="background:#f9fafb;border-radius:10px;padding:14px">
      <div style="font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px">🏰 Moat Score</div>
      <div style="font-size:1.4rem;font-weight:800;color:{n['moat_score']['color']}">{n['moat_score']['pct']}%</div>
      <div style="font-size:12px;font-weight:600;color:{n['moat_score']['color']};margin-top:2px">{n['moat_score']['label']}</div>
      <div style="background:#e5e7eb;border-radius:4px;height:5px;margin-top:8px">
        <div style="background:{n['moat_score']['color']};height:5px;border-radius:4px;width:{n['moat_score']['pct']}%"></div>
      </div>
      <div style="font-size:11px;color:#9ca3af;margin-top:6px">Margin stability · ROCE · growth</div>
    </div>

    <!-- Management -->
    <div style="background:#f9fafb;border-radius:10px;padding:14px">
      <div style="font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px">👔 Management Score</div>
      <div style="font-size:1.4rem;font-weight:800;color:{n['mgmt_score']['color']}">{n['mgmt_score']['pct']}%</div>
      <div style="font-size:12px;font-weight:600;color:{n['mgmt_score']['color']};margin-top:2px">{n['mgmt_score']['label']}</div>
      <div style="background:#e5e7eb;border-radius:4px;height:5px;margin-top:8px">
        <div style="background:{n['mgmt_score']['color']};height:5px;border-radius:4px;width:{n['mgmt_score']['pct']}%"></div>
      </div>
      <div style="font-size:11px;color:#9ca3af;margin-top:6px">VPR · earnings quality · dilution</div>
    </div>

    <!-- DCF -->
    <div style="background:#f9fafb;border-radius:10px;padding:14px">
      <div style="font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px">💰 DCF Intrinsic Value</div>
      <div style="font-size:1.4rem;font-weight:800;color:{'#059669' if (n['dcf'].get('base_iv') or 0) > d['current_price'] else '#dc2626'}">
        {'₹'+str(int(n['dcf']['base_iv'])) if n['dcf'].get('base_iv') else 'N/A'}
      </div>
      <div style="font-size:12px;color:#6b7280;margin-top:2px">Base case (current ₹{fmt(d['current_price'],0)})</div>
      <div style="font-size:12px;font-weight:600;margin-top:6px;color:{'#059669' if (n['dcf'].get('base_iv') or 0) > d['current_price'] else '#dc2626'}">
        {'Undervalued' if (n['dcf'].get('base_iv') or 0) > d['current_price'] else 'Overvalued'} vs DCF
      </div>
      <div style="font-size:11px;color:#9ca3af;margin-top:4px">MoS buy zone: {'₹'+str(int(n['dcf']['mos_buy'])) if n['dcf'].get('mos_buy') else 'N/A'}</div>
    </div>

    <!-- Cyclicality -->
    <div style="background:#f9fafb;border-radius:10px;padding:14px">
      <div style="font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px">🌊 Cyclicality</div>
      <div style="font-size:1.4rem;font-weight:800;color:{n['cyclicality']['color']}">{n['cyclicality']['score']}/10</div>
      <div style="font-size:12px;font-weight:600;color:{n['cyclicality']['color']};margin-top:2px">{n['cyclicality']['label']}</div>
      <div style="background:#e5e7eb;border-radius:4px;height:5px;margin-top:8px">
        <div style="background:{n['cyclicality']['color']};height:5px;border-radius:4px;width:{n['cyclicality']['score']*10}%"></div>
      </div>
      <div style="font-size:11px;color:#9ca3af;margin-top:6px">Mid-cycle PAT: {'₹'+fmt(n['cyclicality'].get('mid_cycle_pat') or 0,0)+' Cr' if n['cyclicality'].get('mid_cycle_pat') else 'N/A'}</div>
    </div>

    <!-- Sector -->
    <div style="background:#f9fafb;border-radius:10px;padding:14px">
      <div style="font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px">📊 Sector Position</div>
      {sect_tile_html}
    </div>

    <!-- Red Flags -->
    <div style="background:#f9fafb;border-radius:10px;padding:14px">
      <div style="font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px">🚩 Red Flags</div>
      <div style="font-size:1.4rem;font-weight:800;color:{n['red_flags']['color']}">{n['red_flags']['count']}</div>
      <div style="font-size:12px;font-weight:600;color:{n['red_flags']['color']};margin-top:2px">{n['red_flags']['overall'].split('—')[1].strip() if '—' in n['red_flags']['overall'] else n['red_flags']['overall']}</div>
      <div style="font-size:11px;color:#9ca3af;margin-top:8px">{len(n['red_flags']['high'])} high · {len(n['red_flags']['medium'])} medium · {len(n['red_flags']['low'])} low severity</div>
    </div>

  </div>

  <!-- Buy/Avoid reasons -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:18px">
    <div style="background:#f0fdf4;border-radius:10px;padding:14px">
      <div style="font-size:11px;font-weight:700;color:#059669;text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px">✅ Reasons to Consider</div>
      {''.join('<div style="font-size:12px;color:#374151;padding:3px 0;border-bottom:1px solid #dcfce7">· '+r+'</div>' for r in n['combined']['reasons_buy']) or '<div style="font-size:12px;color:#9ca3af">None identified</div>'}
    </div>
    <div style="background:#fef2f2;border-radius:10px;padding:14px">
      <div style="font-size:11px;font-weight:700;color:#dc2626;text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px">⚠ Reasons for Caution</div>
      {''.join('<div style="font-size:12px;color:#374151;padding:3px 0;border-bottom:1px solid #fee2e2">· '+r+'</div>' for r in n['combined']['reasons_avoid']) or '<div style="font-size:12px;color:#9ca3af">None identified</div>'}
    </div>
  </div>

  <!-- Score breakdown bar -->
  <div style="margin-top:14px;padding:12px;background:#f9fafb;border-radius:8px">
    <div style="font-size:11px;color:#9ca3af;margin-bottom:8px;text-transform:uppercase;letter-spacing:.05em">Score Breakdown (weighted)</div>
    <div style="display:flex;gap:4px;height:14px;border-radius:6px;overflow:hidden">
      {''.join('<div title="'+k+': '+str(round(v,1))+' pts" style="flex:'+str(round(v/n['combined']['max_pts']*100))+';background:'+{'moat':'#6366f1','mgmt':'#10b981','dcf':'#3b82f6','pe_hist':'#8b5cf6','rf':'#f59e0b','cyclicality':'#f97316','sector':'#06b6d4'}.get(k,'#94a3b8')+'"></div>' for k,v in n['combined']['scores'].items())}
    </div>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:6px">
      {''.join('<span style="font-size:11px;color:#6b7280"><span style="display:inline-block;width:8px;height:8px;border-radius:2px;background:'+{'moat':'#6366f1','mgmt':'#10b981','dcf':'#3b82f6','pe_hist':'#8b5cf6','rf':'#f59e0b','cyclicality':'#f97316','sector':'#06b6d4'}.get(k,'#94a3b8')+';margin-right:3px"></span>'+k.replace('_',' ').title()+'</span>' for k in n['combined']['scores'])}
    </div>
  </div>
</div>

<!-- COMPANY OVERVIEW -->
<div class="stitle">What Does This Company Do?</div>
<div class="cc full">
  <div class="ct">{cn} — Business Overview</div>
  <p style="font-size:13px;color:#4b5563;line-height:1.8;margin-bottom:10px">{about}</p>
  {kp_html}
  {'<p style="font-size:12px;color:#9ca3af;margin-top:10px"><strong>Sector:</strong> '+sector+' &nbsp;·&nbsp; <strong>Industry:</strong> '+industry+'</p>' if sector else ''}
  <p style="font-size:12px;color:#9ca3af;margin-top:4px"><strong>Peers:</strong> {peers} &nbsp;·&nbsp; <a href="{url}" target="_blank">View on Screener.in ↗</a></p>
  {pros_cons}
</div>

<!-- AT A GLANCE -->
<div class="stitle">At a Glance</div>
<div class="mg">
  <div class="mc"><div class="ml">PAT CAGR (5Y)</div>
    <div class="mv {'good' if g5 and g5>0.15 else 'warn' if g5 and g5>0.05 else 'bad'}">{pct(g5)}</div>
    <div class="ms">profit/yr last 5 yrs</div></div>
  <div class="mc"><div class="ml">ROE (Latest)</div>
    <div class="mv {'good' if roe_latest and roe_latest>20 else 'warn' if roe_latest and roe_latest>10 else 'bad'}">{fmt(roe_latest)}%</div>
    <div class="ms">₹ earned per ₹100 equity</div></div>
  <div class="mc"><div class="ml">P/E vs Avg</div>
    <div class="mv {'good' if val['vs_hist'] and val['vs_hist']<-5 else 'warn' if not val['vs_hist'] or val['vs_hist']<15 else 'bad'}">{pe_v}</div>
    <div class="ms">avg {avgpe_v}</div></div>
  <div class="mc"><div class="ml">SSGR</div>
    <div class="mv {'good' if ssgr_latest and ssgr_latest>15 else 'warn' if ssgr_latest and ssgr_latest>8 else 'bad'}">{fmt(ssgr_latest)}%</div>
    <div class="ms">self-fund growth rate</div></div>
  <div class="mc"><div class="ml">D/E Ratio</div>
    <div class="mv {'good' if de_latest is not None and de_latest<0.5 else 'warn' if de_latest and de_latest<1 else 'bad'}">{fmt(de_latest)}x</div>
    <div class="ms">lower = safer</div></div>
  <div class="mc"><div class="ml">FCF/CFO (10Y)</div>
    <div class="mv {'good' if d['fcf_cfo'] and d['fcf_cfo']>25 else 'warn' if d['fcf_cfo'] and d['fcf_cfo']>0 else 'bad'}">{fmt(d['fcf_cfo'])}%</div>
    <div class="ms">free cash generated</div></div>
  <div class="mc"><div class="ml">Value / ₹1 Retained</div>
    <div class="mv {'good' if d['vpr'] and d['vpr']>2 else 'warn' if d['vpr'] and d['vpr']>1 else 'bad'}">₹{fmt(d['vpr'])}</div>
    <div class="ms">capital allocation quality</div></div>
  <div class="mc"><div class="ml">Int. Coverage (Dr VM)</div>
    <div class="mv {'good' if ic_latest and ic_latest>4 else 'warn' if ic_latest and ic_latest>2 else 'bad'}">{fmt(ic_latest)}x</div>
    <div class="ms">at 12% cost of debt</div></div>
</div>

<!-- GROWTH SUMMARY -->
<div class="stitle">Growth Rate Summary</div>
<div class="cc full">
  <div class="ce">CAGR = average annual growth, like compound interest. 15% CAGR = ₹1 lakh grew to ₹4 lakhs in 10 years.</div>
  <table class="gt">
    <thead><tr><th>Metric</th><th>10-Year CAGR</th><th>5-Year CAGR</th><th>3-Year CAGR</th><th>Last Year (YoY)</th></tr></thead>
    <tbody>
      {crow("Revenue (Sales)", d['sales_cagr'])}
      {crow("Net Profit (PAT)", d['pat_cagr'])}
      {crow("EPS (per share)", d['eps_cagr'])}
      {crow("Book Value / share", d['bv_cagr'])}
      {crow("Dividends", d['div_cagr'], good=0.08, warn=0.0)}
    </tbody>
  </table>
</div>

<!-- CHARTS -->
<div class="stitle">10-Year Financial History</div>
<div class="cc full">
  <div class="ct">Revenue vs Net Profit (₹ Cr)</div>
  <div class="ce">Sales = total earnings. Profit = what's left after all costs. Rising profit with growing sales = improving efficiency.</div>
  <div class="cw" style="height:260px"><canvas id="c1"></canvas></div>
  <div class="leg"><span><span class="ld" style="background:#3b82f6"></span>Sales</span><span><span class="ld" style="background:#10b981"></span>Net Profit</span></div>
</div>
<div class="cg" style="margin-top:16px">
  <div class="cc">
    <div class="ct">Operating & Net Margins (%)</div>
    <div class="ce">How much of every ₹100 revenue becomes operating/net profit. Rising = getting more efficient.</div>
    <div class="cw" style="height:180px"><canvas id="c2"></canvas></div>
  </div>
  <div class="cc">
    <div class="ct">ROE & ROCE (%)</div>
    <div class="ce">ROE = return on shareholder money. ROCE = return on all capital (debt + equity). Both above 20% = excellent.</div>
    <div class="cw" style="height:180px"><canvas id="c3"></canvas></div>
  </div>
</div>
<div class="cg" style="margin-top:16px">
  <div class="cc">
    <div class="ct">Historical P/E Band</div>
    <div class="ce">Red line = today's PE. Orange = 10-year avg. Bars below red line = historically cheaper than now.</div>
    <div class="cw" style="height:200px"><canvas id="c4"></canvas></div>
    <div class="leg">
      <span><span class="ld" style="background:#6366f1"></span>Historical PE</span>
      <span><span class="ld" style="background:#ef4444"></span>Current {pe_v}</span>
      <span><span class="ld" style="background:#f59e0b"></span>10Y Avg {avgpe_v}</span>
    </div>
  </div>
  <div class="cc">
    <div class="ct">SSGR vs Sales CAGR</div>
    <div class="ce">SSGR = max growth without new debt. If sales growth (orange) exceeds SSGR (blue), debt must fund the gap. Watch for divergence.</div>
    <div class="cw" style="height:200px"><canvas id="c_ssgr"></canvas></div>
    <div class="leg">
      <span><span class="ld" style="background:#6366f1"></span>SSGR %</span>
      <span><span class="ld" style="background:#f59e0b"></span>Actual Sales Growth % (YoY)</span>
    </div>
  </div>
</div>
<div class="cg" style="margin-top:16px">
  <div class="cc">
    <div class="ct">Debt vs Cash from Operations</div>
    <div class="ce">Falling debt + rising CFO = healthy deleveraging. Rising debt + weak CFO = balance sheet stress.</div>
    <div class="cw" style="height:180px"><canvas id="c5"></canvas></div>
  </div>
  <div class="cc">
    <div class="ct">Free Cash Flow (₹ Cr)</div>
    <div class="ce">FCF = cash remaining after capex. Positive = business funds itself. Negative = needs external money.</div>
    <div class="cw" style="height:180px"><canvas id="c_fcf"></canvas></div>
  </div>
</div>
<div class="cc full">
  <div class="ct">Working Capital Cycle (Days)</div>
  <div class="ce">Lower = better. Receivable days + Inventory days. Rising = cash getting trapped longer in the business.</div>
  <div class="cw" style="height:180px"><canvas id="c7"></canvas></div>
</div>

<!-- QUARTERLY RESULTS DASHBOARD -->
<div class="stitle" style="margin-top:2rem">Quarterly Results — Deep Dive</div>
<div class="deep-intro" style="padding:16px 20px;margin-bottom:1rem">
  <h2 style="font-size:1rem;margin-bottom:4px">📅 Last 10 Quarters — All metrics from Dr Vijay Malik's Excel</h2>
  <p>Always compare the same quarter year-over-year (Q2 FY26 vs Q2 FY25), not sequential quarters.
  Seasonal patterns make sequential comparisons misleading for most businesses.</p>
</div>

<div class="cc full">
  <div class="ct">Quarterly Revenue vs Operating Profit vs Net Profit (₹ Cr)</div>
  <div class="ce">Revenue bars with Operating Profit and Net Profit as lines.
  Watch for margin compression: when profit lines fall faster than revenue bars, costs are rising or pricing power is weakening.</div>
  <div class="cw" style="height:260px"><canvas id="cq1"></canvas></div>
  <div class="leg">
    <span><span class="ld" style="background:#6366f1"></span>Revenue</span>
    <span><span class="ld" style="background:#f59e0b"></span>Operating Profit</span>
    <span><span class="ld" style="background:#10b981"></span>Net Profit</span>
  </div>
</div>

<div class="cg" style="margin-top:16px">
  <div class="cc">
    <div class="ct">Quarterly Margins (%)</div>
    <div class="ce">Operating Margin = Op Profit / Sales. Net Margin = PAT / Sales.
    Stable or widening margins = pricing power. Narrowing = cost pressure.</div>
    <div class="cw" style="height:200px"><canvas id="cq2"></canvas></div>
    <div class="leg">
      <span><span class="ld" style="background:#6366f1"></span>OPM %</span>
      <span><span class="ld" style="background:#10b981"></span>NPM %</span>
    </div>
  </div>
  <div class="cc">
    <div class="ct">Quarter-on-Quarter YoY Growth (%) — Same Quarter Last Year</div>
    <div class="ce">Green bars = growing vs same quarter last year. Red bars = declining.
    This removes seasonal distortion. 4 quarters shown (YoY pairs only).</div>
    <div class="cw" style="height:200px"><canvas id="cq3"></canvas></div>
    <div class="leg">
      <span><span class="ld" style="background:#6366f1"></span>Sales YoY %</span>
      <span><span class="ld" style="background:#10b981"></span>PAT YoY %</span>
    </div>
  </div>
</div>

<div class="cg" style="margin-top:16px">
  <div class="cc">
    <div class="ct">Quarterly Interest & Depreciation (₹ Cr)</div>
    <div class="ce">Rising interest = debt is growing or rates are rising.
    Rising depreciation = new assets being added (capex bearing fruit). Both eat into profit.</div>
    <div class="cw" style="height:180px"><canvas id="cq4"></canvas></div>
    <div class="leg">
      <span><span class="ld" style="background:#ef4444"></span>Interest</span>
      <span><span class="ld" style="background:#f59e0b"></span>Depreciation</span>
    </div>
  </div>
  <div class="cc">
    <div class="ct">Quarterly PBT vs Tax vs PAT (₹ Cr)</div>
    <div class="ce">PBT = profit before tax. The gap between PBT and PAT is tax.
    Erratic tax rate (gap changing significantly) = one-off deferred tax items — do not read as operating performance.</div>
    <div class="cw" style="height:180px"><canvas id="cq5"></canvas></div>
    <div class="leg">
      <span><span class="ld" style="background:#8b5cf6"></span>PBT</span>
      <span><span class="ld" style="background:#ef4444"></span>Tax</span>
      <span><span class="ld" style="background:#10b981"></span>PAT</span>
    </div>
  </div>
</div>

<!-- COST STRUCTURE -->
<div class="stitle">Cost Structure (Latest Year % of Sales)</div>
<div class="cc full">
  <div class="ce">Understanding where money goes. For a manufacturer, raw material is typically 60–70%. Rising employee/selling costs relative to revenue = margin pressure ahead.</div>
  <table style="width:100%;max-width:500px">{cost_rows}</table>
  <p style="font-size:12px;color:#9ca3af;margin-top:10px">Operating Margin = 100% minus all cost percentages above = <strong>{fmt(opm_latest)}%</strong></p>
</div>

<!-- EXTENDED CHARTS — new metrics -->
<div class="stitle">Extended Analysis Charts</div>
<div class="cg">
  <div class="cc">
    <div class="ct">EBITDA Margin vs Operating Margin (%)</div>
    <div class="ce">EBITDA Margin includes other income. Gap between lines = other income contribution. Both should be stable or rising.</div>
    <div class="cw" style="height:180px"><canvas id="c_ebitda"></canvas></div>
  </div>
  <div class="cc">
    <div class="ct">Tax Rate % (Tax / PBT)</div>
    <div class="ce">A stable tax rate means reported PAT is reliable. Spikes or dips indicate deferred tax adjustments or one-time items distorting profits.</div>
    <div class="cw" style="height:180px"><canvas id="c_tax"></canvas></div>
  </div>
</div>
<div class="cg" style="margin-top:16px">
  <div class="cc">
    <div class="ct">Net Cash Generation per Year (₹ Cr)</div>
    <div class="ce">FCF + Other Income + ΔDebt − Interest − Dividends. Green = surplus year (self-funding). Red = deficit year (needs external capital).</div>
    <div class="cw" style="height:180px"><canvas id="c_ncg"></canvas></div>
  </div>
  <div class="cc">
    <div class="ct">Cumulative Surplus Funds (₹ Cr)</div>
    <div class="ce">Running total of net cash generation. Rising line = company is a net cash producer over time. Falling = structural cash drain.</div>
    <div class="cw" style="height:180px"><canvas id="c_surplus"></canvas></div>
  </div>
</div>
<div class="cg" style="margin-top:16px">
  <div class="cc">
    <div class="ct">Adjusted Shares Outstanding (Crores)</div>
    <div class="ce">Split/bonus adjusted share count. Rising = dilution (your ownership % shrinks). Flat = management respects existing shareholders.</div>
    <div class="cw" style="height:180px"><canvas id="c_shares"></canvas></div>
  </div>
  <div class="cc">
    <div class="ct">Reinvestment Rate (Capex / Dep+FCF)</div>
    <div class="ce">&gt;1 = investing aggressively for growth. &lt;1 = harvesting. &gt;2 = heavy expansion mode (future capacity being built).</div>
    <div class="cw" style="height:180px"><canvas id="c_ri"></canvas></div>
  </div>
</div>
<div class="cg" style="margin-top:16px">
  <div class="cc">
    <div class="ct">Depreciation % of NFA</div>
    <div class="ce">Rising = asset base ageing faster than renewal (new capex needed soon). Falling = fresh long-life assets added recently.</div>
    <div class="cw" style="height:180px"><canvas id="c_depnfa"></canvas></div>
  </div>
  <div class="cc">
    <div class="ct">NFA + CWIP — Capacity Pipeline (₹ Cr)</div>
    <div class="ce">Net Fixed Assets + Capital Work in Progress. A rising CWIP bulge = projects under construction = future revenue capacity.</div>
    <div class="cw" style="height:180px"><canvas id="c_nfacwip"></canvas></div>
  </div>
</div>
<div class="cg" style="margin-top:16px">
  <div class="cc">
    <div class="ct">Raw Material & Employee Cost % of Sales (Trend)</div>
    <div class="ce">Declining RM% = pricing power or input cost efficiency. Rising Emp% over time = wage inflation eating margins.</div>
    <div class="cw" style="height:180px"><canvas id="c_costs"></canvas></div>
  </div>
  <div class="cc">
    <div class="ct">Market Capitalisation History (₹ Cr)</div>
    <div class="ce">How the market valued the company each year. Compare slope with PAT CAGR — parallel lines = rational market. MCap growing faster = re-rating.</div>
    <div class="cw" style="height:180px"><canvas id="c_mcap"></canvas></div>
  </div>
</div>

<!-- DR VM SCORECARD -->
<div class="stitle">Full Scorecard — Dr Vijay Malik Framework (hover any row for explanation)</div>
<div class="cc full"><table class="qt">{sc}</table></div>

<!-- DOT-JOINING NARRATIVE -->
<div class="stitle" style="margin-top:3rem">The Story the Numbers Are Telling — Joining the Dots</div>
<div class="deep-intro">
  <h2>📖 What does ALL this data mean together?</h2>
  <p>Individual metrics are just numbers. The real insight comes from reading them as a system.
  Below, we connect each set of metrics into a coherent narrative about this business's quality,
  financial health, operational efficiency, and investment merit.</p>
</div>

<div class="deep-card" id="dc_q">
  <div class="deep-hdr" onclick="tog('q')"><span class="deep-em">💎</span>
    <div class="deep-q">Business Quality — Is this a fundamentally good business?</div>
    <span class="deep-chev" id="ch_q">−</span></div>
  <div class="deep-body" id="db_q">
    {sig_block(n['business_quality']['signals'], n['business_quality']['warnings'])}
  </div>
</div>

<div class="deep-card" id="dc_h">
  <div class="deep-hdr" onclick="tog('h')"><span class="deep-em">🏦</span>
    <div class="deep-q">Financial Health — Is the balance sheet safe?</div>
    <span class="deep-chev" id="ch_h">+</span></div>
  <div class="deep-body" id="db_h" style="display:none">
    {sig_block(n['financial_health']['signals'], n['financial_health']['warnings'])}
  </div>
</div>

<div class="deep-card" id="dc_o">
  <div class="deep-hdr" onclick="tog('o')"><span class="deep-em">⚙️</span>
    <div class="deep-q">Operational Efficiency — Is management running this well?</div>
    <span class="deep-chev" id="ch_o">+</span></div>
  <div class="deep-body" id="db_o" style="display:none">
    {sig_block(n['operational']['signals'], n['operational']['warnings'])}
  </div>
</div>

<div class="deep-card" id="dc_ssgr">
  <div class="deep-hdr" onclick="tog('ssgr')"><span class="deep-em">🌱</span>
    <div class="deep-q">Growth Sustainability (SSGR) — Can it grow without drowning in debt?</div>
    <span class="deep-chev" id="ch_ssgr">+</span></div>
  <div class="deep-body" id="db_ssgr" style="display:none">
    <div class="sig-card sig-neutral" style="margin-bottom:12px">
      <strong>What is SSGR?</strong> Self-Sustainable Growth Rate = Net Profit Margin × NFA Turnover × (1 − Dividend Payout).
      It answers: "How fast can this company grow WITHOUT borrowing more money?" If actual growth > SSGR, it MUST borrow to fund the gap.
      Dr Vijay Malik considers this one of the most revealing metrics for long-term investors.
    </div>
    {sig_block(n['growth_sustainability']['signals'], n['growth_sustainability']['warnings'])}
  </div>
</div>

<div class="deep-card" id="dc_m">
  <div class="deep-hdr" onclick="tog('m')"><span class="deep-em">🏰</span>
    <div class="deep-q">Moat Analysis — What's the competitive advantage? Can competition kill it?</div>
    <span class="deep-chev" id="ch_m">+</span></div>
  <div class="deep-body" id="db_m" style="display:none">
    <div class="sig-card sig-neutral" style="margin-bottom:12px">
      A "moat" is what prevents competitors from taking away customers or compressing margins over time.
      Types include: cost advantage, switching costs, network effects, intangible assets (brand/patents), and efficient scale.
      In auto-components, moats tend to be narrow — relationships matter but are renegotiated regularly.
    </div>
    {moat_type_html}
    {sig_block(n['moat']['signals'], n['moat']['warnings'])}
  </div>
</div>

<!-- 8-DIMENSION METRIC INTERPRETER ENGINE CARDS -->
<div class="stitle" style="margin-top:3rem">8-Dimension Metric Interpreter — Joining the Dots</div>
<div class="deep-intro">
  <h2>📐 Complete Analysis of All ~80 Sheet-2 Metrics</h2>
  <p>Each dimension reads multiple metrics together and produces a verdict — not individual numbers in isolation.
  This is how a seasoned analyst reads a balance sheet: patterns, not data points.</p>
</div>

<div class="deep-card" id="dc_roce">
  <div class="deep-hdr" onclick="tog('roce')"><span class="deep-em">📈</span>
    <div class="deep-q">ROCE Trend — Is capital becoming more or less productive over time?</div>
    <span class="deep-chev" id="ch_roce">+</span></div>
  <div class="deep-body" id="db_roce" style="display:none">
    <div class="sig-card sig-neutral" style="margin-bottom:10px">
      <strong>ROCE = EBIT / Avg Capital Employed.</strong> Dr VM thresholds: &lt;10% = bad, &gt;35% = excellent.
      The <em>trend</em> matters as much as the absolute level — a rising ROCE on a growing capital base
      is the hallmark of a compounding machine.
    </div>
    {sig_block(n['roce_analysis']['signals'], n['roce_analysis']['warnings'])}
  </div>
</div>

<div class="deep-card" id="dc_at">
  <div class="deep-hdr" onclick="tog('at')"><span class="deep-em">🏭</span>
    <div class="deep-q">Asset Turnover — Is the company sweating its assets harder or getting lazy?</div>
    <span class="deep-chev" id="ch_at">+</span></div>
  <div class="deep-body" id="db_at" style="display:none">
    <div class="sig-card sig-neutral" style="margin-bottom:10px">
      <strong>NFA Turnover = Sales / Avg Net Fixed Assets.</strong> Higher = more revenue per rupee of plant.
      Depreciation % of NFA reveals asset age — rising % = ageing assets, falling % = fresh investment.
      CWIP signals future capacity.
    </div>
    {sig_block(n['asset_turnover_analysis']['signals'], n['asset_turnover_analysis']['warnings'])}
  </div>
</div>

<div class="deep-card" id="dc_wc">
  <div class="deep-hdr" onclick="tog('wc')"><span class="deep-em">💧</span>
    <div class="deep-q">Working Capital Cycle — How long is cash trapped in the business?</div>
    <span class="deep-chev" id="ch_wc">+</span></div>
  <div class="deep-body" id="db_wc" style="display:none">
    <div class="sig-card sig-neutral" style="margin-bottom:10px">
      <strong>WC Cycle = Receivable Days + Inventory Days.</strong>
      Every extra day of WC cycle ties up (Annual Sales ÷ 365) crores of capital.
      A business with a shrinking WC cycle is self-releasing cash — like a free credit line.
    </div>
    {sig_block(n['wc_analysis']['signals'], n['wc_analysis']['warnings'])}
  </div>
</div>

<div class="deep-card" id="dc_ri">
  <div class="deep-hdr" onclick="tog('ri')"><span class="deep-em">🔄</span>
    <div class="deep-q">Reinvestment Rate — Is the company investing for growth or just maintaining?</div>
    <span class="deep-chev" id="ch_ri">+</span></div>
  <div class="deep-body" id="db_ri" style="display:none">
    <div class="sig-card sig-neutral" style="margin-bottom:10px">
      <strong>Reinvestment Rate = Capex / (Depreciation + FCF).</strong>
      &gt;1 = investing beyond maintenance (growth mode).
      &lt;1 = harvesting the business (cash cow mode).
      FCF/CFO shows what fraction of operating cash escapes after capex.
    </div>
    {sig_block(n['reinvestment_analysis']['signals'], n['reinvestment_analysis']['warnings'])}
  </div>
</div>

<div class="deep-card" id="dc_dil">
  <div class="deep-hdr" onclick="tog('dil')"><span class="deep-em">🍕</span>
    <div class="deep-q">Shareholder Dilution — Is your slice of the pie shrinking?</div>
    <span class="deep-chev" id="ch_dil">+</span></div>
  <div class="deep-body" id="db_dil" style="display:none">
    <div class="sig-card sig-neutral" style="margin-bottom:10px">
      <strong>Share count change over 10 years.</strong>
      If shares outstanding grew 20%, every per-share metric (EPS, book value, dividend) is 20% smaller
      for the same total profit. Dilution is a silent tax on existing shareholders.
    </div>
    {sig_block(n['dilution_analysis']['signals'], n['dilution_analysis']['warnings'])}
  </div>
</div>

<div class="deep-card" id="dc_cyc">
  <div class="deep-hdr" onclick="tog('cyc')"><span class="deep-em">🌊</span>
    <div class="deep-q">Cyclicality — Will this business punish you during downturns?</div>
    <span class="deep-chev" id="ch_cyc">+</span></div>
  <div class="deep-body" id="db_cyc" style="display:none">
    <div class="sig-card sig-neutral" style="margin-bottom:10px">
      Cyclicality is read from: PAT decline years, EBITDA margin range, tax rate stability.
      A highly cyclical business should never be valued at peak earnings — always use normalised/mid-cycle figures.
    </div>
    {sig_block(n['cyclicality_analysis']['signals'], n['cyclicality_analysis']['warnings'])}
  </div>
</div>

<div class="deep-card" id="dc_ca">
  <div class="deep-hdr" onclick="tog('ca')"><span class="deep-em">♟️</span>
    <div class="deep-q">Capital Allocation — Is management making good decisions with your money?</div>
    <span class="deep-chev" id="ch_ca">+</span></div>
  <div class="deep-body" id="db_ca" style="display:none">
    <div class="sig-card sig-neutral" style="margin-bottom:10px">
      Capital allocation is read from: VPR (value per ₹1 retained), incremental ROE,
      dividend vs FCFE2 payout ratio, cumulative net cash generation, and total debt change.
      Together these reveal whether management earns its keep.
    </div>
    {sig_block(n['capital_allocation_analysis']['signals'], n['capital_allocation_analysis']['warnings'])}
  </div>
</div>

<div class="deep-card" id="dc_gs">
  <div class="deep-hdr" onclick="tog('gs')"><span class="deep-em">🌱</span>
    <div class="deep-q">Growth Sustainability — Can growth continue without balance sheet stress?</div>
    <span class="deep-chev" id="ch_gs">+</span></div>
  <div class="deep-body" id="db_gs" style="display:none">
    <div class="sig-card sig-neutral" style="margin-bottom:10px">
      <strong>SSGR</strong> (Self-Sustainable Growth Rate) = NPM × NFA Turnover × (1 − payout).
      If actual growth > SSGR, every percentage point above that rate is funded by debt or equity.
      Net Cash Generation confirms whether the business is a net cash producer or consumer over time.
    </div>
    {sig_block(n['growth_sustainability_ext']['signals'], n['growth_sustainability_ext']['warnings'])}
  </div>
</div>

<!-- ═══════════════ 6 ADVANCED ANALYTICAL ENGINES ═══════════════ -->
<div class="stitle" style="margin-top:3rem">Advanced Analytical Engines</div>
<div class="deep-intro">
  <h2>🔬 Institutional-Grade Analysis — Beyond Screener</h2>
  <p>Six quantitative engines running on 10 years of financial data. Each produces a score, verdict, and
  plain-English explanation — so you know not just <em>what</em> the number is, but <em>what it means</em> for your investment.</p>
</div>

<!-- 1. DCF INTRINSIC VALUE -->
<div class="deep-card" id="dc_dcf">
  <div class="deep-hdr" onclick="tog('dcf')"><span class="deep-em">💰</span>
    <div class="deep-q">Intrinsic Value (DCF) — What is this stock actually worth?</div>
    <span class="deep-chev" id="ch_dcf">−</span></div>
  <div class="deep-body" id="db_dcf">
    {dcf_html}
  </div>
</div>

<!-- 2. MOAT SCORE -->
<div class="deep-card" id="dc_moat">
  <div class="deep-hdr" onclick="tog('moat')"><span class="deep-em">🏰</span>
    <div class="deep-q">Moat Score — How defensible is this business against competition?</div>
    <span class="deep-chev" id="ch_moat">+</span></div>
  <div class="deep-body" id="db_moat" style="display:none">
    {moat_html}
  </div>
</div>

<!-- 3. MANAGEMENT QUALITY -->
<div class="deep-card" id="dc_mgmt2">
  <div class="deep-hdr" onclick="tog('mgmt2')"><span class="deep-em">👔</span>
    <div class="deep-q">Management Quality Score — Are they good stewards of your capital?</div>
    <span class="deep-chev" id="ch_mgmt2">+</span></div>
  <div class="deep-body" id="db_mgmt2" style="display:none">
    {mgmt_score_html}
  </div>
</div>

<!-- 4. CYCLICALITY -->
<div class="deep-card" id="dc_cyc2">
  <div class="deep-hdr" onclick="tog('cyc2')"><span class="deep-em">🌊</span>
    <div class="deep-q">Cyclicality Detection — Will this business punish you in a downturn?</div>
    <span class="deep-chev" id="ch_cyc2">+</span></div>
  <div class="deep-body" id="db_cyc2" style="display:none">
    {cyc_html}
  </div>
</div>

<!-- 5. SECTOR COMPARISON -->
<div class="deep-card" id="dc_sector">
  <div class="deep-hdr" onclick="tog('sector')"><span class="deep-em">📊</span>
    <div class="deep-q">Sector Comparison — Is this stock better or worse than its peers?</div>
    <span class="deep-chev" id="ch_sector">+</span></div>
  <div class="deep-body" id="db_sector" style="display:none">
    {sector_html}
  </div>
</div>

<!-- 6. RED FLAGS -->
<div class="deep-card" id="dc_rf">
  <div class="deep-hdr" onclick="tog('rf')"><span class="deep-em">🚩</span>
    <div class="deep-q">Red Flag Detection — What risks are hiding in the numbers?</div>
    <span class="deep-chev" id="ch_rf">+</span></div>
  <div class="deep-body" id="db_rf" style="display:none">
    {rf_html}
  </div>
</div>

<!-- DEEP INVESTOR QUESTIONS -->
<div class="stitle" style="margin-top:3rem">Deep Investor Questions</div>
<div class="deep-intro">
  <h2>The Questions Every Long-Term Investor Must Answer</h2>
  <p>Each answer is derived directly from the financial data — not generic advice.</p>
</div>

<div class="deep-card">
  <div class="deep-hdr" onclick="tog('val')"><span class="deep-em">🔭</span>
    <div class="deep-q">Is future growth already priced in? Will the stock stagnate while earnings catch up?</div>
    <span class="deep-chev" id="ch_val">+</span></div>
  <div class="deep-body" id="db_val" style="display:none">
    <div style="{'background:#d1fae5;color:#065f46;border-left:4px solid #059669' if (val['vs_hist'] or 0)<0 else 'background:#fef3c7;color:#78350f;border-left:4px solid #d97706'};padding:12px 16px;border-radius:8px;margin:0 0 12px;font-size:13px;font-weight:600">
      {'Growth not fully priced in — stock below historical PE' if (val['vs_hist'] or 0)<0 else 'Some growth is priced in'}
    </div>
    <ul style="padding-left:20px;margin:0">
      <li style="margin:8px 0;font-size:13px;color:#374151;line-height:1.6"><strong>P/E:</strong> {pe_v} vs 10Y avg {avgpe_v} (range {fmt(val['pe_min'])}x–{fmt(val['pe_max'])}x). Stock is trading {abs(val['vs_hist'] or 0):.0f}% {'below' if (val['vs_hist'] or 0)<0 else 'above'} its historical average.</li>
      <li style="margin:8px 0;font-size:13px;color:#374151;line-height:1.6"><strong>PEG:</strong> {peg_v} — {'below 1 = growth not fully priced in (good)' if val['peg'] and val['peg']<1 else 'between 1-2 = fairly priced' if val['peg'] and val['peg']<2 else 'above 2 = expensive relative to growth'}.</li>
      <li style="margin:8px 0;font-size:13px;color:#374151;line-height:1.6"><strong>P/E × P/B = {pepb_v}</strong> — Benjamin Graham's composite. {'Safe: below 22.5.' if val['pe_pb'] and val['pe_pb']<22.5 else 'WARNING: above 22.5 — Graham would consider this expensive.'}</li>
      <li style="margin:8px 0;font-size:13px;color:#374151;line-height:1.6"><strong>Growth priced in (Graham formula):</strong> {gpi_v}/yr. If actual growth is lower than this, the stock will move sideways or fall.</li>
    </ul>
  </div>
</div>

<div class="deep-card">
  <div class="deep-hdr" onclick="tog('bubble')"><span class="deep-em">🫧</span>
    <div class="deep-q">Is the stock in a bubble?</div>
    <span class="deep-chev" id="ch_bubble">+</span></div>
  <div class="deep-body" id="db_bubble" style="display:none">
    <div style="{'background:#d1fae5;color:#065f46;border-left:4px solid #059669' if len(n['valuation']['buy']) and (val['vs_hist'] or 0)<20 else 'background:#fef3c7;color:#78350f;border-left:4px solid #d97706'};padding:12px 16px;border-radius:8px;margin:0 0 12px;font-size:13px;font-weight:600">
      {'No bubble signals' if (val['vs_hist'] or 0)<30 else 'Caution — elevated valuation'}
    </div>
    <ul style="padding-left:20px;margin:0">
      <li style="margin:8px 0;font-size:13px;color:#374151;line-height:1.6">Current PE ({pe_v}) vs 10Y range ({fmt(val['pe_min'])}x–{fmt(val['pe_max'])}x): {'trading within historical norms' if val['pe'] and val['pe_min'] and val['pe']<val['pe_max']*0.9 else 'near 10-year highs'}</li>
      <li style="margin:8px 0;font-size:13px;color:#374151;line-height:1.6">P/E × P/B = {pepb_v} — Graham's 22.5 ceiling: {'✅ Safe' if val['pe_pb'] and val['pe_pb']<22.5 else '❌ Breached'}</li>
      <li style="margin:8px 0;font-size:13px;color:#374151;line-height:1.6">MCap CAGR ({pct(d['mcap_cagr'])}) vs earnings CAGR ({pct(g10)}): {'broadly aligned — no price/earnings disconnect' if abs((d['mcap_cagr'] or 0)-(g10 or 0))<0.05 else 'diverging — stock may have run ahead of fundamentals'}</li>
    </ul>
  </div>
</div>

<div class="deep-card">
  <div class="deep-hdr" onclick="tog('risks')"><span class="deep-em">⚠️</span>
    <div class="deep-q">What risks am I not seeing? Is it cyclical, seasonal, secular?</div>
    <span class="deep-chev" id="ch_risks">+</span></div>
  <div class="deep-body" id="db_risks" style="display:none">
    <ul style="padding-left:20px;margin:0">{risks_html}</ul>
  </div>
</div>

<div class="deep-card">
  <div class="deep-hdr" onclick="tog('5x')"><span class="deep-em">🎯</span>
    <div class="deep-q">Probability of 5× in 10 years?</div>
    <span class="deep-chev" id="ch_5x">+</span></div>
  <div class="deep-body" id="db_5x" style="display:none">
    <div style="background:{val['prob5x_color']};color:#fff;padding:12px 16px;border-radius:8px;margin:0 0 12px;font-size:13px;font-weight:600">{val['prob5x']}</div>
    <ul style="padding-left:20px;margin:0">
      <li style="margin:8px 0;font-size:13px;color:#374151;line-height:1.6"><strong>🐂 Bull ({pct(val['bull_g'])}/yr, PE stays {pe_v}):</strong> ₹1L → {bull_d}</li>
      <li style="margin:8px 0;font-size:13px;color:#374151;line-height:1.6"><strong>📊 Base ({pct(val['base_g'])}/yr, PE drifts to {avgpe_v}):</strong> ₹1L → {base_d}</li>
      <li style="margin:8px 0;font-size:13px;color:#374151;line-height:1.6"><strong>🐻 Bear ({pct(val['bear_g'])}/yr, PE compresses to {fmt(val['pe_l'])}x):</strong> ₹1L → {bear_d}</li>
    </ul>
  </div>
</div>

<div class="deep-card">
  <div class="deep-hdr" onclick="tog('struct')"><span class="deep-em">🏗️</span>
    <div class="deep-q">Are there structural weaknesses?</div>
    <span class="deep-chev" id="ch_struct">+</span></div>
  <div class="deep-body" id="db_struct" style="display:none">
    {sig_block(n['business_quality']['signals'][-2:]+n['operational']['signals'],
               n['business_quality']['warnings']+n['operational']['warnings'])}
  </div>
</div>

<div class="deep-card">
  <div class="deep-hdr" onclick="tog('mgmt')"><span class="deep-em">👔</span>
    <div class="deep-q">What do the numbers reveal about management quality?</div>
    <span class="deep-chev" id="ch_mgmt">+</span></div>
  <div class="deep-body" id="db_mgmt" style="display:none">
    <div class="sig-card sig-neutral" style="margin-bottom:10px">Management cannot be interviewed by retail investors — but numbers are their report card.</div>
    <div class="sig-card {'sig-green' if d['vpr'] and d['vpr']>1.5 else 'sig-red' if d['vpr'] and d['vpr']<1 else 'sig-amber'}"><strong>Capital Allocation:</strong> ₹1 retained → ₹{fmt(d['vpr'])} market cap gain. {'Excellent stewardship.' if d['vpr'] and d['vpr']>2 else 'Creates value but modest.' if d['vpr'] and d['vpr']>1 else 'Destroying shareholder value through retention.'}</div>
    <div class="sig-card {'sig-green' if inc_roe_latest and inc_roe_latest>15 else 'sig-red' if inc_roe_latest and inc_roe_latest<5 else 'sig-amber'}"><strong>Incremental ROE:</strong> {fmt(inc_roe_latest)}% — {'reinvested capital generating strong new profits' if inc_roe_latest and inc_roe_latest>15 else 'moderate returns on reinvestment' if inc_roe_latest and inc_roe_latest>5 else 'reinvestment barely generating new profit — question the expansion strategy'}.</div>
    <div class="sig-card {'sig-green' if sum(1 for c,p in zip(d['cfo'],d['pat']) if c and p and c>p)>=7 else 'sig-amber'}"><strong>Earnings Quality:</strong> CFO > PAT in {sum(1 for c,p in zip(d['cfo'],d['pat']) if c and p and c>p)}/10 years. {'Management not inflating profits.' if sum(1 for c,p in zip(d['cfo'],d['pat']) if c and p and c>p)>=7 else 'Sometimes reports profits without equivalent cash generation — verify.'}</div>
    <div class="sig-card sig-neutral"><strong>Dividend Track Record:</strong> Paid in {sum(1 for v in d['div'] if v and v>0)}/10 years. Payout ~{fmt(dpay_latest)}% of profits. {'Consistent.' if sum(1 for v in d['div'] if v and v>0)>=8 else 'Inconsistent.'} Retained earnings are reinvested into the business.</div>
  </div>
</div>

<div class="deep-card">
  <div class="deep-hdr" onclick="tog('alloc')"><span class="deep-em">⚖️</span>
    <div class="deep-q">How much portfolio allocation should I assign?</div>
    <span class="deep-chev" id="ch_alloc">+</span></div>
  <div class="deep-body" id="db_alloc" style="display:none">
    <div style="background:#eff6ff;color:#1d4ed8;border-left:4px solid #3b82f6;padding:12px 16px;border-radius:8px;margin:0 0 12px;font-size:13px;font-weight:600">
      Suggested: <strong>{alloc}% of portfolio</strong> &nbsp;({n['alloc_green']}/{n['alloc_total']} quality checks pass)
    </div>
    <div style="background:#f9fafb;border-radius:8px;padding:14px;margin:12px 0">
      <div style="font-size:12px;color:#6b7280;margin-bottom:4px">Currently held: {held_pct:.1f}% → Recommended: {alloc}%</div>
      <div style="height:12px;background:#e5e7eb;border-radius:6px;overflow:hidden"><div style="width:{fill:.0f}%;height:100%;background:#3b82f6;border-radius:6px"></div></div>
      <div style="font-size:12px;color:#374151;margin-top:6px">{alloc_msg}</div>
    </div>
    <p style="font-size:13px;color:#6b7280">Max single-stock for a long-term diversified portfolio: 8-10%. Adjust based on your conviction and sector exposure.</p>
  </div>
</div>

<div class="deep-card">
  <div class="deep-hdr" onclick="tog('buy')"><span class="deep-em">🕐</span>
    <div class="deep-q">Is now a good time to buy?</div>
    <span class="deep-chev" id="ch_buy">+</span></div>
  <div class="deep-body" id="db_buy" style="display:none">
    <div style="background:{bv_color};color:#fff;padding:12px 16px;border-radius:8px;margin:0 0 12px;font-size:13px;font-weight:600">{buy_label}</div>
    <p style="font-size:13px;color:#374151;line-height:1.7;margin:0 0 10px">{buy_desc}</p>
    <ul style="padding-left:20px;margin:0">
      <li style="margin:8px 0;font-size:13px;color:#374151;line-height:1.6">PE {pe_v} is {abs(val['vs_hist'] or 0):.0f}% {'below' if (val['vs_hist'] or 0)<0 else 'above'} historical average {avgpe_v}.</li>
      <li style="margin:8px 0;font-size:13px;color:#374151;line-height:1.6">For 5+ year horizons: valuation matters more than timing. Use SIP-style tranches to average in.</li>
    </ul>
  </div>
</div>

<!-- PORTFOLIO -->
<div class="stitle" style="margin-top:3rem">Your Portfolio Snapshot</div>
<div class="cc full">
  <div style="display:flex;gap:24px;margin-bottom:16px;flex-wrap:wrap">
    <div><span style="font-size:12px;color:#9ca3af">Invested</span><br><strong style="font-size:18px">₹{total_inv:,.0f}</strong></div>
    <div><span style="font-size:12px;color:#9ca3af">Current Value</span><br><strong style="font-size:18px">₹{total_val:,.0f}</strong></div>
    <div><span style="font-size:12px;color:#9ca3af">P&amp;L</span><br><strong style="font-size:18px;color:{pnl_col}">₹{pnl_tot:,.0f} ({pnl_pct:.1f}%)</strong></div>
  </div>
  <table class="gt">
    <thead><tr><th>Stock</th><th>Avg Cost</th><th>LTP</th><th>Invested</th><th>Current</th><th>P&amp;L</th></tr></thead>
    <tbody>{port_rows}</tbody>
  </table>
</div>

<div class="disc">⚠ DISCLAIMER: Educational only. Not investment advice. Consult a SEBI-registered advisor before investing. All probabilities are illustrative, not forecasts. Data from Screener.in Excel.</div>
</div>
<div class="foot">Generated · {now} · Dr Vijay Malik Analysis Framework · Screener.in</div>

<script>
const yrs={jsl(d['fy_labels'])};
const sales={jsa(d['sales'])};
const pat={jsa(d['pat'])};
const opm={jsa(d['opm'])};
const npm={jsa(d['npm'])};
const roe={jsa(d['roe'])};
const roce={jsa(d['roce'])};
const debt={jsa(d['borrow'])};
const cfo={jsa(d['cfo'])};
const fcf={jsa(d['fcf'])};
const rDays={jsa(d['rec_days'])};
const iDays={jsa(d['inv_days'])};
const wDays={jsa(d['wc_days'])};
const hPE={jsa(d['pe_h'])};
const ssgr={ssgr_data};
const qL={jsl(d['q_dates'])};
const qS={jsa(d['q_sales'])};      // Quarterly Revenue
const qP={jsa(d['q_pat'])};        // Quarterly PAT
const qOP={jsa(d['q_op'])};        // Quarterly Operating Profit
const qOPM={jsa(d['q_opm'])};      // Quarterly OPM %
const qNPM={jsa(d['q_npm'])};      // Quarterly NPM %
const qInt={jsa(d['q_int'])};      // Quarterly Interest
const qDep={jsa(d['q_dep'])};      // Quarterly Depreciation
const qPBT={jsa(d['q_pbt'])};      // Quarterly PBT
const qTax={jsa(d['q_tax'])};      // Quarterly Tax
const qSYoY={jsa(d['q_sales_yoy'])};  // Sales YoY growth %
const qPYoY={jsa(d['q_pat_yoy'])};    // PAT YoY growth %
// YoY labels: only last 6 quarters have a YoY pair
const qYoYL={jsl(d['q_dates'][-6:])};
const qSYoYv={jsa(d['q_sales_yoy'][-6:])};
const qPYoYv={jsa(d['q_pat_yoy'][-6:])};
const avgPE={round(val['avg_pe'],1) if val['avg_pe'] else 'null'};
const curPE={round(val['pe'],2) if val['pe'] else 'null'};
// New metric series
const ebitdaMargin={jsa(d['ebitda_margin'])};
const taxPct={jsa(d['tax_pct'])};
const ncg={jsa(d['net_cash_gen'])};
const surplus={jsa(d['surplus_funds'])};
const adjSh={jsa(d['adj_sh'])};
const riRate={jsa(d['reinvestment_rate'])};
const depNfa={jsa(d['dep_pct_nfa'])};
const nfaCwip={jsa(d['nfa_plus_cwip'])};
const rmPct={jsa(d['rm_pct_series'])};
const empPct={jsa(d['emp_pct_series'])};
const mcapHist={jsa(d['mcap_hist'])};

// YoY sales growth % for SSGR chart
const salesGrowth=sales.map((v,i)=>i===0?null:(v&&sales[i-1]?+((v/sales[i-1]-1)*100).toFixed(1):null));

const gc='rgba(0,0,0,0.05)',tc='#9ca3af',tf={{size:11,family:'inherit'}};
function bo(cb,legend=false){{return{{responsive:true,maintainAspectRatio:false,
  plugins:{{legend:{{display:legend,labels:{{color:tc,font:tf}}}},tooltip:{{mode:'index',intersect:false}}}},
  scales:{{x:{{grid:{{color:gc}},ticks:{{color:tc,font:tf}}}},
           y:{{grid:{{color:gc}},ticks:{{color:tc,font:tf,callback:cb}}}}}}}};}}

new Chart(document.getElementById('c1'),{{type:'bar',data:{{labels:yrs,datasets:[
  {{label:'Sales',data:sales,backgroundColor:'rgba(59,130,246,0.7)',borderRadius:4,order:2}},
  {{label:'Net Profit',data:pat,type:'line',borderColor:'#10b981',backgroundColor:'rgba(16,185,129,0.1)',tension:0.35,pointRadius:4,fill:true,order:1}}
]}},options:bo(v=>'₹'+v)}});

new Chart(document.getElementById('c2'),{{type:'line',data:{{labels:yrs,datasets:[
  {{label:'OPM%',data:opm,borderColor:'#6366f1',backgroundColor:'rgba(99,102,241,0.1)',tension:0.35,pointRadius:3,fill:true}},
  {{label:'NPM%',data:npm,borderColor:'#10b981',backgroundColor:'rgba(16,185,129,0.08)',tension:0.35,pointRadius:3,fill:true}}
]}},options:bo(v=>v+'%',true)}});

new Chart(document.getElementById('c3'),{{type:'line',data:{{labels:yrs,datasets:[
  {{label:'ROE%',data:roe,borderColor:'#3b82f6',backgroundColor:'rgba(59,130,246,0.1)',tension:0.35,pointRadius:3,fill:true}},
  {{label:'ROCE%',data:roce,borderColor:'#f59e0b',tension:0.35,pointRadius:3,borderDash:[4,3]}}
]}},options:bo(v=>v+'%',true)}});

new Chart(document.getElementById('c4'),{{type:'bar',data:{{labels:yrs,datasets:[
  {{label:'Hist PE',data:hPE,backgroundColor:hPE.map(v=>v&&curPE?v>curPE*1.1?'rgba(239,68,68,.45)':v<curPE*.9?'rgba(16,185,129,.5)':'rgba(99,102,241,.6)':'rgba(99,102,241,.6)'),borderRadius:4}},
  {{label:'Current',data:yrs.map(()=>curPE),type:'line',borderColor:'#ef4444',borderDash:[6,4],pointRadius:0,borderWidth:2}},
  {{label:'Avg',data:yrs.map(()=>avgPE),type:'line',borderColor:'#f59e0b',borderDash:[3,3],pointRadius:0,borderWidth:1.5}}
]}},options:bo(v=>v+'x')}});

new Chart(document.getElementById('c_ssgr'),{{type:'bar',data:{{labels:yrs,datasets:[
  {{label:'SSGR%',data:ssgr,backgroundColor:'rgba(99,102,241,0.65)',borderRadius:4,order:2}},
  {{label:'Sales Growth%',data:salesGrowth,type:'line',borderColor:'#f59e0b',backgroundColor:'rgba(245,158,11,0.1)',tension:0.35,pointRadius:3,fill:true,order:1}}
]}},options:bo(v=>v+'%',true)}});

new Chart(document.getElementById('c5'),{{type:'bar',data:{{labels:yrs,datasets:[
  {{label:'Debt',data:debt,backgroundColor:debt.map(v=>v>1000?'rgba(239,68,68,.65)':'rgba(251,146,60,.6)'),borderRadius:4,order:2}},
  {{label:'CFO',data:cfo,type:'line',borderColor:'#10b981',backgroundColor:'rgba(16,185,129,0.1)',tension:0.35,pointRadius:3,fill:true,order:1}}
]}},options:bo(v=>'₹'+v,true)}});

new Chart(document.getElementById('c_fcf'),{{type:'bar',data:{{labels:yrs,datasets:[
  {{data:fcf,borderRadius:4,backgroundColor:fcf.map(v=>v===null?'#e5e7eb':v<0?'rgba(239,68,68,.7)':'rgba(16,185,129,.65)')}}
]}},options:bo(v=>'₹'+v)}});

new Chart(document.getElementById('c7'),{{type:'line',data:{{labels:yrs,datasets:[
  {{label:'Rec Days',data:rDays,borderColor:'#f59e0b',tension:0.3,pointRadius:3}},
  {{label:'Inv Days',data:iDays,borderColor:'#ef4444',tension:0.3,pointRadius:3}},
  {{label:'WC Cycle',data:wDays,borderColor:'#6366f1',tension:0.3,pointRadius:3,borderDash:[5,4]}}
]}},options:{{...bo(v=>v+'d',true),scales:{{x:{{grid:{{color:gc}},ticks:{{color:tc,font:tf}}}},y:{{min:0,grid:{{color:gc}},ticks:{{color:tc,font:tf,callback:v=>v+'d'}}}}}}}}}});

new Chart(document.getElementById('cq1'),{{
  type:'bar',
  data:{{labels:qL,datasets:[
    {{label:'Revenue',data:qS,backgroundColor:'rgba(99,102,241,0.55)',borderRadius:4,order:2}},
    {{label:'Operating Profit',data:qOP,type:'line',borderColor:'#f59e0b',backgroundColor:'transparent',tension:0.3,pointRadius:4,pointBackgroundColor:'#f59e0b',order:1}},
    {{label:'Net Profit',data:qP,type:'line',borderColor:'#10b981',backgroundColor:'transparent',tension:0.3,pointRadius:4,pointBackgroundColor:'#10b981',order:1}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:false}},tooltip:{{mode:'index',intersect:false}}}},
    scales:{{x:{{grid:{{color:gc}},ticks:{{color:tc,font:tf,maxRotation:45}}}},
             y:{{grid:{{color:gc}},ticks:{{color:tc,font:tf,callback:v=>'\u20b9'+v}}}}}}}}
}});

new Chart(document.getElementById('cq2'),{{
  type:'line',
  data:{{labels:qL,datasets:[
    {{label:'OPM %',data:qOPM,borderColor:'#6366f1',backgroundColor:'rgba(99,102,241,0.08)',tension:0.3,pointRadius:4,fill:true}},
    {{label:'NPM %',data:qNPM,borderColor:'#10b981',backgroundColor:'rgba(16,185,129,0.08)',tension:0.3,pointRadius:4,fill:true}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:false}},tooltip:{{mode:'index',intersect:false}}}},
    scales:{{x:{{grid:{{color:gc}},ticks:{{color:tc,font:tf,maxRotation:45}}}},
             y:{{grid:{{color:gc}},ticks:{{color:tc,font:tf,callback:v=>v+'%'}}}}}}}}
}});

new Chart(document.getElementById('cq3'),{{
  type:'bar',
  data:{{labels:qYoYL,datasets:[
    {{label:'Sales YoY %',data:qSYoYv,backgroundColor:qSYoYv.map(v=>v===null?'#e5e7eb':v>=0?'rgba(99,102,241,0.65)':'rgba(239,68,68,0.65)'),borderRadius:4}},
    {{label:'PAT YoY %',data:qPYoYv,backgroundColor:qPYoYv.map(v=>v===null?'#e5e7eb':v>=0?'rgba(16,185,129,0.65)':'rgba(239,68,68,0.65)'),borderRadius:4}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:false}},tooltip:{{mode:'index',intersect:false,callbacks:{{label:ctx=>ctx.dataset.label+': '+ctx.parsed.y+'%'}}}}}},
    scales:{{x:{{grid:{{color:gc}},ticks:{{color:tc,font:tf,maxRotation:45}}}},
             y:{{grid:{{color:gc}},ticks:{{color:tc,font:tf,callback:v=>v+'%'}}}}}}}}
}});

new Chart(document.getElementById('cq4'),{{
  type:'line',
  data:{{labels:qL,datasets:[
    {{label:'Interest',data:qInt,borderColor:'#ef4444',backgroundColor:'rgba(239,68,68,0.08)',tension:0.3,pointRadius:4,fill:true}},
    {{label:'Depreciation',data:qDep,borderColor:'#f59e0b',backgroundColor:'rgba(245,158,11,0.08)',tension:0.3,pointRadius:4,fill:true}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:false}},tooltip:{{mode:'index',intersect:false}}}},
    scales:{{x:{{grid:{{color:gc}},ticks:{{color:tc,font:tf,maxRotation:45}}}},
             y:{{grid:{{color:gc}},ticks:{{color:tc,font:tf,callback:v=>'\u20b9'+v}}}}}}}}
}});

new Chart(document.getElementById('cq5'),{{
  type:'bar',
  data:{{labels:qL,datasets:[
    {{label:'PBT',data:qPBT,backgroundColor:'rgba(139,92,246,0.65)',borderRadius:4}},
    {{label:'Tax',data:qTax,backgroundColor:'rgba(239,68,68,0.55)',borderRadius:4}},
    {{label:'PAT',data:qP,backgroundColor:'rgba(16,185,129,0.65)',borderRadius:4}}
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:false}},tooltip:{{mode:'index',intersect:false}}}},
    scales:{{x:{{grid:{{color:gc}},ticks:{{color:tc,font:tf,maxRotation:45}}}},
             y:{{grid:{{color:gc}},ticks:{{color:tc,font:tf,callback:v=>'\u20b9'+v}}}}}}}}
}})

// ── Extended charts ─────────────────────────────────────────────────
new Chart(document.getElementById('c_ebitda'),{{type:'line',data:{{labels:yrs,datasets:[
  {{label:'EBITDA Margin%',data:ebitdaMargin,borderColor:'#6366f1',backgroundColor:'rgba(99,102,241,0.1)',tension:0.35,pointRadius:3,fill:true}},
  {{label:'OPM%',data:opm,borderColor:'#10b981',tension:0.35,pointRadius:3,borderDash:[4,3]}}
]}},options:bo(v=>v+'%',true)}});

new Chart(document.getElementById('c_tax'),{{type:'line',data:{{labels:yrs,datasets:[
  {{data:taxPct,borderColor:'#f97316',backgroundColor:'rgba(249,115,22,0.1)',tension:0.35,pointRadius:4,fill:true}}
]}},options:bo(v=>v+'%')}});

new Chart(document.getElementById('c_ncg'),{{type:'bar',data:{{labels:yrs,datasets:[
  {{data:ncg,borderRadius:4,backgroundColor:ncg.map(v=>v===null?'#e5e7eb':v>=0?'rgba(16,185,129,.65)':'rgba(239,68,68,.65)')}}
]}},options:bo(v=>'₹'+v)}});

new Chart(document.getElementById('c_surplus'),{{type:'line',data:{{labels:yrs,datasets:[
  {{data:surplus,borderColor:'#3b82f6',backgroundColor:'rgba(59,130,246,0.1)',tension:0.35,pointRadius:3,fill:true}}
]}},options:bo(v=>'₹'+v)}});

new Chart(document.getElementById('c_shares'),{{type:'bar',data:{{labels:yrs,datasets:[
  {{data:adjSh,borderRadius:4,backgroundColor:'rgba(99,102,241,0.6)'}}
]}},options:bo(v=>v+'Cr')}});

new Chart(document.getElementById('c_ri'),{{type:'bar',data:{{labels:yrs,datasets:[
  {{data:riRate,borderRadius:4,backgroundColor:riRate.map(v=>v===null?'#e5e7eb':v>1.5?'rgba(59,130,246,.7)':v>0?'rgba(16,185,129,.6)':'rgba(239,68,68,.65)')}}
]}},options:bo(v=>v+'x')}});

new Chart(document.getElementById('c_depnfa'),{{type:'line',data:{{labels:yrs,datasets:[
  {{data:depNfa,borderColor:'#f59e0b',backgroundColor:'rgba(245,158,11,0.1)',tension:0.35,pointRadius:3,fill:true}}
]}},options:bo(v=>v+'%')}});

new Chart(document.getElementById('c_nfacwip'),{{type:'bar',data:{{labels:yrs,datasets:[
  {{data:nfaCwip,borderRadius:4,backgroundColor:'rgba(129,140,248,.65)'}}
]}},options:bo(v=>'₹'+v)}});

new Chart(document.getElementById('c_costs'),{{type:'line',data:{{labels:yrs,datasets:[
  {{label:'RM%',data:rmPct,borderColor:'#ef4444',tension:0.35,pointRadius:3}},
  {{label:'Employee%',data:empPct,borderColor:'#f59e0b',tension:0.35,pointRadius:3,borderDash:[4,3]}}
]}},options:bo(v=>v+'%',true)}});

new Chart(document.getElementById('c_mcap'),{{type:'line',data:{{labels:yrs,datasets:[
  {{data:mcapHist,borderColor:'#8b5cf6',backgroundColor:'rgba(139,92,246,0.1)',tension:0.35,pointRadius:3,fill:true}}
]}},options:bo(v=>'₹'+v)}});

function tog(i){{
  var b=document.getElementById('db'+i=='db_q'?'db_q':'db_'+i)||document.getElementById('db'+i);
  var c=document.getElementById('ch'+i=='ch_q'?'ch_q':'ch_'+i)||document.getElementById('ch'+i);
  if(!b||!c)return;
  var open=b.style.display!=='none';
  b.style.display=open?'none':'block'; c.textContent=open?'+':'−';
}}
// open first card by default
document.getElementById('db_q').style.display='block';
</script>
</body></html>"""


# ─────────────────────── main ───────────────────────
def main():
    p=argparse.ArgumentParser(description='Long-term investor dashboard generator v3')
    p.add_argument('--excel');  p.add_argument('--portfolio'); p.add_argument('--url')
    p.add_argument('--output','-o',default='')
    a=p.parse_args()

    print(f"📂 Excel: {a.excel}")
    d=extract_excel(a.excel)
    print(f"   ✅ {d['company_name']} | ₹{d['current_price']} | SSGR={latest(d['ssgr'])}%")
    print(f"   ✅ PAT CAGR 5Y={pct(d['pat_cagr'].get('5y'))} | Avg PE={fmt(d['avg_pe'])} | VPR=₹{fmt(d['vpr'])}")

    print(f"📂 Holdings: {a.portfolio}")
    holdings,ti,tv=extract_holdings(a.portfolio)
    print(f"   ✅ {len(holdings)} stocks | ₹{ti:,.0f} invested | ₹{tv:,.0f} value")

    print(f"🌐 Screener: {a.url}")
    si=scrape_screener(a.url)
    print(f"   {'✅' if si.get('about') else '⚠ (network blocked in sandbox — will populate when run locally)'} About: {len(si.get('about',''))} chars")

    print("🧠 Building narrative…")
    n=build_narrative(d,si)
    print(f"   ✅ Verdict: {n['verdict']['text']} ({n['verdict']['score']}%)")

    print("🎨 Rendering HTML…")
    now=datetime.now().strftime('%d %b %Y')
    html=render(d,si,n,holdings,ti,tv,a.url,now)

    slug=re.sub(r'[^A-Z0-9]','_',d['company_name'].upper())
    out=a.output or f"{slug}_dashboard.html"
    Path(out).write_text(html,encoding='utf-8')
    print(f"\n✅ Saved: {out}  ({len(html)//1024} KB)")
    webbrowser.open(f"file://{os.path.abspath(out)}")

if __name__=='__main__':
    main()
