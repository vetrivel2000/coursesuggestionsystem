import requests
from bs4 import BeautifulSoup
import pandas as pd
from textblob import TextBlob

reviewlist = []
tutorlist = []

def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    return soup


def get_reviews(soup):
    reviews = soup.find_all('div', {'class': 'review'})
    try:
        for item in reviews:
            review = {
            'NAME':item.find('p', {'class': 'reviewerName'}).text.replace('By', '').strip(),        
            'COMMENTS':item.find('div',{'class': 'reviewText'}).text.strip(),
            }
            reviewlist.append(review)
    except:
        pass        

link = input("Enter the course link you want to purchase:")
for x in range(1,4):
    soup = get_soup(f'{link}/reviews?page={x}')
    print(f'Getting page: {x}')    
    get_reviews(soup)
    print(len(reviewlist))

coursename = soup.find('div',{'class':'font-sm'}).text.replace('Back to', '').strip()

clink = get_soup(link)
instructor = clink.find_all('div',{'class':'instructor-wrapper'})
for item in instructor:
    tutor = {
    'Name':item.find('h3',{'class':'instructor-name'}).text.strip(),
    'No.of.courses':item.find('div',{'class':'courses-count'}).text.strip(),
    'No.of.learners':item.find('div',{'class':'learners-count'}).text.strip(),        
    } 
    tutorlist.append(tutor)


print("The tutors are:")
print(tutorlist)


print(reviewlist)


df = pd.DataFrame(reviewlist)
df.to_csv(r'E:\\coreview.csv',index=False)
dfc=df['COMMENTS']
print(dfc)
positive=0
negative=0
for dtr in dfc:
    blob=TextBlob(dtr)
    print(blob.sentiment)
    if blob.sentiment.polarity>0:
        positive+=1
    elif blob.sentiment.polarity<=0:
        negative+=1
print(positive)
print(negative)
if negative<1/2*positive:
   print(f'{coursename} Highly Recommended')    
else:
   print(f'{coursename} would not be Recommended')
