import json

from fpdf import FPDF
from jinja2 import Environment

with open('templates/report-template.jinja',"r") as f:
    template_string = " ".join(line.strip() for line in f)

with open('data.json') as f:
    response = json.load(f)

invoice = response["data"]["invoice"]

template = Environment().from_string(template_string)
pdf = FPDF()
pdf.add_page()
pdf.write_html(template.render(**globals()))
pdf.output("report-with-jinja.pdf")
