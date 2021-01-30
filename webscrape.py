import requests
from html.parser import HTMLParser

'''
Scrapes planet minecraft for skin files to train a tensorflow model.
l1npengtul Rho (C) 2020-2021
This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''


taglist = []
todownloadlinklist = []
linklist = []
planetmc = "https://www.planetminecraft.com/resources/skins/?p="
planetmc_raw = "https://www.planetminecraft.com"
gdata = ""
emptyskipcnt = 0
# HTTP Headers required to make Planet Minecraft get the proper response instead of 403 Forbidden
# Do not change
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0'}

class parsehtml_1(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    if attr[1][0] == "/":
                        if "/skin/" in attr[1]:
                            taglist.append(str(attr[1]))
                            #print(attr[1])


# if statements are lies created by the american government to make people believe that they can have choice
class parsehtml_2(HTMLParser):
    appendList = list()
    appendTuple = tuple()

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            try:
                #print(a)
                if attrs[0][0] == 'class' and attrs[0][1] == 'js_link':
                    if'file' in attrs[1][1]:
                        if attrs[1][1] not in linklist:
                            self.appendTuple = tuple((attrs[1][1],))
                            linklist.append(attrs[1][1])
                            #print(attrs[1][1])
            except IndexError:
                pass

    def handle_data(self, data):
        if data == "Male":
            # TODO: ADD TUPLE MALE
            if self.appendTuple not in todownloadlinklist and self.appendTuple is not tuple():
                self.appendTuple = self.appendTuple + tuple(('Male',))
                todownloadlinklist.append(self.appendTuple)
                print(self.appendTuple)
                self.appendTuple = tuple()


        elif data == "Other":
            # TODO: ADD TUPLE OTHER
            if self.appendTuple not in todownloadlinklist and self.appendTuple is not tuple():
                self.appendTuple = self.appendTuple + tuple(('Other',))
                todownloadlinklist.append(self.appendTuple)
                print(self.appendTuple)
                self.appendTuple = tuple()
            print(self.appendTuple)

        elif data == "Female":
            # TODO: ADD TUPLE FEMALE
            if self.appendTuple not in todownloadlinklist and self.appendTuple is not tuple():
                self.appendTuple = self.appendTuple + tuple(('Female',))
                todownloadlinklist.append(self.appendTuple)
                print(self.appendTuple)
                self.appendTuple = tuple()
            print(self.appendTuple)
        else:
            pass


def getdownloadimage(href):
    baselink = "https://www.planetminecraft.com"
    downloadpage = requests.get(baselink + href, headers=headers)
    parse = parsehtml_2()
    parse.feed(downloadpage.content.decode())


def downloadlist(links):
    print(links)
    for link in links:
        image_url = planetmc_raw + link[0]
        aws_rawimageurl = ""
        print(link)
        imagerequest_s1 = requests.get(image_url, headers=headers, allow_redirects=True)

        if link[1] == 'Male' or link[1] == 'Other':
            imagelink_split = link[0].split('/')
            print(imagelink_split)
            with open(f'download/male_or_other_skins/{imagelink_split[2]}{imagelink_split[-2]}-{link[1]}.png', 'wb') as out_file:
                out_file.write(imagerequest_s1.content)
                out_file.close()

        elif link[1] == 'Female':
            imagelink_split = link[0].split('/')
            with open(f'download/female_skins/{imagelink_split[2]}{imagelink_split[-2]}-{link[1]}.png', 'wb') as out_file:
                out_file.write(imagerequest_s1.content)
                out_file.close()


print("""
egirl_detect_dc_bot webscraper  Copyright (C) 2020-2021  l1npengtul Rho
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.
""")

for i in range(10000):
    webHTML = requests.get(f'{planetmc}{i+1}', headers=headers)
    parse = parsehtml_1()
    parse.feed(webHTML.content.decode())
    for link in taglist:
        getdownloadimage(link)
    downloadlist(todownloadlinklist)
    # So turns out im a dumb ass
    # I didn't reset these checking lists
    # So the program would get slower by 2^X every for loop iteration
    # Bruh Momento
    todownloadlinklist = []
    taglist = []
    linklist = []
