from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from os import system

driver = webdriver.Chrome("/Users/mattiabernardi/Documents/01_Workspace/05_IOT/02_server/chromedriver")

def shouldAdd(selector):
    return selector

def addToCart(selector):
    if (not shouldAdd(selector)) :
        print("Item Already in Cart!")
        return False
    url = "https://www.amazon.it/s?k=B084W8DMJT&__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss_2"
    driver.implicitly_wait(1)
    driver.get(url)
    driver.maximize_window()
    driver.find_element_by_id('sp-cc-accept').click()

    driver.find_element_by_xpath(
        '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[2]/div/span/div/div/span/a/div'
        ).click()
    
    # Check for time based purchase
    try:
        driver.find_element_by_id("newAccordionRow").click()
        print("Periodic Purchase Available, Switching to single purchase...")
    except NoSuchElementException:
        print("No Periodic Purchase Available...")
    
    print("Item Not in Cart Yet, Adding...")
    driver.find_element_by_id("add-to-cart-button").click()
    driver.find_element_by_id('hlb-view-cart-announce').click()

if __name__ == "__main__":
    selector = True
    while(True):
        print("Dimostrazione 'Add to Cart':\n")
        print("Per la dimostrazione utilizzeremo il prodotto 'Viakal Anticalcare'")
        system('clear')
        addToCart(selector)
        selector = False
        input("Premere Invio per Provare ad aggiungere di nuovo...")
        system('clear')
        addToCart(selector)
        print("\nRiprovare? [y/n]")
        sel = input()
        if sel == "n":
            break


