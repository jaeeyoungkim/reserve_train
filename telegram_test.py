import requests

def send_telegram_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, data=data)
    return response.json()

bot_token = "6794329002:AAEiWc8Ji5dN3-X2kU_W7qJJBTD_jQRVWPY"
chat_id = "-4014888163"
text = "예약성공 10분 안에 예매해야함"

response = send_telegram_message(bot_token, chat_id, text)
print(response)
