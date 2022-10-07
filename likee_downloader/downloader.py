import re
import os
import json
import requests
import argparse
from tqdm import tqdm
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class LikeeDownloader:
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='likee-downloader — by Richard Mwewa', epilog='A program for downloading videos from Likee, given a username')
        self.parser.add_argument('username', help='username')
        self.parser.add_argument('-s', '--screenshot', help='capture a screenshot of the target\'s profile', action='store_true')
        self.parser.add_argument('-c', '--videos-count', help='number of videos to download (default: %(default)s)', default=10, dest='videos_count', type=int)
        self.args = self.parser.parse_args()

        option = webdriver.FirefoxOptions()
        option.add_argument('--headless')
        self.driver = webdriver.Firefox(options=option)
        
        self.program_version_number = "2022.1.3.1"
        self.user_profile_url = "https://likee.video/@{}"
        self.user_videos_api_endpoint = "https://api.like-video.com/likee-activity-flow-micro/videoApi/getUserVideo"
        self.update_check_endpoint = "https://api.github.com/repos/rly0nheart/likee-downloader/releases/latest"
        
    def notice(self):
        notice_msg = f"""
    likee-downloader {self.program_version_number} Copyright (C) 2022  Richard Mwewa
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
    """
        print(notice_msg)
        
        
    def check_updates(self):
        self.notice()
        response = requests.get(self.update_check_endpoint).json()
        if response['tag_name'] == self.program_version_number:
            """Ignore if the program is up to date"""
            pass
        else:
            print(f"[!] A new release is available ({response['tag_name']}). Run 'pip install --upgrade likee-downloader' to get the updates.\n")
            
            
    def capture_screenshot(self):
        print("Capturing profile screenshot:", self.args.username)
        self.driver.get(self.user_profile_url.format(self.args.username))
        self.driver.get_screenshot_as_file(f"downloads/screenshots/{self.args.username}_likee-downloader.png")
        print(f"Captured: downloads/screenshots/{self.args.username}_likee-downloader.png")
        
        
    def get_user_id(self):
        print("Obtaining userId (This may take a while)...")
        response = requests.get(f"{self.user_profile_url.format(self.args.username)}/video/{self.get_user_videoId()}")
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
        print(f"userId obtained: {json_data['uid']}")
        return payload, json_data['uid']
        
        
    def get_user_videoId(self):
        self.driver.get(self.user_profile_url.format(self.args.username))
        """
        Wait for 20 seconds for an element matching the given criteria to be found (we wait for the page to be fully loaded)
        In order to get the videoId, we have to click on a video,
        in this case we click on the first video
        """
        first_video_element = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '//div[@class="card-video poster-bg"]')))
        first_video_element.click()
        video_id = self.driver.current_url[-19:]
        self.driver.quit()
        return video_id
        
        
    def path_finder(self):
        directory_list = ['downloads/videos', 'downloads/screenshots']
        for directory in directory_list:
            os.makedirs(directory, exist_ok=True)
            
            
    def download_user_videos(self):
        try:
            self.check_updates()
            self.path_finder()
            
            if self.args.screenshot:
                self.capture_screenshot()
                
            response = requests.post(self.user_videos_api_endpoint, json=self.get_user_id()[0]).json()
            videos = response['data']['videoList']
            print(f'Found: {len(videos)} videos\n')
            downloaded_videos = 0
            downloading_videos = 0
            for video in videos[:self.args.videos_count]:
                downloading_videos += 1
                pprint(video)
                """
                Downloading video and saving it by the username_postId format
                """
                downloaded_videos += 1
                response = requests.get(video['videoUrl'], stream=True)
                with open(f"downloads/videos/{self.args.username}_{video['postId']}.mp4", "wb") as file:
                    for chunk in tqdm(response.iter_content(chunk_size=1024 * 1024), desc=f"Downloading {downloading_videos}/{self.args.videos_count}: {video['postId']}.mp4"):
                        if chunk:
                            file.write(chunk)
                print(f"Downloaded: {file.name}\n")
            print(f"Complete!")
                
        except KeyboardInterrupt:
            print("Process interrupted with Ctrl+C.")
            
        except Exception as e:
            print("An error occured:", e)

