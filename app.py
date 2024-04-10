from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import os
import urllib.parse
import shutil

app = Flask(__name__)

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        topic = request.form['genre']
        url = f"https://catalog.data.gov/dataset/?q={topic}"

        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        download_dir = os.path.join(os.getcwd(), "downloadStore")
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        elements = soup.find_all(class_="label-default")

        for count,element in enumerate(elements):
            if element.get_text().strip() in ["CSV","XML","JSON", "ZIP", "HTML"]:
                href = element.get("href")
                parsed_url = urllib.parse.urlparse(href)
                filename = f"{topic}_{count}_"+os.path.basename(parsed_url.path)
                file_path = os.path.join(download_dir, filename)
                download_file(href, file_path)
                print(f"Downloaded: {filename}")

        return "Scraping and downloading completed successfully!"
    except KeyboardInterrupt:
        return "Download interrupted by user"

@app.route('/files')
def files():
    download_dir = os.path.join(os.getcwd(), "downloadStore")
    files_list = os.listdir(download_dir)
    return render_template('files.html', files=files_list)

@app.route('/sort')
def sort_files():
    path = os.getcwd() + "/downloadStore/"
    path1 = os.getcwd() + "/sorting"
    files = os.listdir(path)

    for file in files:
        filename, extension = os.path.splitext(file)
        extension = extension[1:]

        if extension == "":
            if not os.path.exists(path1+'/others'):
                os.makedirs(path1+'/others')
            shutil.move(os.path.join(path, file), os.path.join(path1, 'others', file))
        else:
            if not os.path.exists(os.path.join(path1, extension)):
                os.makedirs(os.path.join(path1, extension))
            shutil.move(os.path.join(path, file), os.path.join(path1, extension, file))

    return "File sorting completed successfully!"

@app.route('/sorted_files')
def sorted_files():
    sorted_files_data = {}  # Dictionary to store sorted files data
    sorted_directory = os.getcwd() + "/sorting"  # Path to the directory containing sorted files

    # Iterate over directories in sorted directory
    for category in os.listdir(sorted_directory):
        category_path = os.path.join(sorted_directory, category)
        if os.path.isdir(category_path):
            files_list = os.listdir(category_path)
            sorted_files_data[category] = files_list
    
    return render_template('sorted_files.html', sorted_files=sorted_files_data)  # Corrected variable name

@app.route('/deleteDownloads')
def delete_downloads_directory():
    # if os.getcwd() + "/downloadStore" == True:
    folder_path = os.getcwd() + "/downloadStore"
    shutil.rmtree(folder_path)
    return "Download directory deleted successfully!"
    # else:
    #     return "No downloads found :)"

@app.route('/deleteSortedFiles')
def delete_sorted_directory():
    # if os.getcwd() + "/sorting" == True:
    folder_path = os.getcwd() + "/sorting"
    shutil.rmtree(folder_path)
    return "Download directory deleted successfully!"
    # else:
    #     return "Sorted Folder Not Found !"

if __name__ == '__main__':
    app.run(debug=True)
