import requests
import time

from html_extract import scrape_page
from llm_test import generate_stock_data, generate_stock_valuation

telegram_token = '1912863077:AAGH-iVztSPAw5K117Us-GKEx9pj-j3GUzw'
telegram_chat_id = '-586722077'
URL = f"https://api.telegram.org/bot{telegram_token}/"


def send_message(chat_id, text):
    """Send a message to a Telegram chat."""
    url = URL + "sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    print(f"Message sent: {response.json()}")


def get_updates(offset=None):
    """Fetch updates from the Telegram bot."""
    url = URL + "getUpdates"
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params)
    return response.json()


def respond_to_messages():
    """Continuously fetch and respond to incoming messages."""
    last_update_id = None

    while True:
        updates = get_updates(offset=last_update_id)
        print('msg received :', updates)

        if "result" in updates:
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1
                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    message_text = update["message"].get("text", "")

                    print(f"Received message: {message_text} from chat ID: {chat_id}")

                    # Respond to the received message
                    if message_text.lower() == "hello":
                        send_message(chat_id, "Hi there! How can I help you? Please share me the Stock Symbol")
                    elif message_text.lower() != "exit":
                        url = f"https://www.screener.in/company/{message_text.upper()}/"  # Replace with your target URL
                        print('stock url :', url)
                        # Scrape elements with tag 'div' and class 'company-ratios'
                        # results = scrape_page(url, "div", class_="company-ratios")
                        results = scrape_page(url, "div", class_="card card-large")
                        if results:
                            # print(results)
                            response = generate_stock_data(f'''  {results}  ''')
                            # print(response)
                            response = generate_stock_valuation(f'''{response}''')
                            print(response)
                            send_message(chat_id, response)
                        else:
                            send_message(chat_id,f'Sorry Unable to fetch stock details for  {message_text} ')
                    else:
                        send_message(chat_id, 'Please provide a valid stock symbol')

        time.sleep(1)  # Avoid hitting the API rate limit


if __name__ == "__main__":
    print("Bot is running...")
    respond_to_messages()
