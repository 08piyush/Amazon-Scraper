# IMPORTING LIBRARIES 
from bs4 import BeautifulSoup
import requests
import random 
from lxml import etree, html
import time

# ROTATING USER AGENTS FOR SECURITY 
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
	,'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
	,'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
	,'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
	,'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
	,'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
	,'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]


#  BASE URL OF AMAZON WEBSITE 
BaseURL = "https://www.amazon.in/s"

# FUNCTION WHICH SCRAPES PRODUCTS FROM WEBSITE BASED ON ATTRIBUTES 
def scrape_product(product_soup, file) :

	# EXTRACT BRAND NAME IF EXISTS OTW NA
	try:
		brand_name = product_soup.find("span" , attrs= {"class": 'a-size-base-plus a-color-base'}).string.strip().replace(',','')
	except:
		brand_name = "NA" 

	# EXTRACT THE TITLE STRING/ PRODUCT DESCRIPTION 1
	try:
		title_string1 = product_soup.find("span" , attrs= {"class": 'a-size-base-plus a-color-base a-text-normal' }).string.strip().replace(',','')
	except:
		title_string1 = "NA" 
	
	# EXTRACT THE TITLE STRING/ PRODUCT DESCRIPTION 2
	try:
		title_string2 = product_soup.find("span" , attrs= {"class": 'a-size-medium a-color-base a-text-normal' }).string.strip().replace(',','')
	except:
		title_string2 = "NA" 
	
	# EXTRACT THE PRICE OF THE PRODUCT IN RS 
	try:
		price = product_soup.find("span" , attrs= {"class": 'a-offscreen' }).string.strip().replace(',', '')
	except:
		price = "NA" 	

	# EXTRACT THE RATING OF THE PRODUCT
	try:
		rating = product_soup.find("span" , attrs= {"class": 'a-icon-alt' }).string.strip().replace(',','')
	except:
		rating = "NA"

# WRITING INTO THE FILE 
	if((title_string1 != "NA" or title_string2 != "NA")):
		file.write(f"{brand_name},")
		if( title_string1 != "NA"):
			file.write(f"{title_string1},")
		else:
			file.write(f"{title_string2},")
		file.write(f"{price},")
		file.write(f"{rating}")
		file.write("\n")  

# MAIN FUNCTION 
def main():
	# USER ENTERS THE KEYWORD TO SEARCH, OUTPUT STORED IN THE FILE WITH SAME NAME 
	keyword = input("-----ENTER SEARCH KEYWORD-🔎---------- ") 
	File = open(keyword+".csv", "w", encoding="utf-8") # OUTPUT FILE 

	page_number = 1
	total_pages = 1
	total_products = 0 

	#  ITERATING THROUGH ALL THE PAGES ; IMPLEMENTATION OF PAGINATION 
	while page_number <= total_pages:
		user_agent = random.choice(user_agents) 
		HEADERS = {'User-Agent': user_agent,'Accept-Language': 'en-US, en;q=0.5'}
		params = {"k" : keyword,"page" : page_number} 

		webpage = requests.get(BaseURL, headers=HEADERS, params= params)
		soup = BeautifulSoup(webpage.content, "lxml")
		# print(soup.title.text) 
		# print(user_agent)
		print(random.choice(["Loading...", "Heavy traffic... ", "Too many requests...", "Loading...", "Hold On..."]))

		#  IF THE PAGE IS NOT BLOCKED BY ERROR 503
		if "503" not in soup.title.text :
			count = 0 
			products = soup.find_all("div", attrs = {"class" : "sg-col-inner"} )   
			max_pages = soup.find("span" , attrs = {"class" : "s-pagination-item s-pagination-disabled"})

			# EXRACTING THE TOTAL NUMBER OF PAGES 
			if total_pages ==1 and max_pages is not None :
				total_pages = int(max_pages.text)

			# SCRAPING EACH PRODUCT THROUGH THE PAGE 
			for product in products :
				count +=1 
				scrape_product(product, File)
			total_products += count

			# OUTPUT PAGES AND PRODUCTS COUNT 
			print("-----current page_number--📄----------------------- ", page_number)
			print("-----total pages----------📃---------------------- ", total_pages)
			print("-----total products retrieved on this page-🟢------ ", count)
			print("-----total products retrieved yet--📀-------------- ", total_products)
			print("-----output is saved in "+keyword+".csv file-------")

			# MOVING ON TO NEXT PAGE 
			page_number +=1 

		# SLIGHT WAIT BEFORE REQUESTING NEXT PAGE 
		time.sleep(random.uniform(0, 2))
	File.close()

if __name__ == '__main__':
	main()
