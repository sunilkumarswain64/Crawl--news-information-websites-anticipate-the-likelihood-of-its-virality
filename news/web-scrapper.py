import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

res = requests.get('https://www.ndtv.com/world-news')
soup = BeautifulSoup(res.content, 'html.parser')


weblinks = soup.find_all('div', attrs = {'class':'nstory_header'})


pagelinks = []
for link in weblinks:     
    link = link.find('a') 
    pagelinks.append(link.get('href'))


articletitle = []
articletext = []
tag = []
description=[]
for link in pagelinks:    
    # store the text for each article
    paragraphtext = []    

    # get page text
    
    try:
        res = requests.get(link)
        
    except requests.ConnectionError as e:
        print(str(e))            
        continue
    except requests.Timeout as e:
        print(str(e))
        continue
    except requests.RequestException as e:
        print(str(e))
        continue
    except KeyboardInterrupt:
        print("closed the program")
    # parse with BFS
    soup = BeautifulSoup(res.text, 'html.parser')    

    # get article title

    atitle = soup.find(class_="sp-ttl").get_text() 
    #article description
    adescription = soup.find(class_="sp-descp").get_text()
    #article tags
    atag = soup.find(class_="tg_wrp").get_text() 
    
    # get main article page
    articlebody = soup.find(class_="sp-cn ins_storybody")
    # get text
    atext = soup.find_all('p')
    # print text
    for paragraph in atext:
        # get the text only
        text = paragraph.get_text()
        paragraphtext.append(text)    
        
    # combine all paragraphs into an article
    articletext.append(paragraphtext)
    articletitle.append(atitle)
    tag.append(atag)
    description.append(adescription)
    
myarticle = [' '.join(article) for article in articletext]
print('Done!!!!')
# save article data to file
data = {'link':pagelinks,
        'Title':articletitle,
        'description':description,  
        'Article':myarticle, 
        'Tags':tag
        }
news = pd.DataFrame(data=data)
news.to_csv('news.csv', mode='a', header=False)
print('Saved...')
 