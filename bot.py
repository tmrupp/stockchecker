import time
from selenium import webdriver
import sys
import json
import winsound

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--disable-notifications")
chromeOptions.add_argument("start-maximized") 

# "./chromedriver", 
driver = webdriver.Chrome("./chromedriver", options=chromeOptions)  # Optional argument, if not specified will search path.
# driver.get(ASUS3080);
# driver.get('https://secure.newegg.com/identity/signin?tk=c07d00037e504dd888db417363be960b16222')

ADDTOCART = "//*[@id=\"ProductBuy\"]/div/div[2]/button"
OOS = "//*[@id=\"ProductBuy\"]/div/div/span"


NOTHANKS = "//*[@id=\"modal-intermediary\"]/div/div/div/div[3]/button[1]"
INITIALPOPUP = "//*[@id=\"popup-close\"]"
VIEWCART = ["//*[@id=\"modal-intermediary\"]/div/div/div[2]/div[2]/button[2]",
"//*[@id=\"modal-intermediary\"]/div/div/div/div[3]/button[2]"]
OOPS = "//*[@id=\"modal-pc-builder-check\"]/div/div/div/button/span/i"
PAYPAL = "//*[@id=\"app\"]/div/section/div/div/form/div[2]/div[1]/div[2]/div[3]/div/div[2]/div/div[3]/div[1]/div[2]/div/div[2]/div"
SECURECHECKOUT = "//*[@id=\"app\"]/div[1]/section/div/div/form/div[2]/div[3]/div/div/div[3]/div/button"

ENTEREMAIL = "//*[@id=\"labeled-input-signEmail\"]"
ENTERPASSWORD = "//*[@id=\"labeled-input-password\"]"
SIGNINSUBMIT = "//*[@id=\"signInSubmit\"]"

LOGIN = "//*[@id=\"app\"]/header/div[1]/div[4]/div[1]/div[1]/a/div[2]"

CONTINUETOPAYMENT = "//*[@id=\"app\"]/div/section/div/div/form/div[2]/div[1]/div[2]/div[2]/div/div[3]/button"

NEWEGGLOGIN = "https://secure.newegg.com/identity/signin?tk=e9c84ef3cc154b3da823eb7ce01dca7624111a"

CVV = "//*[@id=\"app\"]/div/section/div/div/form/div[2]/div[1]/div[2]/div[3]/div/div[2]/div/div[3]/div[2]/div[3]/div[1]/div/label/div[4]/input"

j = json.load(open("./personal_info.json"))

EMAIL = j["email"]
PASSWORD = j["password"]

initialSetup = True

def tryClick (b):
    try:
        button = driver.find_element_by_xpath(b)
        button.click()
        return True
    except:
        print("no " + b)
        return False

def clickButton (b, maxTries=5):
    if isinstance(b, list): 
        for x in b:
            if (clickButton(x)):
                return True
        return False
    else:
        clicked = False
        tries = 0
        while (not clicked and (maxTries == 0 or tries < maxTries)):
            clicked = tryClick(b)
            tries = tries + 1

        return clicked

def tryInfo (f, v):
    try:
        field = driver.find_element_by_xpath(f)
        field.send_keys(v)
        return True
    except:
        print("no " + f)
        return False

def enterInfo (f, v, maxTries=5):
    clicked = False
    tries = 0
    while (not clicked and (maxTries == 0 or tries < maxTries)):
        clicked = tryInfo(f, v)
        tries = tries + 1

def findStock ():
    while (True):
        if (tryClick(OOS)):
            return False
        elif (tryClick(ADDTOCART)):
            return True

def login ():
    enterInfo(ENTEREMAIL, EMAIL, 100)
    clickButton(SIGNINSUBMIT)
    enterInfo(ENTERPASSWORD, PASSWORD, 100)
    clickButton(SIGNINSUBMIT)

#login first?
#check for not in stock vs add to cart (don't manually time out)

# multithreaded check?
def NEWEGG_attempt (s):
    driver.get(s)

    global initialSetup

    if (initialSetup):
        time.sleep(4)
        clickButton(INITIALPOPUP)
        time.sleep(2)
        clickButton(LOGIN)
        login()
        initialSetup = False

    if (findStock()):
        winsound.Beep(2500, 1000)
        if (clickButton(NOTHANKS, 20)):
            if (clickButton(VIEWCART)):
                if (clickButton(SECURECHECKOUT, 20)):
                    if (clickButton(CONTINUETOPAYMENT, 30)):
                        input("Press Enter to continue...")

while (True):
    for x in j["products"]:
        NEWEGG_attempt(x)