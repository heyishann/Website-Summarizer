from flask import Flask, render_template, request, url_for
import os
from image_generator import text_scraping, image_scraping

app = Flask(__name__)

# Folder to store generated images
STATIC_DIR = os.path.join('static')

@app.route('/')
def home():
    return render_template('index.html', image1=None, image2=None)

@app.route('/generate', methods=['POST'])
def generate():
    url = request.form['url']
    
    # Generate two images
    wordcloud_image = text_scraping(url)
    scraped_images = image_scraping(url)

    return render_template('index.html', image1=wordcloud_image, image2=scraped_images)

if __name__ == '__main__':
    app.run(debug=True)
