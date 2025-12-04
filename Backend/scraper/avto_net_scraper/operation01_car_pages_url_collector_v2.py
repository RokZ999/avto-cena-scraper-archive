from typing import List

from Backend.scraper.avto_net_scraper.common.common_constants import CAR_PAGES_TXT, OPERATION01_DIR, BASE_URL, \
    SEARCH_MAKES
from Backend.scraper.avto_net_scraper.models.BrandNumberUrl import BrandNumberUrl
from Backend.scraper.utils.curl_imp_proccessor import curl_threading
from Backend.scraper.utils.dir_helper import remove_dir_if_exists_and_create
from Backend.scraper.utils.lxml_processor import extract_multiple_text_from_html_threaded_with_parser, \
    get_files_paths_from_directory, extract_direct_links

# XPATHS
YEAR_NUM_OF_CARS_XPATH = "//div[contains(@class, 'pt-2') and contains(@class, 'text-left') and normalize-space(text())='Letnik 1.registracije']/following-sibling::div[1]//a"

# PATHS
car_pages_txt = CAR_PAGES_TXT
# SYSTEM PATHS
operation01_dir = OPERATION01_DIR


def operation01_car_pages_url_collector_v2() -> List[str]:
    remove_dir_if_exists_and_create(operation01_dir)
    list_of_brands_numbers_url_list = get_all_brands_urls()
    all_pages_url = get_all_cars_pages_urls(list_of_brands_numbers_url_list)
    return all_pages_url


BASE_ADS_URL = BASE_URL + "/Ads"
BRAND_NUM_XPATH = "//a[@class = 'stretched-link font-weight-bold text-decoration-none text-truncate d-block']"


def get_all_brands_urls() -> List[BrandNumberUrl]:
    file_name_url_tuple_singelton_list = [(BASE_URL + SEARCH_MAKES, "search_makes")]
    curl_threading(file_name_url_tuple_singelton_list, operation01_dir)
    files_paths_list_str = get_files_paths_from_directory(operation01_dir)

    hrefs_list = extract_direct_links(files_paths_list_str, BRAND_NUM_XPATH)
    brands_list_str = extract_multiple_text_from_html_threaded_with_parser(files_paths_list_str, [BRAND_NUM_XPATH])[0]

    list_of_brands_numbers_url_list = []
    for i in range(len(hrefs_list)):
        url = BASE_ADS_URL + "/results" + hrefs_list[i][hrefs_list[i].index("."):]

        if "Škoda" in url:
            url = url.replace("Škoda", "%8Akoda")

        cleaned_texts_list_str = str(brands_list_str[i]).strip().replace(")", "").split("(")
        brand_name = cleaned_texts_list_str[0].strip()
        number_of_cars = int(cleaned_texts_list_str[1])

        brand_number_href_obj = BrandNumberUrl(brand_name, number_of_cars, url)
        list_of_brands_numbers_url_list.append(brand_number_href_obj)

    return list_of_brands_numbers_url_list


def get_all_cars_pages_urls(list_of_brands_numbers_urls: List[BrandNumberUrl]) -> List[str]:
    all_pages_cars_urls_str = []

    for brand_number_url_obj in list_of_brands_numbers_urls:
        number_of_cars = brand_number_url_obj.number
        url = brand_number_url_obj.url + "&cenaMin=100&EQ7=1000000120&KAT=1010000000&stran="

        if number_of_cars == 0:
            pass
        elif number_of_cars <= 840:
            all_pages_cars_urls_str.extend(get_all_pages_links(url, number_of_cars))
        else:
            all_pages_cars_urls_str.extend(collect_all_pages_over_840_cars(url, brand_number_url_obj.brand))

    return all_pages_cars_urls_str


def collect_all_pages_over_840_cars(car_brand_url: str, name_of_brand) -> List[str]:
    file_name_url_tuple_singelton_list = [(car_brand_url, "temp")]
    curl_threading(file_name_url_tuple_singelton_list, operation01_dir)
    files_paths_list_str = [operation01_dir + "/temp.html"]
    years_list_str = \
        extract_multiple_text_from_html_threaded_with_parser(files_paths_list_str, [YEAR_NUM_OF_CARS_XPATH])[0]

    all_over_840 = []

    for year_num_str in years_list_str:
        if "novo" in year_num_str:
            num_of_cars = year_num_str.split()[-1]
            all_over_840.extend(get_all_pages_links(car_brand_url + "&subSTAR=301", int(num_of_cars)))
        elif "1995" in year_num_str:
            num_of_cars = year_num_str.split("starejši")[1]
            all_over_840.extend(
                get_all_pages_links(car_brand_url + "&subletnikMIN=0&subletnikMAX=1995", int(num_of_cars)))
        else:
            year = year_num_str[0:4]
            num_of_cars = year_num_str.replace(year, "")
            all_over_840.extend(
                get_all_pages_links(car_brand_url + f"&subletnikMIN={year}&subletnikMAX={year}", int(num_of_cars)))
    return all_over_840


def get_all_pages_links(base_brand_url, number_of_cars) -> List[str]:
    if number_of_cars <= 48:
        return [base_brand_url]
    else:
        all_pages_links = []
        number_of_pages = number_of_cars // 48 + 1

        for page_counter in range(1, number_of_pages + 1):
            page_url = []
            if "stran=1" in base_brand_url:
                page_url = base_brand_url.replace("stran=1", f"stran={page_counter}")
            elif "stran=" in base_brand_url:
                page_url = base_brand_url.replace("stran=", f"stran={page_counter}")
            all_pages_links.append(page_url)

        return all_pages_links


def clear_avto_net_url(url):
    params_to_remove = ['model', 'modelID', 'tip', 'znamka2', 'model2', 'tip2', 'znamka3', 'model3', 'tip3', 'cenaMax',
                        'letnikMin', 'letnikMax', 'bencin', 'starost2', 'oblika', 'ccmMin', 'ccmMax', 'mocMin',
                        'mocMax', 'kmMin', 'kmMax', 'kwMin', 'kwMax', 'motortakt', 'motorvalji', 'lokacija', 'sirina',
                        'dolzina', 'dolzinaMIN', 'dolzinaMAX', 'nosilnostMIN', 'nosilnostMAX', 'lezisc', 'presek',
                        'premer', 'col', 'vijakov', 'EToznaka', 'vozilo', 'airbag', 'barva', 'barvaint', 'doseg', 'EQ1',
                        'EQ2', 'EQ3', 'EQ4', 'EQ5', 'EQ6', 'EQ8', 'EQ9', 'PIA', 'PIAzero', 'PIAOut', 'PSLO', 'akcija',
                        'paketgarancije', 'broker', 'prikazkategorije', 'kategorija', 'ONLvid', 'ONLnak', 'zaloga',
                        'arhiv', 'presort', 'tipsort']
    all_params_in_url_original = url.split("&")
    all_params_in_url = all_params_in_url_original.copy()

    for param in all_params_in_url_original:
        if param.split("=")[0] in params_to_remove:
            all_params_in_url.remove(param)
    return "&".join(all_params_in_url)
