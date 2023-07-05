#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os

def download_images(keyword, num_images):
    # Create a directory to store the downloaded images
    if not os.path.exists(keyword):
        os.makedirs(keyword)

    # Configure the Selenium Chrome driver
    service = Service('C:/Users/cheta/anaconda3/Lib/site-packages/chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    # Open the browser and navigate to Google Images
    driver.get(f"https://www.google.com/search?q={keyword}&tbm=isch")

    # Scroll down to load more images
    last_height = driver.execute_script("return document.body.scrollHeight")
    while len(driver.find_elements(By.XPATH, '//img[@class="rg_i Q4LuWd"]')) < num_images:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Find the image elements
    image_elements = driver.find_elements(By.XPATH, '//img[@class="rg_i Q4LuWd"]')

    count = 0
    for image_element in image_elements[:num_images]:
        # Get the image source URL
        image_url = image_element.get_attribute("src")

        if image_url:
            try:
                # Download the image
                urllib.request.urlretrieve(image_url, f"{keyword}/{count}.jpg")
                count += 1
                print(f"Downloaded image {count}")
            except Exception as e:
                print(f"Failed to download image: {e}")

    # Close the browser
    driver.quit()

# Prompt the user for the keyword and the number of images to download
keyword = input("Enter the keyword: ")
num_images = 50

# Call the function to download the images
download_images(keyword, num_images)


# In[ ]:




