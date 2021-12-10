import requests
from bs4 import BeautifulSoup

# we need to get url from requests library
r = requests.get("https://pythonizing.github.io/data/example.html")

# grabbing content (sourcecode) from requested url
content = r.content


# making and object of BeatifulSoup class which points for sourcode we get form requests.content
soup = BeautifulSoup(content, "html.parser")


all = soup.find_all("div", {"class": "cities"})

one = soup.find("div", {"class": "cities"})  # if we want find only first div

# becasue find_all method is returning list we can iterate through it
for i in all:
    print(i.find_all("h2")[0].text)  # iterate through div to get pure h2
print("-"*30)
# if we want to find h1 except of divs we can use again
# find_all method inside variable which stores "div" data
# but we need to use all[index] because all is an list
print(all[0].find_all("h2"))
print("-"*30)
# if we want only text without <>
print(all[0].find_all("h2")[0].text)
