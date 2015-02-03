import requests
import csv
import argparse
import lxml.html

BASE_URL = "http://socialblade.com/instagram/top/100/followers"

def get_instagram_list(BASE_URL):
    root = make_request(BASE_URL)
    names = root.xpath("//div[@class='table-cell']/a")
    return (a.get("href").split("user/")[1] for a in names)

def make_request(url):
    headers = { 'User-Agent' : '"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"' }
    response = requests.get(url)
    return lxml.html.fromstring(response.content)

def get_list_with_name():
    urls = get_instagram_list(BASE_URL)
    for url in urls:
        print "http://instagram.com/{}/".format(url)

def get_twitter(url):
    root = make_request(url)
    links = root.xpath("//h3[@class='r']/a/@href")
    for link in links:
        if "twitter.com" in link:
            return link.split("twitter.com")[1].split("&")[0]
    return None

def get_twitter_list():
    goog_url = "https://www.google.com/search?safe=off&biw=1359&bih=598&noj=1&site=webhp&source=hp&q={}+twitter"
    file = open("celebs.txt", "r")
    a = csv.reader(file)
    for user in a:
        url = goog_url.format("+".join(user[1].strip().split(" ")))
        print get_twitter(url)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--twitter', action='store_true')
    args = parser.parse_args()

    if args.twitter:
        get_twitter_list()

    else:
        get_list_with_name()
