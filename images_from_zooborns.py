import bs4
import requests

response = requests.get('https://www.zooborns.com/zooborns/')
#print(response)

soup = bs4.BeautifulSoup(response.text, "html.parser")
#print(soup.prettify())

a_sonuclari = soup.find_all('a')
#print(a_sonuclari)

list_a = []
for a in a_sonuclari:
    if a.has_attr('class') and a['class'][0] == 'asset-img-link':
        list_a.append(a)
#print(list_a)
        
list_img_url = []
for a in list_a:
    img_listesi = a.find_all('img')
    for b in img_listesi:
        list_img_url.append(b['src'])
#print(list_img_url)

count = 0
for url in list_img_url:
    count = count + 1
    print("Currently downlading image from: " + url)
    response = requests.get(url)
    file = open("hayvan" + str(count) + ".jpeg", "wb")
    file.write(response.content)
    file.close()
   
print("done")

