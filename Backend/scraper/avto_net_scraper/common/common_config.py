from selenium_driverless import webdriver
from Backend.scraper.avto_net_scraper.common.common_constants import UBLOCK_CRX_PATH

def production_options_driver():
    options = webdriver.ChromeOptions()
    options.add_extension(UBLOCK_CRX_PATH)
    options.add_argument("--disable-gpu")
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-search-engine-choice-screen")
    options.add_argument("--disable-domain-reliability")
    options.add_argument("--disable-crash-reporter")
    options.add_argument("--disable-breakpad")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-session-crashed-bubble")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-multilingual-spellchecker")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--disable-device-discovery-notifications")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-component-extensions-with-background-pages")
    options.add_argument("--password-store=basic")
    options.add_argument("--metrics-recording-only")
    options.add_argument("--disable-speech-api")
    options.add_argument("--disable-fetching-hints-at-navigation-start")
    options.add_argument("--disable-component-update")
    options.add_argument("--disable-component-updater=2")
    options.add_experimental_option(
        "prefs", {
            # block image loading
            "profile.managed_default_content_settings.images": 2,
            # 'profile.managed_default_content_settings.javascript': 2
        }
    )
    options.headless = True
    return options

def dev_options_driver():
    options = webdriver.ChromeOptions()
    #options.add_extension(UBLOCK_CRX_PATH)
    options.add_argument("--disable-gpu")
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_experimental_option(
        "prefs", {
            # block image loading
            "profile.managed_default_content_settings.images": 2,
            # 'profile.managed_default_content_settings.javascript': 2
        }
    )
    return options

def get_options_driver(options_type: str) -> webdriver.ChromeOptions:
    if options_type == "prod":
        return production_options_driver()
    elif options_type == "dev":
        return dev_options_driver()
    else:
        raise Exception("Invalid options type")









