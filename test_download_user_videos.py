from downloader import download_user_videos
     
def test_download_user_videos():
    username = 'Baselrajab'
    download_user_videos(username, screenshot=None, videos_count=1)
