import asyncio

from selenium_driverless.types.by import By
from selenium_driverless.types.webelement import WebElement, NoSuchElementException

from Backend.logger.log_config import log

# XPATHS
ANY_BUTTON_TEMPLATE_XPATH = "//*[text()='{}']"
ANY_BUTTON_TEMPLATE_WITH_INDEX_XPATH = "(//*[text()='{}'])[{}]"

# TIMEOUTS CONSTANTS
TIMEOUT = 10
MEDIUM_SLEEP = 1

async def get_elements_with_xpath_async(driver, element_xpath: str):
    """
    Waits for an element to be present in the DOM identified by its XPath and returns it.
    """
    try:
        elements = await driver.find_elements(By.XPATH, element_xpath)
        return elements
    except:
        log.error(f"Could not find element with XPath: {element_xpath}")
        return None

async def solve_cloudflare_async(driver) -> None:
    if 'Just' in await driver.title:
        log.info("CF check")
        try:
            web_element: WebElement = await driver.find_element(By.XPATH, '//iframe[starts-with(@src, "https://challenges.cloudflare.com/cdn-cgi/challenge-platform/")]', timeout=0)
            await asyncio.sleep(0.1)
            if not await web_element.is_displayed():
                return None
            iframe_document: WebElement = await web_element.content_document
            try:
                web_element2: WebElement = await iframe_document.find_element(By.XPATH, '//*[@id="success"]', timeout=0)
                await asyncio.sleep(0.1)
                if await web_element2.is_displayed():
                    return None
            except Exception:
                pass
            try:
                web_element2: WebElement = await iframe_document.find_element(By.XPATH, '//div[@id="challenge-overlay"]/a[@onclick="window.location.reload(true);"]', timeout=0)
                await asyncio.sleep(0.1)
                if await web_element2.is_displayed():
                    await driver.refresh()
                    await asyncio.sleep(0.1)
                    return None
            except Exception:
                pass
            try:
                web_element2: WebElement = await iframe_document.find_element(By.XPATH, '//*[@type="checkbox"]', timeout=0)
                await asyncio.sleep(0.1)
                if await web_element2.is_displayed():
                    await web_element2.click()
            except NoSuchElementException:
                pass
            await asyncio.sleep(0.1)
        except Exception:
            pass