import time
import numpy as np
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image


def get_image_address(src):
    main_address = "https://www.banknoteworld.com/images/product/"
    image_address = main_address + src.split("/")[-1]
    return image_address

def get_images_from_webpage(wd, delay, max_images, country):
    def scroll_down(wd):
        if np.random.random() < 0.15:
            wd.execute_script(f"window.scrollBy(0, -600);")
        else:
            wd.execute_script(f"window.scrollBy(0, 1500);")
        time.sleep(delay)

    url = "https://www.banknoteworld.com/banknotes/Banknotes-by-Country/?filter_bjeu3kfrd7=Banknote&filter_1vrzi848n7=Non-Graded&filter_5ammzleauo=" + country + "&filter_4xxkjcs9k5=2010-2019"
    wd.get(url)


    image_urls = set()
    timeout_seconds = 6.0
    start_time = time.time()

    while len(image_urls) < max_images:
        previous_length = len(image_urls)
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, "photo")
        for img in thumbnails[len(image_urls): max_images]:
            image_url = get_image_address(img.get_attribute("src"))
            if country.split(" ")[0][0:3].lower() in image_url.lower():
                image_urls.add(get_image_address(img.get_attribute("src")))

        print(f"Found images of {country}", len(image_urls))

        if len(image_urls) == previous_length:
            elapsed_time = time.time() - start_time
            if elapsed_time >= timeout_seconds:
                print(f"No new items added in the last {timeout_seconds} seconds. Stopping the process.")
                wd.quit()
                break
                
        else:
            start_time = time.time()
        

        
    return image_urls


def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name
        with open(file_path, "wb") as f:
            image.save(f, "JPEG")
        print("Success")
    except Exception as e:
        print("Failed -", e)