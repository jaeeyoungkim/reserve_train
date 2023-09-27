import time
import winsound as sd
from korail2 import *
from datetime import datetime
from SRT import SRT


def beepsound():
    fr = 2500  # range : 37 ~ 32767
    du = 30000  # 1000 ms ==1second
    sd.Beep(fr, du)  # winsound.Beep(frequency, duration)

def reserve_ktx():
    KORAIL_ID = '1463203706'
    KORAIL_PW = 'ahfmsek2!'

    PUSHOVER_APP_TOKEN = 'APP_TOKEN'
    PUSHOVER_USER_TOKEN = 'USER_TOKEN'

    DEP = '부산'
    ARV = '서울'
    DEP_DATE = '20231003'
    DEP_TIME = '143000'
    LIMIT_DEP_TIME_STRING = '160000'
    LIMIT_DEP_TIME_DATETIME = datetime.strptime(LIMIT_DEP_TIME_STRING, "%H%M%S")
    PSGRS = [AdultPassenger(1)]
    TRAIN_TYPE = TrainType.KTX

    k = Korail(KORAIL_ID, KORAIL_PW, auto_login=False)
    if not k.login():
        print("login fail")

    is_continue = True
    while is_continue:
        try:
            trains = k.search_train_allday(DEP, ARV, DEP_DATE, DEP_TIME, passengers=PSGRS, train_type=TRAIN_TYPE)
            print(f"train_list:{trains}")
            if len(trains) > 0:
                for idx, train in enumerate(trains):

                    DEP_TIME_DATETIME = datetime.strptime(train.dep_time, "%H%M%S")
                    if DEP_TIME_DATETIME <= LIMIT_DEP_TIME_DATETIME:
                        k.reserve(trains[idx], passengers=PSGRS)
                        print(f"예약성공- 기차시간:{train.dep_time}//{datetime.now()}")
                        is_continue = False
                    else:
                        print(f"예약안함- 기차시간 초과:{train.dep_time}//{datetime.now()}")
                    if not is_continue:
                        beepsound()
        except Exception as e:
            if "No Results" in str(e):
                print(f"No Results//{datetime.now().time()}")
                continue
            if "잔여석없음" in str(e):
                print(f"잔여석없음//{datetime.now().time()}")
                continue
            k.login()
            print(f"로그인 다시 시도 error:{e}")
            continue


def reserve_srt():
    srt = SRT("010-2442-6349", "Ahfmsek9413!")
    dep = '수서'
    arr = '부산'
    date = '20230928'
    start_time = '080000'
    time_limit = '180000'

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
                        beepsound()
                        is_continue = False
                        with open(file="reserve.log", mode="a+") as f:
                            f.write(f"{reservation}//{datetime.now()}")
                time.sleep(0.1)
            except Exception as e:
                print(f"로그인 다시 시도 error:{e}")
                srt = SRT("010-2442-6349", "Ahfmsek9413!")
                continue

if __name__ == "__main__":
    reserve_ktx()