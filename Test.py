import requests
from bs4 import BeautifulSoup
import pandas as pd
htmlList = ["0.html", "10.html", "20.html"]
contentList = []
soupList = []
for i in htmlList:
    print(i)
    r = requests.get(
        "https://pythonizing.github.io/data/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="+i)

    c = r.content
    contentList.append(c)
for content in contentList:
    soup = BeautifulSoup(content, "html.parser")
    soupList.append(soup)
print(len(soupList))
allList = []
for soups in soupList:
    all = soups.find_all('div', {"class": "propertyRow"})
    allList.append(all)

# znalezienie wszystkich divow o klasie propertyRow
#all[0].find('h4', {"class":"propPrice"}).text.replace("\n",'').replace(' ', '')
# sposrod tych dibow chcemy zeby wyswietlalo nam h4 z klasa propPrice w formie tekstu
homeList = []
i = 0
while i <= 3:
    for i in range(0, 3):
        for item in allList[i]:
            i += 1
            print(i)
            # musimy dodac do kazdej petli slownik, ktory bedzie przechowywal dane
            d = {}
            d["Address"] = item.find_all('span', {'class': 'propAddressCollapse'})[
                0].text.replace("\n", '')
            d["Locality"] = item.find_all('span', {'class': 'propAddressCollapse'})[
                1].text.replace("\n", '')
            d["Price"] = item.find('h4', {"class": "propPrice"}).text.replace(
                "\n", '').replace(' ', '')
            # try to prevent None attribute error
            try:
                d["Beds"] = item.find(
                    'span', {"class": "infoBed"}).find('b').text
            except:
                d["Beds"] = None
            # find('b') because value was inside of <span><b> value</b></span>
            try:
                d["Full Bath"] = item.find(
                    'span', {"class": "infoValueFullBath"}).find('b').text
            except:
                d["Full Bath"] = None
            try:
                d["Area"] = item.find(
                    'span', {"class": "infoSqFt"}).find('b').text
            except:
                d["Area"] = None
            try:
                d["Half Baths"] = item.find(
                    'span', {"class": "infoValueHalfBath"}).find('b').text
            except:
                d["Half Baths"] = None
                # iterujemy na poczatku przez wszystkie divy o klasie columnGroup w celu wylapania wszystkich <span> przechowujacych feature name i feature group
            for column_group in item.find_all('div', {"class": 'columnGroup'}):
                # print(column_group)
                # iterujemy nastepnie przez wczesniej znalezione <span> tj. 2 kolumny feature group i feature name
                for feature_group, feature_name in zip(column_group.find_all('span', {"class": 'featureGroup'}), column_group.find_all('span', {"class": "featureName"})):
                    if "Age" in feature_group.text:
                        d["Age"] = feature_name.text
                    if "Lot Size" in feature_group.text:
                        d["Lot Size"] = feature_name.text
                # Jezeli feature group danego boxa nazywa sie "age" to przypisz mu jego wartosc feature name
            print('\n')
            # z racji tego, ze adresy mieszcza sie w dwoch boksach, to musimy uzyc
            # funkcji find_all, aby stworzyc listy i wskazywac na konkretne boxy
            # indeksami z listy
            homeList.append(d)


df = pd.DataFrame(homeList)
df.to_csv('Output.csv')
print(df)
