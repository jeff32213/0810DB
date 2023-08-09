import requests
import json
import time
from fake_useragent import UserAgent
import pymssql
import concurrent.futures


db_settings = {
    "host": "127.0.0.1",
    "user": "db",
    "password": "db",
    "database": "ncu_db",
    "charset": "utf8"
}

def find(url):
    try:
        user_agent = UserAgent()
        conn = pymssql.connect(**db_settings)
        with conn.cursor() as cursor:
            insert_command = "INSERT INTO [dbo].[stock_data](stock_code, date, tv, t, o, h, l, c, d, v) VALUES (%s, %s, %d, %d, %s, %s, %s, %s, %s, %s)"
            try:
                response = requests.get(url=url, headers={ 'user-agent': user_agent.random })
                data = response.text  # 這是json格式的資料
                a_json = json.loads(data)  # 轉成dict
                if("tpex" in url):
                    data_str = "aaData"
                else:
                    data_str = "data"
                for data in a_json[data_str]:
                    date = data[0].split("/")
                    data[0] = str(1911 + int(date[0])) + date[1] + date[2]
                    data[1] = int(data[1].replace(",", ""))
                    data[2] = int(data[2].replace(",", ""))
                    data[3] = float(0.0 if data[3].replace(',', '') == '--' else data[3].replace(',', ''))
                    data[4] = float(0.0 if data[4].replace(',', '') == '--' else data[4].replace(',', ''))
                    data[5] = float(0.0 if data[5].replace(',', '') == '--' else data[5].replace(',', ''))
                    data[6] = float(0.0 if data[6].replace(',', '') == '--' else data[6].replace(',', ''))
                    data[7] = float(0.0 if data[7].replace(',', '') == 'X0.00' else data[7].replace(',', ''))
                    data[8] = float(data[8].replace(",", ""))
                    company_id = url.split("=")[-1]
                    cursor.execute(insert_command, (company_id, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
                    conn.commit()
                time.sleep(10)
                print(time.strftime("%H:%M:%S", time.localtime()) + " " + str(url))
            except Exception as ex:
                time.sleep(10)
                print(time.strftime("%H:%M:%S", time.localtime()) + " error " + str(url))
        conn.close()
    except Exception as e:
        print(e)


def run():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(find, all_url)


try:  
    all_url = []
    all_stock =[]
    conn = pymssql.connect(**db_settings)
    with conn.cursor() as cursor:
        command = "select * from [dbo].[stock_list] where [isTaiwan50] = 1"
        cursor.execute(command)
        result = cursor.fetchall()
        for year in range(2023, 2024):
            for month in range(1, 13):
                for r in result:
                    try:
                        stock = r[0]
                        date = str(year)+f"{month:02d}"+"01"
                        if r[2].strip() == "上市":
                            address = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={date}&stockNo={stock}"
                        elif r[2].strip() == "上櫃":
                            date = str(year-1911) + f"{month:02d}"
                            address = f"http://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info/st43_result.php?d={date}&stkno={stock}"
                        all_url.append(address)
                        all_stock.append(r[0])
                    except Exception as ex:
                        continue                                     
        conn.close()           
except Exception as ex:
    print(ex)

# print(all_url[0])
run()
