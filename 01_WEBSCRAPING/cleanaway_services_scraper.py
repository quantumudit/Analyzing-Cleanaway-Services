import pandas as pd
import pyfiglet
from concurrent.futures import ThreadPoolExecutor
from fx_cleanaway_services_scraper_template import *

def extract_all_service_links() -> None:
    """
    This function loops though each of the page and scrapes all the different service links
    """
        
    with ThreadPoolExecutor() as executor:
        executor.map(scrape_service_links, all_page_links)
    return

def scrape_all_service_details() -> None:
    """
    This function loops through all the individual service links and scrapes the details; that are get added to 'all_services' list
    """
    
    with ThreadPoolExecutor() as executor:
        executor.map(scrape_service_details, all_service_links)
    return

def load_data() -> None:
    """
    This function loads the scraped data into a CSV file
    """
    
    services_df = pd.DataFrame(all_services)
    services_df.to_csv('cleanaway_services_raw_data.csv', encoding="utf-8", index=False)
    return

if __name__ == '__main__':
    
    scraper_title = "CLEANAWAY SERVICES SCRAPER"
    ascii_art_title = pyfiglet.figlet_format(scraper_title, font='small')
    
    start_time = datetime.now()
    
    print('\n\n')
    print(ascii_art_title)
    print('Collecting Cleanaway Services...')
    
    generate_page_links()
    
    print(f'Total Pages to scrape: {len(all_page_links)}')
    print('Gathering all service links to scrape...')
    
    extract_all_service_links()
    
    print(f'Total services to scrape: {len(all_service_links)}')
    print('\n')
    print('Scraping service details from each service link...')
    
    scrape_all_service_details()
    
    end_time = datetime.now()
    scraping_time = end_time - start_time
    
    print('\n')
    print('All Services Scraped...')
    print(f'Time spent on scraping: {scraping_time}')
    print(f'Total services scraped: {len(all_services)}')
    print('\n')
    print('Loading data into CSV...')
    
    load_data()
    
    print('Data Exported to CSV...')
    print('Webscraping Completed !!!')