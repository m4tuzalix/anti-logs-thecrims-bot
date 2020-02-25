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
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--proxy-server=http://%s' % PROXY)
        self.browser = webdriver.Chrome("D:\crims\chromedriver.exe")
        self.browser.get("https://www.thecrims.com/")

        self.killers = {}
        self.killed_people = []
        self.x_request = None
        self.club = None

        self.log_in()
        self.clubs()
        self.kill_people()


    def log_in(self):
        login = self.browser.execute_script(js_request_login, self.login, self.password)
        sleep(3)
        self.alert_catcher("x_req")
    
    def clubs(self):
        all_clubs = self.browser.execute_script(js_get_clubs, self.x_request)
        sleep(2)
        self.alert_catcher("club")
        self.thread_logs("/nightlife", "enter", self.club)
    
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
        if args:
            restore_hp = True
        
        if self.action == "exit":
            post_route = "https://www.thecrims.com/api/v1/nightclub/exit"
            move = "https://www.thecrims.com/newspaper#/nightlife"
        elif self.action == "enter":
            post_route = "https://www.thecrims.com/api/v1/nightclub"
            move = "https://www.thecrims.com/newspaper#/nightlife/nightclub"

        #// sends the request to server
        self.browser.execute_script(js_main_requests_pattern, dumps(Logs), post_route, self.x_request, move, restore_hp)

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
        self.thread_logs("/nightlife", "normal", "")
        people_to_avoid = ["Hitman","Padrino","Kingpin", "Godfather", "Top executive", "Mobster", "Desperado",  "Director", "Consigliere"]
        
        self.current_stamina = self.browser.find_element_by_xpath('//div[@class="text-center"]//div[@id="nightclub-singleassault-attack-18"]//div[@class="default-1CS8SFNfrzFfM38mxoY6af_0"]').value_of_css_property("width")
        self.percent_stamina = round(100*float(self.current_stamina[:-2])/128)
        exit_but = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH,"//div[@id='page']//div[@id='content']//table[@id='content_table']//tbody//tr//td//div[@id='content_middle']//div[@class='content_style main-content ']//div[3]//div//button[@class='btn btn-inverse btn-large pull-right']")))
        exit_but_id = exit_but.get_attribute("id")
        if self.percent_stamina < 50:
            self.restore(exit_but, exit_but_id)
        else:
            try:
                middle = WebDriverWait(self.browser, 8).until(EC.presence_of_element_located((By.XPATH, "//div[@id='content_middle']//div[@class='content_style main-content ']//div//div//ul[@class='unstyled inline user_list nightlife_user_list-wvAHNDRXPPwuDdwQZDzyK_0']//li")))
                if middle:
                    data = self.browser.execute_script(js_get_victim_data)
                    print(data["respect"])
                    self.exit_club(exit_but, exit_but_id)
                        
            except TimeoutException: #/// ff none comes to club then timeoutexception arises - it is treated as repetition of entering the club
                try:
                    self.exit_club(exit_but, exit_but_id)
                except:
                    WebDriverWait(self.browser, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay")))
                    self.clubs()
                    
    def restore(self, exit_but, exit_id):
        self.thread_logs("/nightlife", "enter", str(exit_id[12:]), True)
        self.exit_club(exit_but, exit_id)
            
    def exit_club(self, exit_but, exit_id):
        for x in range(randint(1,4)):
                    self.thread_logs("/nightlife", "exit", str(exit_id[12:]))
        exit_but.click()
        sleep(2)
        self.clubs()

if __name__ == "__main__":
    login = "login" #// put your login here
    password = "password" #// put your password here
    try:
        app = crims_hitman(login, password)
        # app.log_in()
        # app.get_killers()
        # app.restore_stamina()
        # app.kill_people()
    except:
        pass
