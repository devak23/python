import pypdf
import re

reader = pypdf.PdfReader("AccountStmt.pdf")
pages = reader.pages
pattern_to_find = "Folio Id : [0-9]+"

for page in reader.pages:
    text = page.extract_text()
    match = re.search(pattern_to_find, text)
    print (match, match.group())
    print(match.group().split(' : ')[1])
