import glob
import os
from typing import List

from lxml import etree
from lxml import html as lxml_html
from lxml.html import HTMLParser

from Backend.logger.log_config import log
from Backend.scraper.avto_net_scraper.common.common_constants import ENCODING_WINDOWS_1250
from concurrent.futures import ThreadPoolExecutor, as_completed

def parse_html_with_xpath(content: str, xpath: str) -> List[str]:
    """
    Parse HTML content with XPath to extract attributes from specific elements.

    :param content: The HTML content as a string.
    :param xpath: The XPath query to select elements.
    :return: A list of extracted attributes (e.g., hrefs) from the elements.
    """
    try:
        tree = etree.HTML(content)
        extracted_elements = tree.xpath(xpath)
        log.info(f"Successfully parsed HTML content with XPath: {xpath}")
        return extracted_elements
    except Exception as e:
        log.error(f"Error parsing HTML content with XPath {xpath}: {e}")
        return []


def extract_direct_links(filenames: List[str], xpath: str) -> List[str]:
    """
    Extract direct links from a list of HTML files using a specified XPath.

    :param filenames: A list of paths to HTML files.
    :param xpath: The XPath query to select <a> elements and extract href attributes.
    :return: A list of extracted hrefs as strings.
    """
    hrefs = []
    for index, filename in enumerate(filenames, start=1):
        try:
            with open(filename, 'r', encoding=ENCODING_WINDOWS_1250) as file:
                content = file.read()
                # Parse HTML content to get elements
                elements = parse_html_with_xpath(content, xpath)
                # Extract href attribute from each element and add to the list
                for element in elements:
                    # Ensure element is an <a> tag and has an href attribute
                    if element.tag == 'a' and 'href' in element.attrib:
                        hrefs.append(element.attrib['href'])
                log.info(f"Extracted {len(hrefs)} hrefs from {filename}")
        except Exception as e:
            log.error(f"Error parsing {filename}: {e}")

    log.info(f"Total extracted hrefs: {len(hrefs)}")
    return hrefs


def extract_text_from_html(filenames: List[str], xpath: str) -> List[str]:
    """
    Extract text content from elements in a list of HTML files using a specified XPath.

    :param filenames: A list of paths to HTML files.
    :param xpath: The XPath query to select elements from which text will be extracted.
    :return: A list of extracted text content as strings.
    """
    extract_multiple_text_from_html_threaded_with_parser(filenames, [xpath])

def extract_text_from_html_with_own_parser(filename, xpaths):
    """
    Extract text from an HTML file using specified XPaths. This function is designed
    to be called within a ThreadPoolExecutor.
    """
    extracted_texts = []
    try:
        parser = HTMLParser()  # Create a new parser instance for each task
        with open(filename, 'r', encoding=ENCODING_WINDOWS_1250, errors='replace') as file:
            content = file.read()
        tree = lxml_html.fromstring(content, parser=parser)
        for xpath in xpaths:
            elements = tree.xpath(xpath)
            for element in elements:
                text = element.text_content().strip()
                if text:
                    extracted_texts.append(text)
        log.info(f"Processed file: {filename}")
    except Exception as e:
        log.error(f"Error parsing {filename}: {e}")
    return extracted_texts


def extract_multiple_text_from_html_threaded_with_parser(filenames, xpaths, append_filename=False):
    """
    Extract text content using specified XPaths, using a ThreadPoolExecutor for better
    thread management and resource control.
    """
    all_extracted_texts = []
    num_of_workers = int(os.getenv("THREAD_COUNT"))
    with ThreadPoolExecutor(max_workers=num_of_workers) as executor:
        future_to_filename = {executor.submit(extract_text_from_html_with_own_parser, filename, xpaths): filename for
                              filename in filenames}
        for future in as_completed(future_to_filename):
            filename = future_to_filename[future]
            try:
                result = future.result()
                if result and append_filename:
                    result.append(filename)
                if result:
                    all_extracted_texts.append(result)
            except Exception as exc:
                log.error(f'File {filename} generated an exception: {exc}')
    log.info(f"Total extracted texts: {len(all_extracted_texts)}")
    return all_extracted_texts


# TODO: Reaserch if non v2 version is needed
def extract_multiple_text_from_html_threaded_with_parser_v2(filenames, xpaths, append_filename=False):
    """
    Extract text content using specified XPaths, using a ThreadPoolExecutor for better
    thread management and resource control.
    """
    all_extracted_texts = []
    num_of_workers = int(os.getenv("THREAD_COUNT"))
    with ThreadPoolExecutor(max_workers=num_of_workers) as executor:
        future_to_filename = {executor.submit(extract_text_from_html_with_own_parser_v2, filename, xpaths): filename for
                              filename in filenames}
        for future in as_completed(future_to_filename):
            filename = future_to_filename[future]
            try:
                result = future.result()
                if result and append_filename:
                    result.append(filename)
                if result:
                    all_extracted_texts.append(result)
            except Exception as exc:
                log.error(f'File {filename} generated an exception: {exc}')
    log.info(f"Total extracted texts: {len(all_extracted_texts)}")
    return all_extracted_texts

def extract_text_from_html_with_own_parser_v2(filename, xpaths):
    """
    Extract text from an HTML file using specified XPaths. This function is designed
    to be called within a ThreadPoolExecutor.
    """
    extracted_texts = []
    try:
        parser = HTMLParser()  # Create a new parser instance for each task
        with open(filename, 'r', encoding=ENCODING_WINDOWS_1250, errors='replace') as file:
            content = file.read()
        tree = lxml_html.fromstring(content, parser=parser)
        for xpath in xpaths:
            elements = tree.xpath(xpath)
            if elements:
                for element in elements:
                    text = element.text_content().strip()
                    if text:
                        extracted_texts.append(text)
                    else:
                        extracted_texts.append('')
            else:
                extracted_texts.append('')

        log.info(f"Processed file: {filename}")
    except Exception as e:
        log.error(f"Error parsing {filename}: {e}")
    return extracted_texts



def get_files_paths_from_directory(directory_path: str, pattern: str = '*.html') -> List[str]:
    """
    Retrieve file paths matching a given pattern within a directory.

    :rtype: object
    :param directory_path: The path to the directory containing the files.
    :param pattern: The glob pattern to match files. Defaults to '*.html'.
    :return: A list of matching file paths.
    """
    search_path = f"{directory_path}/{pattern}"
    file_paths = glob.glob(search_path)
    log.info(f"Found {len(file_paths)} files in {directory_path} matching pattern '{pattern}'")
    return file_paths
