from dotenv import load_dotenv

from Backend.scraper.avto_net_scraper.avto_net_scraper import avto_net_scraper
from Backend.scraper.dober_avto_scraper.dober_avto_scraper import dober_avto_scraper
from Backend.scraper.utils.decorators import time_it


@time_it
def main() -> None:
    """Main entry point for the car scraping application."""
    load_dotenv()
    avto_net_scraper()
    dober_avto_scraper()


if __name__ == '__main__':
    main()
