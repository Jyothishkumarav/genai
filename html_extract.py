import requests
from bs4 import BeautifulSoup
import json

from llm_test import generate_stock_data, generate_stock_valuation
from telegram_msg_publisher import send_message


def scrape_page(url, tag, **identifiers):
    """
    Scrape a webpage and extract content based on the given element and identifiers.

    Args:
        url (str): The URL of the webpage to scrape.
        tag (str): The HTML tag to target (e.g., 'div', 'p', 'span').
        identifiers (dict): Additional attributes to filter elements (e.g., class_='example-class').

    Returns:
        str: Extracted content as a JSON string with proper spacing.
    """
    try:
        # Fetch the webpage
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all elements matching the given tag and identifiers
        elements = soup.find_all(tag, **identifiers)

        # Extract and clean text from the elements, preserving spaces
        extracted_data = []
        for element in elements:
            # Join child elements' text with spaces for better readability
            text = " ".join(child.strip() for child in element.stripped_strings)
            extracted_data.append(text)

        # Convert the extracted data to JSON with proper Unicode handling
        json_data = json.dumps(extracted_data, ensure_ascii=False, indent=4)
        return json_data

    except Exception as e:
        print(f"Error occurred: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Example URL
    url = "https://www.screener.in/company/KPITTECH/"  # Replace with your target URL

    # Scrape elements with tag 'div' and class 'company-ratios'
    # results = scrape_page(url, "div", class_="company-ratios")
    results = scrape_page(url, "div", class_="card card-large")

    # print(results)
    response = generate_stock_data(f'''  {results}  ''')
    # print(response)
    response = generate_stock_valuation(f'''{response}''')
    print(response)
    send_message(response)

    # # Save results to a file
    # with open("scraped_data.json", "w") as file:
    #     file.write(results)
