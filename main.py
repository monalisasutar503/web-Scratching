from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

review_list = []       


def get_soup(url):     
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      'Chrome/90.0.4430.212 Safari/537.36'}     
    response = requests.get(url, headers=header)
    soup = bs(response.content, 'html.parser')
    return soup         


def get_reviews(soup):     
    reviews = soup.find_all('div', {'data-hook': 'review'})    

    try:
        for items in reviews:       
            review = {
                'review_title': items.find('a', {'data-hook': 'review-title'}).text.strip(),
                'review_description': items.find('span', {'data-hook': 'review-body'}).text.strip(),
                'rating': items.find('i', {'data-hook': 'review-star-rating'}).text.strip(),
                'username': items.find('span', {'class': 'a-profile-name'}).text.capitalize().strip(),
                'review_date': items.find('span', {'data-hook': 'review-date'}).text.strip()
            }
            review_list.append(review)      


for x in range(1, 501):         
    soup = get_soup(f'https://www.amazon.co.uk/All-New-Fire-Tablet-Alexa-Display/product-reviews/B07952CV7L/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
    print(f'Getting review from page: {x}')        
    get_reviews(soup)
    print(len(review_list))                        
    if not soup.find('li', {'class': 'a-disabled a-last'}):    
        pass
    else:
        break

df = pd.DataFrame(review_list)         
df.to_excel('amazon_reviews.xlsx', index=False)         
print('Finished !')            

