from requests_html import HTMLSession
from datetime import datetime, timezone
import re

SESSION = HTMLSession()

all_page_links = []
all_service_links = []
all_services = []

def generate_page_links() -> None:
    """
    This function generate the page URLs that are used to scrape service links
    """
    
    root_url = "https://www.cleanaway.com.au/contact-us/our-locations/"
    response = SESSION.get(root_url)
    
    total_pages = int(response.html.find("div.location-pagination ul li a.\?", first=True).text)
    
    for pgno in range(1, total_pages+1):
        page_url = f'https://www.cleanaway.com.au/contact-us/our-locations/?pg={pgno}'
        all_page_links.append(page_url)
    return

def scrape_service_links(page_url: str) -> None:
    """
    This function fetches the service URLs from the page and adds them to the 'all_service_links' list
    Args: 
        page_url (str): page URL string
    Returns:
        None: This function returns nothing but adds the data to the 'all_books' list
    """
    
    print(f'Collecting service links from: {page_url}')
    
    response = SESSION.get(page_url)
    
    content_blocks = response.html.find("div.white-box.location-output__box>a")
    
    for service in content_blocks:
        service_url =  service.attrs.get("href")
        all_service_links.append(service_url)
    return

def scrape_service_details(service_url: str) -> None:
    """
    This function takes a service URL; scrapes all the required details and adds them to the 'all_services' list
    Args:
        service_url (str): Service URL string
    Returns:
        None: It returns nothing but, adds the scraped service details to the 'all_services' list
    """
    
    print(f'Scraping details from: {service_url}')
    
    utc_timezone = timezone.utc
    current_utc_timestamp = datetime.now(utc_timezone).strftime('%d-%b-%Y %H:%M:%S')
    
    response = SESSION.get(service_url)
    
    service_name = response.html.find("nav#breadcrumbs li:last-child", first=True).text.strip()
    address = response.html.find("div.location-box div.info-block p a", first=True).text.strip()
    
    location_url = response.html.find("div.location-box div.info-block p a", first=True).attrs.get('href')
    
    lat_long_pattern = re.compile(r'.*\?q=(.*)\,(.*)')
    lat_long_matches = lat_long_pattern.match(location_url)
    
    latitude = lat_long_matches.group(1)
    longitude = lat_long_matches.group(2)
    
    if response.html.find("div.location-box div.info-block:last-child div.info-block__title", first=True).text.strip() == "Services offered":
        service_types = response.html.find("div.location-box div.info-block:last-child p", first=True).text.strip()
    else:
        service_types = "Miscellaneous"
    
    try:
        service_description = response.html.find("div.about-us p", first=True).text.strip()
    except:
        service_description = None
    
    service_details = {
        "service_name": service_name,
        "address": address,
        "latitude": latitude,
        "longitude": longitude,
        "service_types": service_types,
        "service_description": service_description,
        "last_updated_at_UTC": current_utc_timestamp
    }
    
    all_services.append(service_details)
    return

# Testing the scraper template #
# ---------------------------- #

if __name__ == '__main__':
    
    generate_page_links()
    
    print('\n')
    print(f'Total pages to scrape: {len(all_page_links)}')
    print('\n')
    print(all_page_links)
    
    page_url = 'https://www.cleanaway.com.au/contact-us/our-locations/?pg=21'
    scrape_service_links(page_url)
    
    print('\n')
    print(all_service_links)
    print('\n')
    print(f'Total services available: {len(all_service_links)}')
    
    service_url = 'https://www.cleanaway.com.au/location/sunshine-west/'
    scrape_service_details(service_url)
    
    print('\n')
    print(all_services)