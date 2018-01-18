import requests
from lxml import html

page = requests.get("http://sublime-text-unofficial-documentation.readthedocs.io/en/latest/reference/keyboard_shortcuts_win.html")
tree = html.fromstring(page.content)

element = tree.xpath('//table[@class="docutils"]/tbody//tr//td[text()="Move line/selection up"]');
print(element[0].text)
