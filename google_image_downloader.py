from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import os
import json
import urllib
import urllib.request
import sys
import time

# adding path to geckodriver to the OS environment variable
os.environ["PATH"] += os.pathsep + os.getcwd()
searchtext = "TYPE YOUR KEYWORDS HERE"
dir_path = os.path.dirname(os.path.realpath(__file__))
download_path = dir_path + '/' + 'download' + '/' + searchtext

def main():

	num_requested = 4000
	number_of_scrolls = num_requested / 400 + 1
	# number_of_scrolls * 400 images will be opened in the browser

	options=Options()
	options.set_headless(headless=True)
	#headless firefox

	if not os.path.exists(download_path):
		os.makedirs(download_path)

	url = "https://www.google.co.in/search?q="+searchtext+"&source=lnms&tbm=isch"
	driver = webdriver.Firefox(firefox_options=options)
	driver.get(url)

	headers = {}
	headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
	extensions = {"jpg", "jpeg", "png", "gif"}
	img_count = 0
	downloaded_img_count = 0
	
	for _ in range(int(number_of_scrolls)):
		for __ in range(10):
			# multiple scrolls needed to show all 400 images
			driver.execute_script("window.scrollBy(0, 1000000)")
			time.sleep(0.2)
		# to load next 400 images
		time.sleep(0.5)
		try:
			driver.find_element_by_xpath("//input[@value='顯示更多結果']").click()
		except Exception as e:
			print ("Less images found:", e)
			break

	imges = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
	print ("Total images:", len(imges), "\n")
	for img in imges:
		try:
			img_count += 1
			img_url = json.loads(img.get_attribute('innerHTML'))["ou"]
			img_type = json.loads(img.get_attribute('innerHTML'))["ity"]
			print ("Downloading image", img_count, ": ", img_url)
			
			if img_type not in extensions:
				img_type = "jpg"
			raw_img = urllib.request.urlretrieve(img_url, download_path+"/"+searchtext + "_" +str(downloaded_img_count)+"."+img_type)
			downloaded_img_count += 1
			time.sleep(2)
		except Exception as e:
			print ("Download failed:", e)
		finally:
			print
		if downloaded_img_count >= num_requested:
			break

	print ("Total downloaded: ", downloaded_img_count, "/", img_count)
	driver.quit()

if __name__ == "__main__":
	main()