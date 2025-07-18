import time
import logging
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

TELEGRAM_TOKEN = "7604446870:AAHpQRJQfMKCPsCt6CG86hPMZtsh24jevts"
CHAT_ID = "719052415"
URLS = [
    "https://inforadar.live/#/dashboard/soccer/live",
    "https://inforadar.live/#/dashboard/basketball/live"
]
CHECK_INTERVAL = 60
ALG_THRESHOLD_POS = 1.00
ALG_THRESHOLD_NEG = -1.00

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        logging.error(f"Telegram Error: {e}")

def start_scraper():
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)

    logging.info("Bot started successfully.")
    send_telegram_message("✅ FotisBot is LIVE on Railway!")

    while True:
        try:
            for url in URLS:
                driver.get(url)
                time.sleep(5)

                rows = driver.find_elements(By.CSS_SELECTOR, "tr")
                for row in rows:
                    try:
                        text = row.text
                        if "Alg.1" in text:
                            alg_value = float(text.split("Alg.1")[-1].strip())
                            if alg_value > ALG_THRESHOLD_POS or alg_value < ALG_THRESHOLD_NEG:
                                match = text.split("\n")[0]
                                send_telegram_message(f"🔥 ALERT\nMatch: {match}\nAlg.1: {alg_value}\nLink: {url}")
                                logging.info(f"Alert sent: {match} - {alg_value}")
                    except:
                        continue

            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            logging.error(f"Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    start_scraper()
