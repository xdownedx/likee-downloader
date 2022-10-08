from likee_downloader.downloader import LikeeDownloader

def main():
    try:
        start = LikeeDownloader()
        start.download_user_videos()
    
    except KeyboardInterrupt:
        print('Process interrupted with Ctrl+C.')

    except Exception as e:
        print('An error occured:', e)