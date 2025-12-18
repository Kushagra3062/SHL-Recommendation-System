import time
import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL_TEMPLATE = "https://www.shl.com/products/product-catalog/?start={}&type=1" 

OUTPUT_FILE = "shl_assessments.csv"

def setup_driver():
    options = Options()

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def scrape_shl_direct_url():
    driver = setup_driver()
    
    all_links = []
    seen_urls = set()
    start_offset = 0
    items_per_page = 12
    page_num = 1
    
    print("--- Starting Scrape (Force Type 1: Individual Solutions) ---")
    
    while True:
 
        current_url = BASE_URL_TEMPLATE.format(start_offset)
        print(f"--- Scraping Page {page_num} (Offset {start_offset}) ---")
        print(f"Loading: {current_url}")
        
        try:
            driver.get(current_url)
            time.sleep(4) 
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            

            wrapper = soup.find('div', class_=re.compile(r'custom__table-wrapper'))
            
            if not wrapper:
                print("Table wrapper not found. Ending.")
                break
                

            rows = wrapper.find_all('tr', attrs={'data-entity-id': True})
            if not rows:

                rows = wrapper.find_all('tr', attrs={'data-course-id': True})
            
            print(f"Found {len(rows)} rows on this page.")
            
            if len(rows) == 0:
                print("No rows found. Reached end of list.")
                break
            
            new_items_count = 0
            for row in rows:
                try:
 
                    title_td = row.find('td', class_='custom__table-heading__title')
                    if not title_td: continue
                    
                    link_tag = title_td.find('a')
                    if not link_tag: continue
                    
                    name = link_tag.get_text(strip=True)
                    url = link_tag['href']
                    
                    if not url.startswith('http'):
                        url = "https://www.shl.com" + url
                    
                    
                    if url not in seen_urls:
                        seen_urls.add(url)
                        all_links.append({"name": name, "url": url})
                        new_items_count += 1
                except Exception as e:
                    continue
            
            print(f"Added {new_items_count} new items. Total collected: {len(all_links)}")

            if new_items_count == 0:
                print("No new items found (potential end of catalog). Stopping.")
                break

            start_offset += items_per_page
            page_num += 1
            

            if page_num > 60:
                print("Safety limit reached.")
                break
                
        except Exception as e:
            print(f"Error on page {page_num}: {e}")
            break

    print(f"\nFinal Count: {len(all_links)} Individual Assessments Found.")
    
 
    print("Starting Deep Scrape (Visiting every link)...")
    final_data = []
    
    for idx, item in enumerate(all_links):
        try:
            driver.get(item['url'])
            
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
           
            desc = "N/A"
            try:
                
                desc_header = soup.find('h4', string=re.compile("Description", re.IGNORECASE))
                if desc_header:
                    
                    desc_p = desc_header.find_next('p')
                    if desc_p: desc = desc_p.get_text(strip=True)
            except: pass
            
            
            test_type = "General"
            try:
                
                type_label = soup.find(string=re.compile("Test Type:"))
                if type_label:
                    
                    key_span = type_label.find_next('span', class_='product-catalogue__key')
                    if key_span:
                        code = key_span.get_text(strip=True)
                       
                        map_types = {'K': 'Knowledge & Skills', 'P': 'Personality & Behavior', 'A': 'Ability', 'S': 'Simulation'}
                        test_type = map_types.get(code, code)
            except: pass

            final_data.append({
                "name": item['name'],
                "url": item['url'],
                "description": desc,
                "test_type": test_type
            })
            
            if idx % 20 == 0:
                print(f"Deep Scraped {idx}/{len(all_links)}: {item['name']}")

        except:
            print(f"Failed to load: {item['url']}")

    driver.quit()
    
    
    df = pd.DataFrame(final_data)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Bhai kaam ho gaya! {len(df)} items saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_shl_direct_url()