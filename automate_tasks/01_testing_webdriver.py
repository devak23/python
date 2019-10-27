from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException


def clickLink(link_text, browser):
  linkElement = browser.find_element_by_link_text(link_text)
  print(linkElement)
  linkElement.click()

def main():
  browser = webdriver.Chrome()
  # browser.implicitly_wait(4)
  print (type(browser))
  browser.get("http://www.inventwithpython.com/")
  clickLink('Cracking Codes with Python', browser)
  clickLink('Read Online for Free', browser)
  linkElement = browser.find_element_by_xpath("/html[1]/body[1]/div[2]/div[1]/ul[2]/li[10]/a[1]")
  print (linkElement)
  linkElement.click()

  input("Press any key to exit...")

if __name__ == '__main__':
  main()
