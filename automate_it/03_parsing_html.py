import bs4

myfile = open("03_python.html", "r")
soup = bs4.BeautifulSoup(myfile, "lxml")

# Making the soup
print ("BeautifulSoup Object: ", type(soup))

# find elements by tags
print (soup.find_all('a'))
print (soup.find_all('strong'))

# find elements by id
print(soup.find('div', {"id": "inventor"}))
print(soup.select('#inventor'))

