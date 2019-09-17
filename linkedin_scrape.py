""" filename: script.py """
# import web driver
from selenium import webdriver
import time
from credentials_linkedin import username, password
from bs4 import BeautifulSoup
import json
import re
import random
from selenium.common.exceptions import ElementClickInterceptedException
# to write the output
import pandas as pd
import numpy as np











# enter your job keyword here:
kword = 'Amazon'
# enter location keyword here:
loca = ''

# specifies the path to the chromedriver.exe
init_driver = webdriver.Chrome(executable_path="/Users/louisleguingruand/Desktop/perso/webscraping/chromedriver")

# run only once
def navigation_to_connections(driver=init_driver, con_level = 2):
    """
    this is the main function using selenium. takes the username and password form credentials_linkedin
    and navigates to the webpage
    :param driver: defualt is the driver. gets the state of the current webpage
    :param con_level: default is 2. takes values 2 or 3: indicates how many connections want to look at (2nd, 3rd network)
    :return: None, navigation happens in the subsequent body elements
    """

    # driver.get method() will navigate to a page given by the URL address
    driver.get('https://www.linkedin.com')
    time.sleep(1)

    try:
        driver.find_element_by_class_name('nav__button-secondary').click()
    except:
        time.sleep(1)
        return driver.find_element_by_class_name('nav__button-secondary').click()

    # locate email form by_class_name
    user = driver.find_element_by_id('username')

    # send_keys() to simulate key strokes
    user.send_keys(username)

    # locate password form by_class_name
    pw = driver.find_element_by_id('password')

    pw.send_keys(password)

    # locate submit button by_class_name
    # right click on node -> copy xpath
    driver.find_element_by_xpath('//*[@id="app__container"]/main/div/form/div[3]/button').click()


    connections = driver.find_elements_by_xpath("//span[contains(., 'Manage your network')]")[0]
    connections.click()

    time.sleep(10)
    driver.find_element_by_link_text("Search with filters").click()
    time.sleep(4)

    driver.find_element_by_xpath("//span[contains(@class, 'artdeco-button__text') and contains(., '1st')]").click()

    time.sleep(2)
    driver.find_element_by_xpath(
        "//span[contains(@class, 'search-s-facet-value__name') and contains(., '2nd')]").click()
    if con_level == 3:
        driver.find_element_by_xpath(
            "//span[contains(@class, 'search-s-facet-value__name') and contains(., '3rd')]").click()

    driver.find_element_by_xpath("//span[contains(@class, 'artdeco-button__text') and contains(., 'Apply')]").click()

    return driver
driver = navigation_to_connections()


def convert_elem_text(elem):
    """
    converts element which is profile infos from current Linkedin page
    :param elem: list of element with the tag included. eg: <span> tom hank </span>
    :return: list of text inside all the elements
    """
    output = []
    for i in elem:
        output.append(i.text)
    return output


def get_profile_info(driver=driver):
    """
    outputs profile infos from current Linkedin page
    :param driver: the current driver (state of page google chrome)
    :return: 3 lists of all elements in the current webpage: names, jobs and locations
    """
    # scroll to the bottom of webpage so that can load all elements:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    page_profile = BeautifulSoup(driver.page_source, 'lxml')
    names = page_profile.find_all('span', {'class': 'name actor-name'})
    name = convert_elem_text(names)
    # slicing to selet elements at even positions (only the job titles not locations
    jobs = page_profile.find_all('span', {'dir': 'ltr'})[0::2]
    job = convert_elem_text(jobs)
    location = page_profile.find_all('span', {'dir': 'ltr'})[1::2]
    locations = convert_elem_text(location)

    new_dict = {i: [j, k] for i, j, k in zip(name, job, locations)}

    try:
        time.sleep(2)
        click_next(driver)
    except ElementClickInterceptedException:
        time.sleep(3)
        click_next(driver)

    return new_dict



# loads it 4 by 4 so i need to get them all on one page!
def click_next(driver=driver):
    """
    clicks on the next page using the next button
    :param driver: current state webpage
    :return: the click
    """
    return driver.find_element_by_xpath("//span[contains(@class, 'artdeco-button__text') and contains(., 'Next')]").click()



profiles_dic = {}


# could just do this:
for i in range(1,100):
    print(i)
    time.sleep(random.randint(1,4))
    profiles_dic.update(get_profile_info())



# can filter on both the job and the location
def filtering(keyword=kword,location=loca):
    dict_regx = profiles_dic
    if keyword!= '':
        allowed = re.compile(str(keyword))
        dict_regx = dict(filter(lambda it: True if allowed.search(it[1][0]) else False, profiles_dic.items()))
    if location!='':
        allowed = re.compile(str(location))
        dict_regx = dict(filter(lambda it: True if allowed.search(it[1][0]) else False, dict_regx.items()))
    return dict_regx

profiles_dico = filtering('Amazon')
print(profiles_dico)

f = open("profile_list.txt","w")
f.write(str(profiles_dico))

df = pd.DataFrame(profiles_dico)  # transpose to look just like the sheet above
df.to_csv('file.csv')
df.to_excel('file.xls')


# soup_level1=BeautifulSoup(driver.page_source, 'lxml')
#
# f=open("webpage.txt", "w")
# f.write(soup_level1.prettify())
#
# soup_level2=BeautifulSoup(driver.page_source, 'lxml')





