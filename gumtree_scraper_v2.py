from bs4 import BeautifulSoup
import requests
import pandas as pd
import concurrent.futures


def scrape_listing(url):
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    df_listing = []
    try:
        list_of_items = soup.find("div", class_="user-ad-collection-new-design__wrapper--row")

        for item in list_of_items:
            title_span = item.find("span", class_="user-ad-row-new-design__title-span") 
            price_span = item.find("span", class_="user-ad-price-new-design__price") 
            location_div = item.find("div", class_="user-ad-row-new-design__location") 
            date_p = item.find("p", class_="user-ad-row-new-design__age")
            description_p = item.find("p", class_="user-ad-row-new-design__description-text") 

            try:
                title = title_span.getText()
                price = price_span.getText()
                location = location_div.getText()

                suburb, rest = location.split(',', 1)
                state = rest.split('<', 1)[0].strip()

                date = date_p.getText()
                description = description_p.getText()
            except:
                title = None
                price = None
                location = None
                suburb = None
                state = None
                date = None
                description = None

            df_item = pd.DataFrame({
                "Title": [title],
                "Price": [price],
                "Location": [location],
                "Suburb": [suburb],
                "State": [state],
                "Date": [date],
                "Description": [description]
            })

            df_listing.append(df_item)
        
        df_listing = pd.concat(df_listing)

        return df_listing
    except:
        print(f"Error in getting the listing: {url}")
        return pd.DataFrame({
                "Title": [None],
                "Price": [None],
                "Location": [None],
                "Suburb": [None],
                "State": [None],
                "Date": [None],
                "Description": [None]
            })


class Category:
    def __init__(self, name, id_):
        self.name = name
        self.code = id_

    def __repr__(self):
        return f"Category(name='{self.name}', id={self.id})"


# Create an empty list to store the categories
categories = []

# Open and read the file
with open('categories.txt', 'r') as file:
    for line in file:
        # Split each line on the space character to get the name and code
        name, code = line.strip().split()
        # Create a new Category object and append it to the list
        categories.append(Category(name, code))

def scrape_category(category):
    df_category_full_listing = []
    urls = []
    for i in range(50):
        if i == 0:
            url = f"https://www.gumtree.com.au/{category.name}/nsw/{category.code}l3008839?sort=price_asc"
            urls.append(url)
        else:
            url = f"https://www.gumtree.com.au/{category.name}/nsw/page-{i}/{category.code}l3008839?sort=price_asc"
            urls.append(url)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        df_category_full_listing = list(executor.map(scrape_listing, urls))
    
    df_category_full_listing = pd.concat(df_category_full_listing)
    
    return df_category_full_listing

df_output_list = []
for category in categories:
    df_category = scrape_category(category)
    df_output_list.append(df_category)

df_output = pd.concat(df_output_list)

df_output = df_output.drop_duplicates()

df_output.to_excel("output.xlsx", index=False, engine='openpyxl')



        



