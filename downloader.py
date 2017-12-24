import os
import shutil
import requests
from bs4 import BeautifulSoup

r = requests.get("") # Put your link here
soup = BeautifulSoup(r.text, "html.parser")
imgElems = soup.find_all("a", class_="fileThumb")
imgLinks = list(map(lambda i: "https:"+i['href'], imgElems))

print("Starting image downloader")
if not os.path.exists('./images'):
    os.makedirs('./images')
for imgLink in imgLinks:
    imgName = imgLink.split('/')[-1]
    with open('./images/'+imgName, "wb") as f:
        print(imgLink)
        r = requests.get(imgLink, stream=True)
        shutil.copyfileobj(r.raw, f)
print("Complete")
