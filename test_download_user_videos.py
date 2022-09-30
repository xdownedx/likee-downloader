from downloader import download_user_videos
     
def test_download_user_videos():
    username = 'ulvaatkins'
    download_user_videos(username, screenshot=None)