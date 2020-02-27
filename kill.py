from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException

from time import sleep
from random import randint
from bypass import bypass
from js_functions import *
from threading import Thread


class crims_hitman():
    
    def __init__(self, login, password):
        self.login = login
        self.password = password
        # PROXY = "186.227.213.234:8080" # IP:PORT or HOST:PORT
        # chrome_options.add_argument('--proxy-server=http://%s' % PROXY)
        self.browser = webdriver.Chrome("D:\crims\chromedriver.exe")
        self.browser.get("https://www.thecrims.com/")

        self.killers = {}
        self.killed_people = []
        self.x_request = None
        self.club = None

    def log_in(self):
        login = self.browser.execute_script(js_request_login, self.login, self.password)
        sleep(3)
        self.alert_catcher("x_req")
        
    
    def clubs(self):
        all_clubs = self.browser.execute_script(js_get_clubs, self.x_request)
        sleep(2)
        self.alert_catcher("club")
        self.change_logs("/nightlife", "enter", self.club)
        self.kill_people()
    
    def alert_catcher(self, var):
        alert = self.browser.switch_to.alert
        if var == "x_req":
            self.x_request = alert.text
        elif var == "club":
            self.club = alert.text
        else:
            print("Wrong value provided")
        alert.accept()
        

    def change_logs(self, route, action, arguments, *args):
        from json import dumps
        self.route = route
        self.action = action
        self.arguments = arguments
        Bypass = bypass(self.route)
        Logs = Bypass.logs_bypass(self.action, self.arguments)
        post_route = ""
        move = ""
        restore_hp = False
        if True in args:
            self.action = "enter"
        else:
            if self.action == "exit":
                post_route = "https://www.thecrims.com/api/v1/nightclub/exit"
                move = ""
            elif self.action == "normal":
                post_route = "https://www.thecrims.com/api/v1/input"
                move = ""
            elif self.action == "kill":
                post_route = "https://www.thecrims.com/api/v1/attack"
                move = ""
            elif self.action == "enter":
                post_route = "https://www.thecrims.com/api/v1/nightclub"
                move = "https://www.thecrims.com/newspaper#/nightlife/nightclub"

        #// sends the request to server
        self.browser.execute_script(js_main_requests_pattern, dumps(Logs), post_route, self.x_request, move)
        
    def thread_logs(self, route, action, arguments, *args):
        self.route = route
        self.action = action
        self.arguments = arguments
        
        thread = Thread(target=self.change_logs, args=[self.route,self.action, self.arguments])
        thread.daemon = True
        thread.start()
        thread.join()

    def get_killers(self):
        url = requests.get("https://www.thecrims.com/stats/killers#/").text #/// scrap people(hitman) from top list
        soup = BeautifulSoup(url, "lxml")

        table = soup.find("table", class_="black_table")
        nicks = table.find_all("span", class_="nicktext")
        kills = table.find_all("td", valign="middle")
        for n,k in zip(nicks,kills):
            self.killers.update({n.text:k.text})
        print("done")
                           
    def kill_people(self):
        from json import loads
        self.change_logs("/nightlife", "normal", "")
        people_to_avoid = ["Hitman","Padrino","Kingpin", "Godfather", "Top executive", "Mobster", "Desperado",  "Director", "Consigliere"]
        try:
            self.current_stamina = self.browser.find_element_by_xpath('//div[@class="text-center"]//div[@id="nightclub-singleassault-attack-18"]//div[@class="default-1CS8SFNfrzFfM38mxoY6af_0"]').value_of_css_property("width")
            self.percent_stamina = round(100*float(self.current_stamina[:-2])/128)
            exit_but = WebDriverWait(self.browser, 15).until(EC.presence_of_element_located((By.XPATH,"//div[@id='page']//div[@id='content']//table[@id='content_table']//tbody//tr//td//div[@id='content_middle']//div[@class='content_style main-content ']//div[3]//div//button[@class='btn btn-inverse btn-large pull-right']")))
            exit_but_id = exit_but.get_attribute("id")
            if self.percent_stamina < 50:
                self.restore(exit_but, exit_but_id)
            else:
                middle = WebDriverWait(self.browser, 8).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='content_middle']//div[@class='content_style main-content ']//div//div//ul[@class='unstyled inline user_list nightlife_user_list-wvAHNDRXPPwuDdwQZDzyK_0']//li")))
                user_respect = ([span.text for span in middle.find_elements_by_xpath("div[2]//div[3]//span") if len(span.text) > 0])
                user_id = middle.find_element_by_xpath("div//span//a//img").get_attribute("data-userid")
                user_name = middle.find_element_by_xpath("div//span//a//img").get_attribute("data-username")
                user_proffesion = middle.find_element_by_xpath("div[2]//div[2]").text
                print(user_name+" - "+user_proffesion+": "+user_respect[0])
                # data = self.browser.execute_script(js_get_victim_data)
                if int(user_respect[0]) > 10000 and int(user_respect[0]) < 200000:
                    for avoid in people_to_avoid:
                        if avoid in user_proffesion:
                            self.exit_club(exit_but, exit_but_id)
                            break
                    choose_victim = WebDriverWait(self.browser, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='content_middle']//div[@class='content_style main-content ']//div//div//div//div[@class='pull-left middle-col-4']//div//div[@class='dropdown']//button[@class='btn btn-inverse dropdown-toggle']"))).click()
                    get_victim = WebDriverWait(self.browser, 15).until(EC.visibility_of_element_located((By.XPATH, f"//div[@id='content_middle']//div[@class='content_style main-content ']//div//div//div//div[@class='pull-left middle-col-4']//div//div//ul[@class='dropdown-menu']//li//a"))).click()
                    kill_him = WebDriverWait(self.browser, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='content_middle']//div[@class='content_style main-content ']//div//div//div//div[@class='pull-left middle-col-4']//button[contains(text(), 'Attack')]"))).click()
                    self.change_logs("/nightlife/nightclub", "kill", int(user_id))
                    print(f"Killed {user_name}")
                    self.exit_club(exit_but, exit_but_id)
                else:
                    self.exit_club(exit_but, exit_but_id)  
        except TimeoutException: #/// ff none comes to club then timeoutexception arises - it is treated as repetition of entering the club
            try:
                self.exit_club(exit_but, exit_but_id)
            except:
                self.clubs()
                    
    def restore(self, exit_but, exit_id):
        self.change_logs("/nightlife", "enter", str(exit_id[12:]), True)
        self.exit_club(exit_but, exit_id, "delay")
            
    def exit_club(self, exit_but, exit_id, *args):
        exit_but.click()
        self.change_logs("/nightlife/nightclub", "exit", str(exit_id[12:]))
            
        nightclub_image = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.btn-inverse.btn-small.pull-right")))
        if nightclub_image:
            if "delay" in args:
                sleep(3)
                refresh = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#menu-sprite-robbery")))
                refresh.click()
                sleep(3)
            self.clubs()

if __name__ == "__main__":
    login = "login" #// put your login here
    password = "password" #// put your password here
    try:
        app = crims_hitman(login, password)
        app.log_in()
        app.clubs()
    except:
        app.clubs()
