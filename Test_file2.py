import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import pandas as pd
import os

# os.popen('chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\All Files\Web Scraping\Chrome cache"')
#
option = webdriver.ChromeOptions()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome("D:/chromedriver.exe", options=option)

# driver.get("https://www.youtube.com/playlist?list=PLVS9j0kNv0qz3LKRu1TE-iIwee2NMZ4e0")

# contents = driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-playlist-video-list-renderer/div[3]')
#
# print("extracting")
# songslist = []
# channelname = []
# for item in contents.find_elements(By.TAG_NAME, 'ytd-playlist-video-renderer'):
#     # print(item.find_element(By.ID, 'video-title').text)
#     name = item.find_element(By.ID, 'video-title').text
#     chname = item.find_element(By.CLASS_NAME, 'style-scope ytd-channel-name').text
#     songslist.append(name)
#     channelname.append(chname)
#     print(len(songslist), name, chname, sep='\t')
#     # break
#
# Datadict = {"Name": songslist,
#             "Channel name": channelname}
#
# data = pd.DataFrame(Datadict)
# print(data)
#
# data.to_csv("Songslist.csv")

# driver.get("https://open.spotify.com/search")

data = pd.read_csv("Songslist.csv")

song_names = list(data["Name"])
status = []

for name in song_names[27:]:
    input = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div[1]/header/div[3]/div/div/form/input')
    input.click()
    # input.click()
    input.clear()
    input.send_keys(name)
    input.send_keys(Keys.RETURN)
    time.sleep(2)

    print(song_names.index(name), name, sep='\t')

    try:
        ac = ActionChains(driver)
        ac.context_click(driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/div[2]/div/div/section[2]/div[2]/div/div/div/div[2]/div[1]')).perform()
        time.sleep(2)

        addtoplaylist = driver.find_element(By.XPATH, '/html/body/div[15]/div/ul/li[7]/button')
        addtoplaylist.click()
        time.sleep(2)

        playlistname = driver.find_element(By.XPATH, '/html/body/div[15]/div/ul/li[7]/div/ul/div/li[3]/button')
        playlistname.click()
        time.sleep(2)

        if str(driver.page_source.text).count('Already added') > 0:
            print("Already added")
            status.append("Already Added")

            Dontadd = driver.find_element(By.XPATH, '/html/body/div[6]/div/div/div/div/button[2]/span')
            Dontadd.click()
            time.sleep(1)
        else:
            status.append("Added")
            print("Added")
    except:
        print("Not Found")
        status.append("Not Found")




print(f"Found:{status.count('Found')} \nNot Found:{status.count('Not found')}")
