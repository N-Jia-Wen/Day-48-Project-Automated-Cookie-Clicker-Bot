import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, "cookie")

timeout = time.time() + 5
end_five_min = time.time() + 60*5

while True:

    cookie.click()

    if time.time() > timeout:

        powerups_elements = driver.find_elements(By.CSS_SELECTOR, "#store b")
        powerups_elements.remove(powerups_elements[-1])

        money_balance = driver.find_element(By.ID, "money").text
        if "," in money_balance:
            money_balance = money_balance.replace(",", "")
        money_balance = int(money_balance)

        highest_price = 0
        powerup_to_buy = None

        for powerup in powerups_elements:
            powerup_price = powerup.text.split("-")[1]
            # Removes , from numbers like 2,000, 50,000 so that it can be converted into an integer
            if "," in powerup_price:
                powerup_price = powerup_price.replace(",", "")

            powerup_price = int(powerup_price)
            # Check if powerup can be bought with current amount of money:
            if powerup_price <= money_balance:
                # Checks if it is the most expensive powerup that can be bought:
                if powerup_price > highest_price:
                    powerup_to_buy = powerup
                    highest_price = powerup_price

        if powerup_to_buy is not None:
            powerup_to_buy.click()

        timeout = time.time() + 5

    if time.time() > end_five_min:
        cookie_rate = driver.find_element(By.ID, "cps").text
        print(cookie_rate)
        break
