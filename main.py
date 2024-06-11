import csv
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def crawling():
    stocks = []
    for i in tqdm(range(1,6)): # 5
        response = requests.get("https://finance.naver.com/sise/sise_market_sum.nhn", {
            "page": i
        })

        if (response.status_code == 200):
            html = response.text
            soup = BeautifulSoup(html, "html.parser")

            count = 0
            offset = 1
            while(count < 50):
                count += 1
                nameWithCode = soup.select_one(f"#contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child({count+offset}) > td:nth-child(2) > a")

                code = nameWithCode.attrs['href'].replace('/item/main.naver?code=', "")
                name = nameWithCode.get_text()
                price = int(soup.select_one(f"#contentarea > div.box_type_l > table.type_2 > tbody > tr:nth-child({count+offset}) > td:nth-child(3)")
                            .get_text().replace(",", ""))

                stocks.append({"code": code, "name": name, "price": price})
                if count%5 == 0 and count != 50:
                    offset+=3
        else:
            print(f"error with {response.status_code}")

    with open("stocks.csv", 'w') as f:
        field_names = stocks[0].keys()
        w = csv.DictWriter(f, fieldnames=field_names)

        w.writeheader()
        w.writerows(stocks)

        f.close()

if __name__ == '__main__':
    crawling()