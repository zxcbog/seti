import bs4
import requests


url = "https://www.muztorg.ru/category/akusticheskie-gitary"


def get_items_data(url, page_id):
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.text, "html.parser")
    items_grid = soup.find("div", class_="thumbnail-list grid-3")
    items_sections = items_grid.find_all("section", class_="product-thumbnail")
    items_data = []
    for i, item in enumerate(items_sections):
        if 'data-price' not in item.attrs:
            continue
        print(f"parsing item {i+1}/{len(items_sections)} at page {page_id}")
        price = item['data-price']
        meta_brand = item.next.next
        meta_prod_id = meta_brand.next.next
        prod_img_block = item.find("div", class_="product-pictures _brand-mark")
        img = prod_img_block.find("img")
        if 'data-src' in img.attrs:
            img = img['data-src']
        else:
            img = ""

        prod_data = item.find("div", class_="product-caption")
        category = prod_data.find("div", class_="product-catalog-grid").text
        prod_name = prod_data.find("div", class_="product-header").text
        prod_offer_data = prod_data.find("div", class_="product_offer")
        prod_price_data = prod_offer_data.find("div", class_="product-price")
        prod_old_price = prod_price_data.find("div", class_="old-price-with-discount")
        if prod_old_price is not None:
            p_old_price = prod_old_price.find("p", class_="old-price")
        else:
            p_old_price = None
        if p_old_price is not None:
            old_price = p_old_price.text.replace("р.", "").replace(" ", "")
            product_discount = prod_old_price.find("div", class_="product-discount").text.replace("\n", "")
        else:
            old_price = price
            product_discount = "0%"
        prod_rating = prod_data.find("div", class_="product-rating")
        if prod_rating is not None:
            prod_rating_value = float(prod_rating.find("div", class_="product-rating__value").text)
            prod_rating_text = prod_rating.find("div", class_="product-rating__text").text.replace("\n", "")
        else:
            prod_rating_value = 0
            prod_rating_text = "0 отзывов"
        items_data.append({
            "price": int(price),
            "old_price":int(old_price),
            "product_discount":product_discount,
            "name":prod_name.replace("\n", ""),
            "brand":meta_brand['content'],
            "rating":prod_rating_value,
            "review_num":prod_rating_text,
            "img":img,
            "product_id":meta_prod_id['content'].split("\\")[-1],
            "prod_category":category.replace("\n", ""),
        })


    return items_data


def parse(url):
    print("start parsing...")
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.text, "html.parser")
    pagination_block = soup.find("div", class_="pagination-container")
    page_number = int(pagination_block.find("li", class_="pagination-container__item _last").text)
    items_data = []
    page_limit = 2
    page_number = page_number if page_limit > page_number else page_limit
    for i in range(page_number):
        if i >= page_limit:
            break
        print(f"parsing page {i+1}/{page_number}")
        page_url = url + f"?page={i+1}"
        items_data += get_items_data(page_url, i + 1)

    print("all items have parsed, data was written in items_data.csv")
    return items_data


items = parse(url)

with open("items_data.csv", "w") as f:
    for item in items:
        item_keys_len = len(item.keys())
        for i, key in enumerate(item.keys()):
            f.write(f"{item[key]}")
            if i != item_keys_len - 1:
                f.write(";")
        f.write("\n")