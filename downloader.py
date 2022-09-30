import re
import json
import requests
import argparse
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By


option = webdriver.FirefoxOptions()
option.add_argument('--headless')
driver = webdriver.Firefox(options=option)
program_version_number = "2022.1.0.0"
user_profile_url = "https://likee.video/@{}"
user_videos_api_endpoint = "https://api.like-video.com/likee-activity-flow-micro/videoApi/getUserVideo"
update_check_endpoint = "https://api.github.com/repos/rly0nheart/Likee-Downloader/releases/latest"


def notice():
    notice_msg = f"""
Likee-Downloader {program_version_number} Copyright (C) 2022  Richard Mwewa

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""
    print(notice_msg)


def check_and_get_updates():
    notice()
    response = requests.get(update_check_endpoint).json()
    if response['tag_name'] == program_version_number:
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
            print(f"Updated: Re-run program.");exit()
        else:
            pass


def capture_screenshot(username):
    print("Capturing profile screenshot:", username)
    driver.get(user_profile_url.format(username))
    driver.get_screenshot_as_file(f"downloads/screenshots/{username}_likee-downloader.png")
    print(f"Captured: downloads/screenshots/{username}_likee-downloader.png")


def get_user_id(username):
    print("Obtaining userId (This may take a while)...")
    response = requests.get(f"{user_profile_url.format(username)}/video/{get_user_videoId(username)}")
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
    return payload


def get_user_videoId(username):
    driver.get(user_profile_url.format(username))
    """
    In order to get the videoId, we have to click on a video,
    in this case we click on the first video
    """
    first_video_element = driver.find_element(By.XPATH, '//div[@class="card-video poster-bg"]')
    first_video_element.click()
    video_id = driver.current_url[-19:]
    driver.quit()
    return video_id

 
def download_user_videos(username, screenshot):
    if screenshot:
        capture_screenshot()

    response = requests.post(user_videos_api_endpoint, json=get_user_id(username)).json()
    videos = response['data']['videoList']
    print(f'Found {len(videos)} videos\n')
    downloaded_videos = 0
    for video in videos[:10]:
        # Printing video information
        print(video['msgText'])
        for video_key, video_value in video.items():
            print(f"├─ {video_key}: {video_value}")
        downloaded_videos += 1
        response = requests.get(video['videoUrl'], stream=True)
        with open(f"downloads/videos/{username}_{video['postId']}.mp4", "wb") as file:
            for chunk in tqdm(response.iter_content(chunk_size=1024 * 1024), desc=f"Downloading: {video['postId']}.mp4"):
                if chunk:
                    file.write(chunk)

        print(f"Downloaded: {file.name}\n")
    print(f"Complete: {downloaded_videos}/{len(videos)} videos were downloaded.")


parser = argparse.ArgumentParser(description='Likee-Downloader — by Richard Mwewa ')
parser.add_argument('username', help='specify target username')
parser.add_argument('-s', '--screenshot', help='capture a screenshot of the target\'s profile', action='store_true')
parser.add_argument('-v', '--version', version='2022.1.0.0', action='version')
args = parser.parse_args()
username = args.username
screenshot = args.screenshot

if __name__ == "__main__":
    try:
        #check_and_get_updates()
        download_user_videos(username, screenshot)

    except KeyboardInterrupt:
        print("Process interrupted with Ctrl+C.")

    except Exception as e:
        print("An error occured:", e)
