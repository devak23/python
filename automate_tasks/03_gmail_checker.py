from sys import argv

from selenium import webdriver

if len(argv) < 2:
  print("Usage: python 03_gmail.py <username> <password>")
  raise ValueError("Usage not appropriate")

browser = webdriver.Chrome()
browser.implicitly_wait(30)

browser.get("http://www.gmail.com")
emailElem = browser.find_element_by_id('identifierId')
emailElem.send_keys(argv[1])

nextBtn = browser.find_element_by_id('identifierNext')
nextBtn.click()


# passElement = browser.find_element_by_xpath("//div[@class='Xb9hP']/input[type='password']")
passElement = browser.find_element_by_xpath("id('password')/div[1]/div[1]/div[1]/input[1]")
passElement.send_keys(argv[2])

nextBtn = browser.find_element_by_id("passwordNext")
nextBtn.click()
