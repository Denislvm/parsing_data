import requests
from bs4 import BeautifulSoup

main_url = "https://eldorado.ua"
category_urls = []
headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0'
}


def get_soup(url):
    response = requests.get(url, headers)
    return BeautifulSoup(response.text, 'html.parser')


category_page = get_soup(main_url)
all_categories = category_page.findAll('div', class_='Megamenustyled__MainCategoryItem-sc-k9lul0-0 hcJnLl '
                                        'ui-library-gridItem-e24a ui-library-gridFlow-6fac ui-library-gridColumn-e638')
# print(all_categories)
for category in all_categories[:3]:
    category_url = category.find('a', class_='ui-library-action-80bf ui-library-actionLink-ec77 '
                                             'ui-library-buttonRadiusDefault-be7f ui-library-blue06-ad90 '
                                             'MenuItemstyled__StyledMegaMenuLink-sc-gkys1m-0 bZICcD').get('href')
    category_url = 'https://eldorado.ua' + category_url
    category_urls.append(category_url)
    subcategories = get_soup(category_url)
    subb = subcategories.find('div', class_='image')
    sub_links = []
    for sub in subb.find_all('a'):
        sub_link = sub.get('href')
        sub_links.append(sub_link)
        subcat_link = "https://eldorado.ua" + sub_link
        page_items = get_soup(subcat_link)
        all_items = page_items.find_all('div', class_='TileRenderstyled__StyledCollectionList-sc-1xi54fh-0 afNYp')
        for it in all_items:
            link_items = it.findAll('a', class_='GoodsImageslyed__StyledLinkWrapper-sc-1j176un-1 ogCdR TileBlockstyled__StyledGoodsImage-sc-ogrpyx-8 lbptpB')
            for link_item in link_items[:3]:
                href_items = link_item['href']
                item_url = main_url + href_items
                product_reviews = get_soup(item_url)
                all_reviews = product_reviews.findAll('div', class_="comments-field")
                for review in all_reviews:
                    try:
                        reviews = review.find('div', class_='comment').text

                    except AttributeError:
                        reviews = None
                    print(reviews, item_url)


    # .text.replace('div', '')







    # Вывести список ссылок на подкатегории
    # print(f"Подкатегории для: {category_url}:")
    # for sub_link in sub_links:
    #     print("https://eldorado.ua" + sub_link)





