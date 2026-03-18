import pandas as pd
import numpy as np
import argparse
import matplotlib.pyplot as plt
from io import BytesIO
import base64


# ------------------------------------------------
# Load Sheet
# ------------------------------------------------

def load_sheet(path):

    df = pd.read_excel(path, sheet_name=1, header=None)

    df = df.dropna(how="all")

    return df


# ------------------------------------------------
# Extract metric from entire sheet
# ------------------------------------------------

def extract_metric(df, keywords):

    if isinstance(keywords,str):
        keywords=[keywords]

    for i,row in df.iterrows():

        first = str(row.iloc[0]).lower()

        for k in keywords:

            if k.lower() in first:

                values = pd.to_numeric(row.iloc[1:], errors="coerce")

                values = values.dropna()

                if len(values)>1:
                    values.index = range(len(values))
                    return values

    return None


# ------------------------------------------------
# CAGR
# ------------------------------------------------

def cagr(series):

    if series is None or len(series)<2:
        return None

    start = series.iloc[0]
    end = series.iloc[-1]

    if start<=0:
        return None

    years = len(series)-1

    return (end/start)**(1/years)-1


# ------------------------------------------------
# Financial interpretation
# ------------------------------------------------

def financial_story(sales,profit,opm,fcf,debt):

    story=[]

    g = cagr(sales)

    if g is not None:

        if g>0.15:
            story.append("Revenue growth is very strong.")

        elif g>0.08:
            story.append("Revenue growth appears steady.")

        else:
            story.append("Revenue growth is slow.")

    if opm is not None:

        if np.std(opm)<3:
            story.append("Operating margins appear stable.")
        else:
            story.append("Margins fluctuate which may indicate cyclicality.")

    if fcf is not None:

        pos = (fcf>0).sum()

        if pos/len(fcf)>0.7:
            story.append("Free cash flow is consistently positive.")
        else:
            story.append("Free cash flow is inconsistent.")

    if debt is not None and len(debt)>1:

        if debt.iloc[-1] > debt.iloc[0]:
            story.append("Debt has increased over time.")
        else:
            story.append("Debt has decreased over time.")

    if len(story)==0:
        story.append("Financial trends could not be derived from the sheet.")

    return story


# ------------------------------------------------
# Chart generator
# ------------------------------------------------

def chart(series,title):

    if series is None:
        return ""

    plt.figure()

    plt.plot(series.values)

    plt.title(title)

    buf=BytesIO()

    plt.savefig(buf,format="png")

    plt.close()

    img=base64.b64encode(buf.getvalue()).decode()

    return f'<img src="data:image/png;base64,{img}" width="450">'


# ------------------------------------------------
# Build HTML
# ------------------------------------------------

def build_html(company,story,charts):

    html=f"""
<html>
<head>
<title>{company} Dashboard</title>

<style>

body {{
font-family: Arial;
background:#f4f4f4;
margin:40px;
}}

.card {{
background:white;
padding:20px;
margin-bottom:20px;
border-radius:8px;
box-shadow:0 0 6px rgba(0,0,0,0.1);
}}

</style>

</head>

<body>

<h1>{company}</h1>

<div class="card">
<h2>Financial Interpretation</h2>
"""

    for s in story:
        html += f"<p>• {s}</p>"

    html += "</div>"

    html += "<div class='card'><h2>Charts</h2>"

    for c in charts:
        html += c

    html += "</div></body></html>"

    return html


# ------------------------------------------------
# MAIN
# ------------------------------------------------

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--excel", required=True)
    parser.add_argument("--portfolio")
    parser.add_argument("--url")

    args = parser.parse_args()

    df = load_sheet(args.excel)

    sales = extract_metric(df,["sales","revenue"])
    profit = extract_metric(df,["net profit"])
    opm = extract_metric(df,["opm"])
    fcf = extract_metric(df,["free cash flow","fcf"])
    debt = extract_metric(df,["borrowings","debt"])

    story = financial_story(sales,profit,opm,fcf,debt)

    charts=[]

    charts.append(chart(sales,"Sales Trend"))
    charts.append(chart(profit,"Profit Trend"))
    charts.append(chart(opm,"Operating Margin"))
    charts.append(chart(fcf,"Free Cash Flow"))

    company = args.excel.replace(".xlsx","")

    html = build_html(company,story,charts)

    with open("dashboard.html","w") as f:
        f.write(html)

    print("Dashboard created -> dashboard.html")


if __name__ == "__main__":
    main()