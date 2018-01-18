import requests
from lxml import html

page = requests.get("https://github.com/pricing/")
# fromString converts the content of the page (from string format) into HTML
tree = html.fromstring(page.content)
print ("Page Object: ", tree)

# look for the h2 with class "alt-h3"
plans = tree.xpath('//h2[@class="alt-h3"]/text()')
# look for span with class default-currency
pricing = tree.xpath('//span[@class="default-currency"]/text()')
print("Plans: ", plans, "Pricing: ", pricing)
