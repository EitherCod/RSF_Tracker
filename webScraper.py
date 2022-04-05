from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.chrome import ChromeDriverManager
from urllib.request import urlopen
import time
from bs4 import BeautifulSoup 
import schedule
from datetime import date
from datetime import datetime


def get_rsf_occupancy():
	#Result File 
	result_file_path = "data.txt"

	#Get Current Date + Time 
	current = datetime.now()
	dt_string = current.strftime("%d/%m/%Y %H:%M")
	print("Executing at {}.".format(dt_string))

	#Target URL + Div Class I Am Scraping From
	url = 'https://safe.density.io/#/displays/dsp_956223069054042646?token=shr_o69HxjQ0BYrY2FPD9HxdirhJYcFDCeRolEd744Uj88e'
	target_class = 'styles_waitTimeFullnessWrapper__3PRdQ'

	#Make sure the browser doesn't pop up 
	chrome_options = webdriver.ChromeOptions()
	chrome_options.headless = True

	#Get the html page source
	s= Service(ChromeDriverManager().install())
	driver = webdriver.Chrome(service=s, options=chrome_options)
	driver.get(url)
	time.sleep(5)
	html = driver.page_source

	#Get the percentage the RSF is full 
	soup = BeautifulSoup(html, 'html.parser')
	target_tag = soup.find("div", class_ = target_class)
	rsf_percentage = target_tag.text[0]

	#Write Result to The Data File
	f = open(result_file_path, 'a')
	f.write(dt_string + ' , ' + str(rsf_percentage) + '\n')
	f.close()

#Log Data every 5 Minutes 
schedule.every(5).minutes.do(get_rsf_occupancy)

while True:
    schedule.run_pending()




