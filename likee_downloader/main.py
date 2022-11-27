from likee_downloader.downloader import LikeeDownloader


def downloader():
    try:
        start = LikeeDownloader()
        start.download_user_videos()
    
    except KeyboardInterrupt:
        print('[CTRLC] Process interrupted with Ctrl+C.')

    except Exception as e:
        print('[ERROR] An error occured:', e)
