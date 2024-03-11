import csv
import string
import requests
from bs4 import BeautifulSoup
import sys
import os
import subprocess
import re
import numpy

# from pyquery import PyQuery as pq
# from lxml import etree
# import urllib

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import Select




print_all = False

driver = webdriver.Chrome()


with open('google_patent_search_results.csv') as csv_patent_list:
    patent_list_reader = csv.DictReader(csv_patent_list)
    counter = 0;
    for row in patent_list_reader:
        if counter == 0:
            counter+=1
            continue
        

        ## OPEN PATENT PAGE IN GOOGLE
        this_patent_code = row['patent_code']
        this_patent_code = this_patent_code.translate(str.maketrans('','',string.punctuation))

        google_URL = "https://patents.google.com/patent/" + this_patent_code + "/en"
        page = requests.get(google_URL)

        # patent_html = pq(url=URL, parser='html_fragments')

        # print(patent_html)
        
        # concept_mentions = patent_html.filter('concept-mention')

        # print(concept_mentions)
        
        
        soup = BeautifulSoup(page.content, "html.parser")
        
        ## CODE
        if print_all:
            print(this_patent_code)
            
        ## TITLE
        
        title = str(soup.find("title"))
        first_space = title.find(" ")
        title = title[first_space+3:]
        second_space = title.find("Google")
        title = title[:second_space-5]
        
        if print_all:
            print(title)
            

        ## ABSTRACT
        abstract = soup.find("abstract")

        abstract = abstract.find("div",attrs={'class' : 'abstract'} )

        if print_all:
            print("Patent Abstract:")
            print(abstract.string)


        ## RELATED PATENT CODES
        concepts = soup.find("section")

        all_codes = concepts.find_all("span",attrs={'itemprop': 'Code' })
       
        codes_string = ""
        for patent_code in all_codes:
            codes_string = codes_string + patent_code.string + ", "

        codes_string = codes_string[:-2]
        if print_all:
            print("Includes patent codes: "+print_string)

        ## DOWNLOAD LINK

        for sections in soup.find_all("a"):
            # print(sections['href'])
            if sections.text == "Download PDF":
                download_link = sections['href']

        if print_all:
            print("Download link: "+download_link)

        ## INVENTOR

        wget_command = "wget "+google_URL+" -q -O goog_dls/"+this_patent_code+".html"
        wget_output = os.system(wget_command)

        if wget_output != 0:
            disp("Unable to download google page.")

        grep_command = "cat goog_dls/"+this_patent_code+".html | grep \"inventor\" > ./goog_dls/grep_output.txt"
        grep_output = str(os.system(grep_command))

        inventors = []
        with open('./goog_dls/grep_output.txt') as grep_output:
            for line in grep_output:
                # print(line)
                end_char = line.find("scheme")
                first_char = line.find("content")
                if end_char != -1:
                    inventors.append(line[first_char+9:end_char-2])
                    

        if print_all:
            print("List of inventors:")
            print(inventors)
                    #findoutput = line.find("repeat")

                # print(findoutput)
                # print("~~~~")
                #   print(grep_output)
                # for char in range(0, len(grep_output)):
                #     if grep_output[char] == '"':
                # print(grep_output[char])
                # print("~~~~")

        ## MOVE TO WIPO PATENTSCOPE
        driver.get("https://patentscope.wipo.int/search/en/structuredSearch.jsf")


        selectors = Select(driver.find_elements(By.XPATH, "//select"))
        print(selectors)
        
        # search_field = Select(driver.find_elements(By.NAME,"structuredSearchForm"))
        # search_field.select_by_visible_text("Inventor All Data")

        
        
        
        # search_field.select(By.VISIBLE_TEXT,"Inventor All Data")
        
        # # for x in ele:
        # #     print(x)
            # print("!!!!")
            # print(x.get_attribute('id'))
        
        # selecter = Select(driver.find_element(By.TEXT("All Numbers and IDs")))
        # print(selector)
                                         
                
     
        print("~~~~~~~~~~~")
        counter = counter + 1
        if counter > 1:
            break

driver.close()
