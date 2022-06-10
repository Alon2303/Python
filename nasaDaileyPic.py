import requests
import configparser
import ctypes

config = configparser.ConfigParser()		
config.read("config.ini")
apikey = config['API_KEYS']
print(apikey)
directory = config['DIR']


url = "https://api.nasa.gov/planetary/apod?api_key=%s"%apikey['NASA_API']

def changeBg(filename):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, filename, 3)
    print("Done")

def saveFile(filename, res):
    with open(f"{directory['NASA_DAILY_PICTURE_DIR']}/{filename}", 'wb') as fd:
     for chunk in res.iter_content(chunk_size=128):
        fd.write(chunk)
    changeBg(f"{directory['NASA_DAILY_PICTURE_DIR']}/{filename}")

def getPic():
    res = requests.get(url)
    hdurl = res.json()['hdurl']
    regurl = res.json()['url']
    res1 = requests.get(regurl)
    res2 = requests.get(hdurl)
    if res2.status_code == 200: 
        saveFile(hdurl.split("/")[6], res2)
    elif res1.status_code == 200:
        saveFile(regurl.split("/")[6], res1)