import re
import json
import logging
import requests
import argparse
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By


class LikeeDownloader:

    def __init__(self, args):
        self.option = webdriver.FirefoxOptions()
        self.option.add_argument('--headless')
        self.driver = webdriver.Firefox(options=self.option)
        self.program_version_number = "2022.1.0.0"
        self.user_profile_url = "https://likee.video/@{}"
        self.user_videos_api_endpoint = "https://api.like-video.com/likee-activity-flow-micro/videoApi/getUserVideo"
        self.update_check_endpoint = "https://api.github.com/repos/rly0nheart/Likee-Downloader/releases/latest"


    def notice(self):
        notice_msg = f"""
    Likee-Downloader {self.program_version_number} Copyright (C) 2022  Richard Mwewa

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    """
        return notice_msg


    def check_and_get_updates(self):
        print(self.notice())
        response = requests.get(self.update_check_endpoint).json()
        if response['tag_name'] == self.program_version_number:
            """Ignore if the program is up to date"""
            pass
        else:
            update_prompt = input(f"[?] A new release is available ({response['tag_name']}). Would you like to install it? (y/n) ")
            if update_prompt.lower() == "y":
                files_to_update = ['downloader.py', 'geckodriver.exe', 'README.md', 'requirements.txt']
                for file in tqdm(files_to_update, desc=f'Updating'):
                    data = requests.get(f'https://raw.githubusercontent.com/rly0nheart/Likee-Downloader/master/{file}')
                    with open(file, "wb") as f:
                        f.write(data.content)
                        f.close()
                exit(f"Updated: Re-run program.")
            else:
                pass


    def capture_screenshot(self):
        print("\n[~] Capturing profile screenshot:", args.username)
        self.driver.get(self.user_profile_url.format(args.username))
        self.driver.get_screenshot_as_file(f"downloads/screenshots/{args.username}_likee-downloader.png")
        print(f"[~] Captured: downloads/screenshots/{args.username}_likee-downloader.png")


    def get_user_id(self):
        print("\n[~] Obtaining userId (This may take a while)...", end='')
        response = requests.get(f"{self.user_profile_url.format(args.username)}/video/{self.get_user_videoId()}")
        regex_pattern = re.compile('window.data = ({.*?});', flags=re.DOTALL | re.MULTILINE)
        str_data = regex_pattern.search(response.text).group(1)
        json_data = json.loads(str_data)
        payload = {"country": "US",
                   "count": 100,
                   "page": 1,
                   "pageSize": 28,
                   "tabType": 0,
                   "uid": json_data['uid']
                   }
        print("\n[+] userId obtained:", json_data['uid'])
        return payload

    
    def get_user_videoId(self):
        self.driver.get(self.user_profile_url.format(args.username))
        """
        In order to get the videoId, we have to click on a video,
        in this case we click on the first video
        """
        first_video_element = self.driver.find_element(By.XPATH, '//div[@class="card-video poster-bg"]')
        first_video_element.click()
        video_id = self.driver.current_url[-19:]
        self.driver.quit()
        return video_id

    
    def download_user_videos(self):
        self.check_and_get_updates()
        if args.screenshot:
            self.capture_screenshot()

        response = requests.post(self.user_videos_api_endpoint, json=self.get_user_id()).json()
        videos = response['data']['videoList']
        print(f'\n[+] Found {len(videos)} videos\n')
        downloaded_videos = 0
        for video in videos[:10]:
            # Printing video information
            print(video['msgText'])
            for video_key, video_value in video.items():
                print(f"├─ {video_key}: {video_value}")
            downloaded_videos += 1
            response = requests.get(video['videoUrl'], stream=True)
            with open(f"downloads/videos/{args.username}_{video['postId']}.mp4", "wb") as file:
                for chunk in tqdm(response.iter_content(chunk_size=1024 * 1024), desc=f"Downloading: {video['postId']}.mp4"):
                    if chunk:
                        file.write(chunk)

            print(f"Downloaded: {file.name}\n")
        print(f"[+] Complete: {downloaded_videos}/{len(videos)} videos were downloaded.")


parser = argparse.ArgumentParser(description='Likee-Downloader — by Richard Mwewa ')
parser.add_argument('username', help='specify target username')
parser.add_argument('-s', '--screenshot', help='capture a screenshot of the target\'s profile', action='store_true')
parser.add_argument('-d', '--debug', help='enable debug mode', action='store_true')
parser.add_argument('-v', '--version', version='2022.1.0.0', action='version')
args = parser.parse_args()
if args.debug:
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%I:%M:%S%p', level=logging.DEBUG)
else:
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%I:%M:%S%p', level=logging.INFO)  

if __name__ == "__main__":
    try:
        LikeeDownloader(args).download_user_videos()

    except KeyboardInterrupt:
        logging.warning("Process interrupted with Ctrl+C.")

    except Exception as e:
        logging.error(e)
