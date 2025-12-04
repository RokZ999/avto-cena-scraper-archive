import asyncio
import random
from typing import List, Dict, Callable

from selenium_driverless import webdriver

from Backend.logger.log_config import log
from Backend.scraper.avto_net_scraper.common.common_constants import UBLOCK_CRX_PATH


async def process_links(driver, links: List[str], stats: Dict[str, int], path_to_save_htmls: str,
                        process_callback: Callable) -> None:
    """Process links with the given WebDriver instance using a specified callback function."""
    for page_link in links:
        try:
            await driver.get(page_link)

            page_source = await driver.page_source
            filename = process_callback(page_link)
            full_path = f"{path_to_save_htmls}/{filename}.html"
            with open(full_path, 'w', encoding='utf-8') as file:
                file.write(page_source)

            log.info(f"Saved successfully {page_link}")
            stats['processed'] += 1
        except UnicodeEncodeError as e:
            log.error(f"Unicode encoding error for {page_link}: {e}")
            stats['encoding_errors'] += 1
        except Exception as e:
            log.error(f"General error scraping {page_link}: {e}")
            stats['errors'] += 1


def default_callback(_):
    return random.randint(1000, 9999999)


async def collect_any_raw_htmls(driver, list_of_urls: List[str], num_of_windows: int, path_to_save_htmls: str,
                                process_callback: Callable = default_callback) -> None:
    log.info("Starting to collect raw HTMLs.")
    stats = {'processed': 0, 'errors': 0}

    num_windows = num_of_windows
    urls_per_window, remainder = divmod(len(list_of_urls), num_windows)

    targets = [await driver.new_window("tab", activate=False) for _ in range(num_windows)]
    tasks = []

    start_index = 0
    for i, target in enumerate(targets):
        extra = 1 if i < remainder else 0
        end_index = start_index + urls_per_window + extra
        window_urls = list_of_urls[start_index:end_index]
        tasks.append(process_links(target, window_urls, stats, path_to_save_htmls, process_callback))
        start_index = end_index

    await asyncio.gather(*tasks)

    log.info(f"Pages processed: {stats['processed']}, Errors: {stats['errors']}")
