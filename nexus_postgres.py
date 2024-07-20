import psycopg2
import nexus_webcrawler as nw
import time

conn = psycopg2.connect(database="CCNCS",
                        user="postgres",
                        password="123456",
                        host="localhost",
                        port=5432)
print("DB connected.")

cur = conn.cursor()
cur.execute("""
            DROP TABLE IF EXISTS crawler_data1;
            CREATE TABLE crawler_data1 (
                id INTEGER PRIMARY KEY NOT NULL,
                title_name TEXT NOT NULL,
                category TEXT,
                price TEXT,
                availability TEXT,
                payment_option TEXT,
                shipping_details TEXT,
                vendor_name TEXT,
                total_sales INTEGER,
                activity TEXT
            );
            """)
conn.commit()
print("Table created.")


if __name__ == "__main__":
    url = "http://nexusma2isutrqi4ineftrzqzui7tefsyeonxsttsnwzdxxpxay26eqd.onion"
    (firefox_options, service) = nw.driver_setup()
    driver = nw.webdriver.Firefox(options=firefox_options, service=service)

    driver.get(url)
    print("Please solve the DDOS Protection in the browser.")
    time.sleep(90)
    print("Time up!")

    username_input = driver.find_element(nw.By.NAME, 'username')
    password_input = driver.find_element(nw.By.NAME, 'password')
    username_input.clear()
    password_input.clear()
    username_input.send_keys('Unknown890market')
    password_input.send_keys('unknown123')
    print("Username and Password entered.")
    time.sleep(30)
    print("Time up!")

    category_links = nw.get_category_links(driver)
    item_no = 1
    for category in category_links:
        driver.get(category)
        last_page_no = nw.get_last_page(driver)
        print(last_page_no)
        for page in range(1, int(last_page_no) + 1):
            if page == 1:
                present_page = category
            else:
                present_page = nw.get_next_page(driver, page - 1)
            products_links = nw.get_product_links(driver)
            for product in products_links:
                driver.get(product)
                info_list = []
                info_res = nw.get_info(driver, info_list, category)
                cur.execute("""
                            INSERT INTO crawler_data1
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, (item_no, info_res[0], info_res[1], info_res[2], info_res[3], info_res[4], info_res[5], info_res[6], info_res[7], info_res[8]))
                conn.commit()
                print(f"Item No: {item_no} added.")
                item_no += 1
            if page == int(last_page_no):
                break
            else:
                driver.get(present_page)
                next_page = nw.get_next_page(driver, page + 1)
                driver.get(next_page)

    driver.quit()
