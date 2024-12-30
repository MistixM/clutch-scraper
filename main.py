import time
import pandas as pd
import csv

from DrissionPage import ChromiumPage
from bs4 import BeautifulSoup

def main():
    # Prepare Chromium object
    driver = ChromiumPage()
    
    with open('data.csv', 'w', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        writer.writerow(['Company', 'URL', 'Team size', 'Hourly Rate'])

        for number in range(5):

            # Get current page
            driver.get(f'https://clutch.co/us/web-designers?agency_size=10+-+49&page={number}&related_services=field_pp_sl_ecommerce&related_services=field_pp_sl_app_interface_design')
            
            # Save html file locally
            page_html = driver.html
            with open(f'page_{number}.html', 'w', encoding='utf-8') as file:
                file.write(page_html)

            # Wait a bit
            time.sleep(0.5)

            # Open html file in soup
            with open(f'page_{number}.html', 'r', encoding='utf-8') as file:
                content = file.read()

            soup = BeautifulSoup(content, 'html.parser')

            agencies = soup.find_all(class_='row')
            
            for agency in agencies:
                company_name_el = agency.find(class_='company_info')
                if company_name_el:
                    if "profile" in company_name_el.a['href']:
                        company_url = f"https://clutch.co/{company_name_el.a['href']}".strip()
                    else:
                        # print(company_name_el)
                        company_url = company_name_el.a['href']

                    company_name = company_name_el.a.text.strip()

                else:
                    continue
                
                try:
                    size = agency.find('div', attrs={'data-content': "<i>Employees</i>"}).text.strip()
                    hourly_rate = agency.find('div', attrs={'data-content': "<i>Avg. hourly rate</i>"}).text.strip()
                
                except Exception:
                    pass
                    
                writer.writerow([company_name, f"{company_url}", size, hourly_rate])

            else:
                pass

    # At the end filter csv file
    remove_duplicates('data.csv')

    driver.quit()

def remove_duplicates(input_file):
    df = pd.read_csv(input_file)
    
    # Remove duplicates
    df.drop_duplicates(inplace=True, subset=['Company'])

    # Write new csv (just replace old)
    df.to_csv(input_file, index=False)

if __name__ == "__main__":
    main()