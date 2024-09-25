import os
import requests
import time
from urllib.parse import urlparse


url = 'https://storage.googleapis.com/panels-api/data/20240916/media-1a-i-p~s'
DOWNLOAD_DIR = 'downloads'

def download_image(image_url, file_path):
    response = requests.get(image_url)
    if response.status_code != 200:
        print(f"⛔ Failed to download image: {response.status_code} - {response.text}")
        return

    with open(file_path, 'wb') as f:
        f.write(response.content)

def print_progress_bar(iteration, total, length=40):
    percent = (iteration / total) * 100
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\r|{bar}| {percent:.2f}%', end='', flush=True)

def main():
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
        print(f"📁 Created directory: {DOWNLOAD_DIR}")

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"⛔ Failed to fetch JSON file: {response.status_code} - {response.text}")
            return

        json_data = response.json()
        data = json_data.get('data')
        if not data:
            print('⛔ JSON does not have a "data" property at its root.')
            return

        total_images = sum(1 for subproperty in data.values() if subproperty and 'dhd' in subproperty)

        file_index = 1
        for key, subproperty in data.items():
            if subproperty and 'dhd' in subproperty:
                image_url = subproperty['dhd']

                parsed_url = urlparse(image_url)
                base_filename = os.path.basename(parsed_url.path)
                filename = f"{file_index}_{base_filename}"
                file_path = os.path.join(DOWNLOAD_DIR, filename)

                download_image(image_url, file_path)
                print_progress_bar(file_index, total_images)

                file_index += 1
                time.sleep(0.25)

        print("\n✅ Download complete!")
        
    except KeyboardInterrupt:
        print(f"\n✖️ Download cancelled!")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    print("🤑 Starting downloads from the image API...")
    time.sleep(2)
    main()
