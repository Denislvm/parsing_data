import json
import requests
from bs4 import BeautifulSoup

main_url = "https://eldorado.ua"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0'
}


def get_soup(url):
    response = requests.get(url, headers)
    return BeautifulSoup(response.text, 'html.parser')


category_page = get_soup(main_url)
all_categories = category_page.findAll('div',
                                       class_='Megamenustyled__MainCategoryItem-sc-k9lul0-0 hcJnLl '
                                              'ui-library-gridItem-e24a ui-library-gridFlow-6fac ui-library-'
                                              'gridColumn-e638')

data = {}

for category in all_categories[:3]:
    category_url = category.find('a', class_='ui-library-action-80bf ui-library-actionLink-ec77 '
                                             'ui-library-buttonRadiusDefault-be7f ui-library-blue06-ad90 '
                                             'MenuItemstyled__StyledMegaMenuLink-sc-gkys1m-0 bZICcD').get('href')
    category_uri = main_url + category_url
    category_data = []
    subcategories = get_soup(category_uri)
    subb = subcategories.find('div', class_='SubCategorystyled__Container-sc-t4vzkk-1 uVwxs ui-library-gridItem-e24a')
    sub_links = []

    for sub in subb.find_all('a')[:1]:
        sub_link = sub.get('href')
        sub_links.append(sub_link)
        subcat_link = "https://eldorado.ua" + sub_link
        page_items = get_soup(subcat_link)
        all_items = page_items.findAll('div', class_='TileRenderstyled__StyledCollectionList-sc-1xi54fh-0 afNYp')

        for itms in all_items:
            link_items = itms.findAll('a', class_='GoodsImageslyed__StyledLinkWrapper-sc-1j176un-1 ogCdR '
                                                  'TileBlockstyled__StyledGoodsImage-sc-ogrpyx-8 lbptpB')

            for link_item in link_items[:3]:
                href_items = link_item.get('href')
                if href_items:
                    item_url = main_url + href_items
                    product_reviews = get_soup(item_url)
                    all_reviews = product_reviews.findAll('div', class_="comments-field")
                    button = product_reviews.find('div', class_="load-more-comments-container")
                    title = product_reviews.find('span', class_='product-name').text
                    rv_without_tags = []

                    for review in all_reviews:
                        reviews = review.findAll('div', class_='comment')

                        for rv in reviews:
                            rv_without_tags.append(rv.text.replace('div', ''))
                        an_list = []
                        date_list = []
                        grade_list = []
                        author_name = review.findAll('div', class_='name')
                        date = review.findAll('div', class_='date')
                        grade = review.findAll('span', itemprop="ratingValue")
                        for an, dt, grde in zip(author_name, date, grade):
                            an_list.append(an.text.replace('div', ''))
                            date_list.append((dt.text.replace('div', '')))
                            grade_list.append((grde.text))
                        try:
                            grade = review.find('span', itemprop="ratingValue").text

                            for rvv, anl, dt, grd in zip(rv_without_tags, an_list, date_list, grade_list):
                                item_data = {
                                    'Author': anl,
                                    'Rating': grd,
                                    'Title': title,
                                    'Review': rvv,
                                    'Date': dt,
                                    'Item URL': item_url
                                }
                                category_data.append(item_data)
                        except AttributeError:
                            item_data = {}
                            category_data.append(item_data)

    category_name = category.find('span', class_='ui-library-body2Regular-7f98 ui-library-actionContentLink-f37f').text

    data[category_name] = category_data
    print(f"Дані для категорії '{category_name}' збережено в файлі '{category_name}.json'.")

    with open(f'reviews/{category_name}.json', 'w', encoding='utf-8') as file:
        json.dump(category_data, file, indent=2, ensure_ascii=False, separators=(',', ': '))

# Вивід тестового варіанту усіх отриманих даних з кожної категорії локально
for category_name, category_data in data.items():
    print(f"Дані для категорії '{category_name}':")
    for item in category_data:
        print(item)