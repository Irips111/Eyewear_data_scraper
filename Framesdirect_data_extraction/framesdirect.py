# Libraries Used
import csv
import json
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Test for response
url = "https://www.framesdirect.com/eyeglasses/"
r = requests.get(url)
print(r)

#  Function to clean price strings
def clean_price(price_str):
    if not price_str:
        return None
    cleaned = re.sub(r"[^\d.]", "", price_str)  # remove $ or other characters
    try:
        return float(cleaned)
    except ValueError:
        return None

# Step 1 - Setup Selenium + WebDriver
print("Setting up webdriver...")
chrome_option = Options()
chrome_option.add_argument("--headless")       # run without browser window
chrome_option.add_argument("--disable-gpu")    # needed for headless
chrome_option.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.6778.265 Safari/537.36"
)
print("done setting up...")

# Install the chrome driver
print("Installing Chrome WebDriver...")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_option)
print("Driver ready.")

# Step 2 - Open FramesDirect Eyeglasses Page 1
url = "https://www.framesdirect.com/eyeglasses/"
print(f"Visiting {url}")
driver.get(url)

# Step 3 - Wait for products to load
try:
    print("Waiting for product grid to load...")
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "fd-cat"))
    )
    print("Products loaded.")
except Exception as e:
    print(f"Error waiting for {url}: {e}")
    driver.quit()
    exit()

# Step 4 - Get page source and parse with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Step 5 - Extract product details
frames_data = []

# Each product card is inside div with class "prod-holder"
product_cards = soup.find_all("div", class_="prod-holder")

print(f"Found {len(product_cards)} products on page 1")

for card in product_cards:
    # Brand name
    brand = card.find("div", class_="catalog-name")
    brand = brand.text.strip() if brand else None

    name = card.find("div", class_="product-name")
    name = name.text.strip() if name else None
    
    # Product name
    product_name = card.find("div", class_="prod-model")
    product_name = product_name.text.strip() if product_name else None

    # Former price
    former_price = card.find("div", class_="prod-catalog-retail-price")
    former_price = clean_price(former_price.text.strip()) if former_price else None

    # Current price
    current_price = card.find("div", class_="prod-aslowas")
    current_price = clean_price(current_price.text.strip()) if current_price else None

    # Discount: make sure empty / missing -> None (so json.dump becomes null)
    discount_tag = card.find("div", class_="frame-discount")
    if discount_tag:
        disc_text = discount_tag.get_text(strip=True)
        discount = disc_text if disc_text != "" else None
    else:
        discount = None
    
    frames_data.append({
        "Brand": brand,
        "Product_Name": product_name,
        "Former_Price": former_price,
        "Current_Price": current_price,
        "Discount": discount
    })

    for item in frames_data:
     print(item)

     # Step 6 - Save data to CSV
if frames_data:
    column_names = frames_data[0].keys()
    with open("framesdirect_page1.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=column_names)
        writer.writeheader()
        writer.writerows(frames_data)
    print(f"Saved {len(frames_data)} records to framesdirect_page1.csv")

    # Step 7 - Save data to JSON
with open("framesdirect_page1.json", "w", encoding="utf-8") as json_file:
    json.dump(frames_data, json_file, indent=4, ensure_ascii=False)
print(f"Saved {len(frames_data)} records to framesdirect_page1.json")


# Step 8 - Close Browser
driver.quit()
print("End of Web Extraction ")