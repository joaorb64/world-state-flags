from bs4 import BeautifulSoup
import json
import re
import unicodedata
import os
import requests
import shutil
import subprocess
import itertools

dont_download = [
    "/misc/"
]


def CanDownload(url):
    for d in dont_download:
        if d in url:
            return False
    return True


def remove_accents_lower(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower().strip()


def download_flag(url, outfile):
    response = requests.get(url)

    if response.status_code == 200:
        with open("./tmp.gif", 'wb') as f:
            f.write(response.content)

        subprocess.call(f'convert ./tmp.gif -resize 64x {outfile}', shell=True)


url = 'https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/countries%2Bstates%2Bcities.json'

r = requests.get(url, allow_redirects=True)
open('countries+states+cities.json', 'wb').write(r.content)

f = open('countries+states+cities.json')
data = json.load(f)

numCountries = len(data)
i = 1

keywordSoups = {}

print("Fetching search...")
for letter in [str(chr(i)) for i in range(ord('a'), ord('z')+1)]:
    url = f'https://www.fotw.info/flags/keyword{letter}.html'
    page = requests.get(url).text
    soup = BeautifulSoup(page, features="lxml")
    keywordSoups[letter] = soup


for country in data:
    print(f'{country.get("name")} - {i}/{numCountries}')
    countryPath = f"./out_flagsnet/{country.get('iso2')}"
    os.makedirs(countryPath, exist_ok=True)

    filePath = f'./images/{country.get("iso2").lower()[0]}/'

    for region in country.get("states"):
        if region.get("state_code") == "CON":
            region["state_code"] = "_CON"

        found = False
        tries = [
            remove_accents_lower(region.get("name")),
            region.get("state_code")
        ]

        for nameTry in tries:
            try:
                url = f'https://www.fotw.info/flags/{country.get("iso2")}-{nameTry}.html'
                page = requests.get(url).text
                soup = BeautifulSoup(page, features="lxml")

                allImages = soup.select("img")
                allImages = [
                    img for img in allImages if CanDownload(img.get("src"))]

                if len(allImages) > 1:
                    imgSrc = allImages[1]["src"]
                    if imgSrc.startswith("../"):
                        imgSrc = f'https://www.fotw.info/{imgSrc[2:]}'
                    print(
                        f'Found {countryPath}/{region.get("state_code")} - {imgSrc}')
                    download_flag(
                        imgSrc,
                        f'{countryPath}/{region.get("state_code").upper()}.png'
                    )
                    found = True
                    break
            except Exception as e:
                print(e)

        if not found:
            try:
                regionName = remove_accents_lower(region.get("name"))
                regionCountry = remove_accents_lower(country.get("name"))

                soup = keywordSoups[regionName[0]]

                links = soup.select("a")

                subpage = None

                for link in links:
                    if remove_accents_lower(link.text) == f"{regionName} ({regionCountry})" and link.get("href"):
                        subpage = "https://www.fotw.info/flags/" + link["href"]
                        break

                if subpage:
                    page = requests.get(subpage).text
                    soup = BeautifulSoup(page, features="lxml")

                    allImages = soup.select("img")
                    allImages = [
                        img for img in allImages if CanDownload(img.get("src"))]

                    if len(allImages) > 1:
                        imgSrc = allImages[1]["src"]
                        if imgSrc.startswith("../"):
                            imgSrc = f'https://www.fotw.info/{imgSrc[2:]}'
                        print(
                            f'Found alternative {countryPath}/{region.get("state_code")} - {imgSrc}')
                        download_flag(
                            imgSrc,
                            f'{countryPath}/{region.get("state_code").upper()}.png'
                        )
            except Exception as e:
                print(e)
    i += 1
