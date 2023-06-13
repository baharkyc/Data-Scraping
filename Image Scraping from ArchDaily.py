"""
Bu kod Archdaily websitesinden mimari imajlar indirir. Bu imajlar bu kod için 'kesit imajları' olmak üzere seçilmiştir.
"""

from selenium import webdriver
import bs4
import time
import requests


# bu fonksiyona istenen sayfanın linki verilecek.
def getUrlListFromSource(soup_source_code):
    
    tag_A = soup.find_all("a")
    # sayfayı kapsayan soup objesinin içerisindeki <a>'ların tamamını çıkarır
    # tüm <a>'ların içerisinden sadece <a class="gridview__content"> olanları filtered_a_list_by_class listesine ekler
    filtered_a_list_by_class = []
    for a in tag_A:
        if a.has_attr('class') and a['class'][0] == 'gridview__content':
            filtered_a_list_by_class.append(a)

    # <a class="gridview__content">'lerin href'lerindeki linkleri alıp url_list'e atar.
    url_list = []
    for a in filtered_a_list_by_class:
        url_list.append(a["href"])
    return url_list 


# [[1, 2], [3, 4], [5, 6, 7]] gibi bir listeyi [1, 2, 3, 4, 5, 6, 7] formuna çevirir. bu operasyona genel olarak flatten denir.
def flatten_list(list):
    flat_list = []
    for sublist in list:
        for item in sublist:
            flat_list.append(item)
    return flat_list


#Selenium ile Ana sayfaya bağlan, sayfayı en aşağı kaydır ve soup'a kaynak kodu ilet..
driver = webdriver.Chrome('Chrome Driver konumunu girmelisiniz.')
main_page = 'https://www.archdaily.com/search/projects/categories/office-buildings?ad_medium=filters'


driver.get(main_page)
count = 0
SCROLL_PAUSE_TIME = 0.5
while count < 21: #kaç kez scroll down yapacak.
    count = count + 1
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") # En aşağı kaydır sayfayı.
    time.sleep(SCROLL_PAUSE_TIME) # sayfa yüklenmesi için bekleme gecikmesi.
source = (driver.page_source)
print(source)
driver.quit()
soup = bs4.BeautifulSoup(source, "html.parser")
# Soup için html kodu hazır.

list_of_links = []
url_list_for_each_page = getUrlListFromSource(soup)
list_of_links.append(url_list_for_each_page)


final_projects_url_list = flatten_list(list_of_links)
print(final_projects_url_list)
print(str(len(final_projects_url_list)) + " links fetched.")


# bu fonksiyon her projenin linkine tek tek uygulanacak, linklerin içinden imajları alacak.
def get_section_images_from_one_link (project_link):
    driver = webdriver.Chrome('/users/Bahar/Desktop/chromedriver')
    driver.get(project_link)
    source = (driver.page_source)
    driver.quit()
    
    soup = bs4.BeautifulSoup(source, "html.parser")
   
    tag_img = soup.find_all("img")
    
    alt_filtered_in_img_list = []
    for x in tag_img:
        if x.has_attr("alt") and ("Section" in x["alt"]):
            alt_filtered_in_img_list.append(x)
            
    # srcset etiketi olanlardan srcsetleri alıyoruz.
    get_srcset_from_alt_section_list = []
    for x in alt_filtered_in_img_list:
        if x.has_attr("srcset"):
            get_srcset_from_alt_section_list.append(x['srcset'])
    
    # srcset stringinde ilk boşluğa kadar olan yazılar bize gereken url, onu alıyoruz.
    img_urls_taken_from_srcset = []
    for x in get_srcset_from_alt_section_list:
       img_urls_taken_from_srcset.append(x.split(" ")[0])
       
    return img_urls_taken_from_srcset

final_section_links = []
for i in final_projects_url_list:
    final_section_links.append(get_section_images_from_one_link(i))

flatten_section_urls_list = flatten_list(final_section_links)
    
print(str(len(flatten_section_urls_list)) + " links fetched.")

count = 0
for url in flatten_section_urls_list:
    count = count + 1
    print("Currently downlading image from: " + url)
    response = requests.get(url)
    file = open("section" + str(count) + ".jpeg", "wb")
    file.write(response.content)
    file.close()
   
print("done")

