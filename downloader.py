import os
import shutil
import errno
import argparse
import requests
from clint.textui import progress
from bs4 import BeautifulSoup

# Grab all of the image links that are on a thread
def get_all_img_links(thread_link):
    r = requests.get(thread_link)
    soup = BeautifulSoup(r.text, "html.parser")
    img_elems = soup.find_all("a", class_="fileThumb")
    img_links = list(map(lambda i: "https:{}".format(i['href']), img_elems))
    return img_links

# Extract the name of the actual *.{png, jpg} file from a link
def extract_img_name(img_link):
    return img_link.split('/')[-1]

# Attempt to create a directory and return True if it succeeded, else False
def create_dir(dirname):
    try:
        os.makedirs(dirname)
        return True
    except OSError as err:
        return err.errno == errno.EEXIST  # If the directory already exists, we're good
    except:
        return False

# Downloads and returns the raw image data from a given link
def download_img_data(img_link):
    return requests.get(img_link, stream=True).raw

# Writes raw image data to a given location
def write_img_data(img_data, loc):
    with open(loc, "wb") as f:
        shutil.copyfileobj(img_data, f)

# Download all images from a thread to a destination
def main(thread_link, dest_dir):
    img_links = get_all_img_links(thread_link)
    res = create_dir(dest_dir)
    if not res:
        return
    for i in progress.bar(range(len(img_links))):
        img_link = img_links[i]
        img_data = download_img_data(img_link)
        img_loc = "{}/{}".format(dest_dir, extract_img_name(img_link))
        write_img_data(img_data, img_loc)

if __name__ == "__main__":
    # Parse commandline arguments
    parser = argparse.ArgumentParser(description="Download all images from a 4chan thread")
    parser.add_argument("-thread", type=str, help="The link where the images are located", dest="thread_link")
    parser.add_argument("-dest", type=str, help="Directory to place the downloaded images", dest="dest_dir")
    args = parser.parse_args()

    # Run the downloader
    thread_link = args.thread_link
    dest_dir = args.dest_dir
    main(thread_link, dest_dir)
