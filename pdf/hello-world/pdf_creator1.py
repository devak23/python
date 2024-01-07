import subprocess

from fpdf import FPDF

LIMIT_X = 208
LIMIT_Y = 295
MARGIN_TOP = 2
MARGIN_LEFT = 2
PADDING_LEFT = 2
PADDING_TOP = 2
BORDER_COLOR_INT = 217

pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.set_title("My First PDF")
pdf.set_author("Abhay K")
pdf.add_page()

pdf.set_margins(left=MARGIN_LEFT, top=MARGIN_TOP)
pdf.set_draw_color(BORDER_COLOR_INT,BORDER_COLOR_INT,BORDER_COLOR_INT)
pdf.rect(PADDING_LEFT, PADDING_TOP, LIMIT_X-PADDING_LEFT, LIMIT_Y-PADDING_TOP, )

pdf.set_font('Arial', 'B', 14)
pdf.cell(w=40, h=10, text='Hello World!', border=0, ln=1, align='', fill=False, link='')

pdf.set_font('Times', '', 8)
pdf.cell(340, 10, 'Powered by FPDF', 0, 1, 'C')

pdf.set_font('Helvetica', '', 12)
pdf.ln(50)
pdf.cell(85)
pdf.cell(0, 0, 'We are ok Houston!', 0)

pdf.image("steve_martin_quote.jpg", x=85, y=32.5, w=60, h=0, type='', link='')

pdf.output("sample.pdf")

subprocess.call(("xdg-open", "sample.pdf"))
