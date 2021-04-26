from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from csv import writer
from bs4 import BeautifulSoup
import re
import time
driver = webdriver.Chrome(executable_path= "C:\chromedriver_win32\chromedriver")
driver.get("http://cbseaff.nic.in/cbse_aff/schdir_Report/userview.aspx")
driver.find_element_by_xpath("//*[@id='optlist_2']").click()
driver.implicitly_wait(5)
all_option = Select(driver.find_element(By.ID,"ddlitem")).options
for j in range(1,len(all_option)):
    option = all_option[j]
    option = option.text.strip() + ".csv"
    all_option[j] = option
    print(all_option[j])

for i in range(1,len(all_option)):
    with open(all_option[i],'w') as csv_file:
        Select(driver.find_element(By.ID,"ddlitem")).select_by_index(i)
        driver.implicitly_wait(200)
        driver.find_element_by_id("search").click()
        total_schools = int(driver.find_element(By.ID,'tot').text)
        total_pages = int(total_schools / 25) + 1
        print(total_schools,total_pages)
        csv_writer = writer(csv_file)
        headers = ['Affiliation No.','Name','Head/Principle','Status of the School:','Affiliated Upto','Address', 'Phone', 'Email']
        csv_writer.writerow(headers)
        driver.implicitly_wait(5)
        for j in range(1,total_pages):
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            rows = soup.select("table#T1 > tbody > tr > td > table")
            rows.pop(0)
            driver.implicitly_wait(5)
            for row in rows:
                col1 = row.select("tbody > tr > td")[7]
                col2 = row.select("tbody > tr > td")[1]
                name = col2.select("tbody > tr a")[0].getText()
                address = re.sub(r"[\n\t]*", "", col1.select("table > tbody > tr")[0].getText()[9:])
                Phoneno = re.sub(r"[\n\t]*", "", col1.select("table > tbody > tr")[1].getText()[10:])
                email = re.sub(r"[\s\n\t]*", "", col1.select("table > tbody > tr")[2].getText()[8:-11])
                Principle_name = re.sub(r"[\n\t]*", "", col2.select("table > tbody > tr")[2].getText()[21:])
                affnum = re.sub(r"[\s\n\t]*", "", col2.select("table > tbody > tr")[0].getText()[16:])
                sos = re.sub(r"[\n\t]*", "", col2.select("table > tbody > tr")[3].getText()[22:])
                upto = re.sub(r"[\n\t]*", "", col2.select("table > tbody > tr")[4].getText()[18:])
                csv_writer.writerow([affnum,name, Principle_name,sos,upto,address, Phoneno, email])
            nextButton = driver.find_element(By.ID,"Button1")
            driver.execute_script("arguments[0].click();", nextButton)
            driver.implicitly_wait(5)
driver.quit()












