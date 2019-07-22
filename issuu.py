from bs4 import BeautifulSoup
import sys
import wget
import os
import urllib.request
import re
import subprocess
import tempfile

url = str(input("Enter the url: "))
howmanypages = int(input("How many pages? "))

def safepath(title):
    return title.replace(os.path.sep, '_')

with tempfile.TemporaryDirectory() as tmpdir:
    for page in range(1, howmanypages + 1):

        # download webpage for scraping
        webpage = urllib.request.urlopen(url)
        soup = BeautifulSoup(webpage, 'html.parser')

        # locate the image asset
        pagetitle = safepath(soup.find('meta', attrs={'property': 'og:title'})['content'])
        imglink3 = soup.find('meta', attrs={'property': 'og:image'})['content']
        imglink2 = imglink3.replace('1.jpg','')
        imglink = imglink2 + str(page) + ".jpg"

        # download image asset
        wget.download(imglink, out=os.path.join(tmpdir, 'page_%04d.jpg' % (page)))
        print('\nPage {}: {}\n'.format(page, imglink))

        with open(pagetitle + ' urls.txt', 'a') as f:
            f.write(imglink + '\n')

    # convert pages to pdf
    params = ['convert', os.path.join(tmpdir, 'page_*'), pagetitle + '.pdf']
    subprocess.run(params)

# collect information on the file
metadata = {}
metadata['URL'] = url
metadata['description'] = soup.find('meta', attrs={'property': 'og:description'})['content']

metadata['uploaded'] = soup.find('div', attrs={'itemprop': 'datePublished'})['datetime']

upload_link_soup = soup.find('div', attrs={'class': 'PublisherInfo__name--3j27Y'})
metadata['uploader_link'] = "https://issuu.com" + upload_link_soup.a['href']

metadata['uploader'] = soup.find('a', attrs={'itemprop': 'author'}).contents[0]

metadata_out = '\n'.join({'{}: {}'.format(k, v) for k, v in metadata.items()})
print(metadata_out)

with open(pagetitle + ' info.txt', 'w') as f:
    f.write(metadata_out)
