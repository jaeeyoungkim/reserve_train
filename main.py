import time
# import winsound as sd
from korail2 import *
from datetime import datetime
from SRT import SRT


# def beepsound():
#     fr = 2500  # range : 37 ~ 32767
#     du = 30000  # 1000 ms ==1second
#     sd.Beep(fr, du)  # winsound.Beep(frequency, duration)
def send_telegram_message(reservation):
    bot_token = "6794329002:AAEiWc8Ji5dN3-X2kU_W7qJJBTD_jQRVWPY"
    chat_id = "-4014888163"
    text = f"예약성공 10분 안에 예매해야함:{reservation}"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, data=data)
    return response.json()
def reserve_ktx():
    KORAIL_ID = '1463203706'
    KORAIL_PW = 'ahfmsek2!'

    PUSHOVER_APP_TOKEN = 'APP_TOKEN'
    PUSHOVER_USER_TOKEN = 'USER_TOKEN'

    DEP = '부산'
    ARV = '서울'
    DEP_DATE = '20240212'
    DEP_TIME = '080000'
    LIMIT_DEP_TIME_STRING = '100000'
    LIMIT_DEP_TIME_DATETIME = datetime.strptime(LIMIT_DEP_TIME_STRING, "%H%M%S")
    PSGRS = [AdultPassenger(1)]
    TRAIN_TYPE = TrainType.KTX

    k = Korail(KORAIL_ID, KORAIL_PW, auto_login=False)
    if not k.login():
        print("login fail")

    is_continue = True
    while is_continue:
        try:
            trains = k.search_train(DEP, ARV, DEP_DATE, DEP_TIME, passengers=PSGRS, train_type=TRAIN_TYPE)
            print(f"train_list:{trains}")
            if len(trains) > 0:
                for idx, train in enumerate(trains):

                    DEP_TIME_DATETIME = datetime.strptime(train.dep_time, "%H%M%S")
                    if DEP_TIME_DATETIME <= LIMIT_DEP_TIME_DATETIME:
                        k.reserve(trains[idx], passengers=PSGRS)
                        message = f"예약성공- 기차시간:{train.dep_time}//{datetime.now()}"
                        print(message)
                        send_telegram_message(message)
                        is_continue = False
                    else:
                        print(f"예약안함- 기차시간 초과:{train.dep_time}//{datetime.now()}")
                    if not is_continue:
                        pass
                        # beepsound()
            # time.sleep(0.1)
        except Exception as e:
            if "No Results" in str(e):
                print(f"No Results//{datetime.now().time()},{e}")
                continue
            if "잔여석없음" in str(e):
                print(f"잔여석없음//{datetime.now().time()}")
                time.sleep(0.1)
                continue
            k.login()
            print(f"로그인 다시 시도 error:{e}")
            continue


def reserve_srt():
    srt = SRT("010-2366-0150", "Eos5k907!@")
    dep = '평택지제'
    arr = '울산(통도사)'
    date = '20231126'
    start_time = '170000'
    time_limit = '170500'

    is_continue = True
    if srt.is_login:
        while is_continue:
            try:
                trains = srt.search_train(dep, arr, date, start_time,
                                          time_limit
                                          )
                print(f"train_list:{trains}")
                if len(trains) > 0:
                    for idx, train in enumerate(trains):
                        reservation = srt.reserve(trains[idx])
                        print(f"예약성공:{reservation}")
                        send_telegram_message(reservation)
                        is_continue = False
                        with open(file="reserve.log", mode="a+") as f:
                            f.write(f"{reservation}//{datetime.now()}")
                time.sleep(0.5)
            except Exception as e:
                print(f"로그인 다시 시도 error:{e}")
                srt = SRT("010-2366-0150", "Eos5k907!@")
                continue

if __name__ == "__main__":
    reserve_ktx()