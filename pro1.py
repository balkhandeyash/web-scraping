from selenium import webdriver
from bs4 import BeautifulSoup
import pymongo
import certifi
ca = certifi.where()

# connect to the MongoDB Atlas database
uri = "mongodb+srv://shreyashwaghmare2019:admin@cluster0.0d5yfla.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri, tlsCAFile=ca)
db = client["test"]
collection = db["companies"]


# initialize the driver
driver = webdriver.Chrome()

# navigate to the website
website = "https://in.indeed.com/jobs?q=data+analyst&l=India&vjk=ea0ff44a26f5a4ec/js"
driver.get(website)

# wait for the page to load
driver.implicitly_wait(10)


# extract the content
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')


#j1= soup.find_all('table', class_='jobCard_mainContent big6_visualChanges')
jobs = soup.find_all('td', class_='resultContent')


data = []
for job in jobs:
    tit = job.find('span').text.strip()
    companyName = soup.find('span', class_='companyName')
    location = soup.find('div', class_='companyLocation')
    salary = soup.find('div', class_='metadata salary-snippet-container')
    print("Job Title : ",tit)
    print("Company Name : ",companyName.get_text())
    print("Location : ",location.get_text())
    print("Salary : ",salary.get_text())
    print("Link : ",website)
    print("--------------------------------------------------")

    data = [
        {
            "Job_Title": tit,
            "Company_Name": companyName.get_text(),
            "Location": location.get_text(),
            "Salary": salary.get_text(),
            "link": website
        }
    ]
    result = collection.insert_many(data)


# close the driver
driver.close()
