import os
import requests
import re
import matplotlib
matplotlib.use('Agg')  # Set matplotlib to use a non-GUI backend
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bS
from wordcloud import WordCloud
from PIL import Image
import shutil

# Static directory path
STATIC_DIR = os.path.join('static')

# First image generation (Word Cloud)
def text_scraping(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to retrieve the page: {response.status_code}")
    
    s = bS(response.text, 'html.parser')
    print("Text scraping successful.")

    joint_i = " "
    for i in s.find_all("p"):
        joint_i += i.text
    return wordcld(joint_i)

def wordcld(text):
    processed_text = re.sub(r'[^\w\s]', '', text.lower())
    print("Generating word cloud.")

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(processed_text)
    print("Word cloud generated.")

    # Save the word cloud as an image in the static folder
    wordcloud_image_path = os.path.join(STATIC_DIR, 'wordcloud_image.png')
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(wordcloud_image_path)
    plt.close()
    
    return 'wordcloud_image.png'

# Second image generation (Image Scraping)
class Folder:
    def __init__(self, base_path=None):
        self.base_path = base_path

    def create_folder(self):
        path = self.base_path if self.base_path else "."
        folder_path = os.path.join(path, "temp_folder_2")
        os.makedirs(folder_path, exist_ok=True)
        return "temp_folder_2"

    def remove_folder(self):
        path = self.base_path if self.base_path else "."
        folder_path = os.path.join(path, "temp_folder_2")
        shutil.rmtree(folder_path, ignore_errors=True)

def convert_image(image_path, folder_name, i):
    image = Image.open(image_path)
    image = image.convert('RGBA')
    converted_image_path = os.path.join(folder_name, f'converted_image_{i}.png')
    image.save(converted_image_path)

def display_images_in_subplots(folder_name):
    image_files = [f for f in os.listdir(folder_name) if f.startswith("converted_image")]
    cols = 5
    rows = (len(image_files) + cols - 1) // cols
    fig, axs = plt.subplots(cols, rows, figsize=(10, 5))
    axs = axs.flatten()

    for i, img_name in enumerate(image_files):
        img_path = os.path.join(folder_name, img_name)
        image = plt.imread(img_path)
        axs[i].imshow(image)
        axs[i].axis('off')

    # Hide any extra subplots
    for j in range(i + 1, len(axs)):
        axs[j].axis('off')

    plt.tight_layout()
    subplot_image_path = os.path.join(STATIC_DIR, 'scraped_images.png')
    plt.savefig(subplot_image_path)
    plt.close()
    
    return 'scraped_images.png'

def image_scraping(link):
    folder = Folder()
    folder.remove_folder()
    response = requests.get(link)
    s = bS(response.text, 'html.parser')

    img_urls = []
    for img_tag in s.find_all("img"):
        src = img_tag.get("src")
        if src:
            if src.startswith('http'):
                img_urls.append(src)
            elif src.startswith('/'):
                img_urls.append('https:' + src)
            else:
                img_urls.append('https://' + src)

    folder_name = folder.create_folder()

    for j, img_url in enumerate(img_urls):
        try:
            response = requests.get(img_url)
            img_path = os.path.join(folder_name, f"img_{j}.png")
            with open(img_path, "wb") as file:
                file.write(response.content)
        except requests.RequestException as e:
            print(f"Error fetching image {img_url}: {e}")

    for i, img_file in enumerate(os.listdir(folder_name)):
        try:
            img_path = os.path.join(folder_name, img_file)
            convert_image(img_path, folder_name, i)
        except Exception as e:
            print(f"Error processing image {img_file}: {e}")

    scraped_image_path = display_images_in_subplots(folder_name)
    folder.remove_folder()

    return scraped_image_path