from download import Download

if __name__ == '__main__':
    url = 'https://www.aparat.com/v/ul3Sx/'
    quality = '144'
    download = Download(url, quality)
    download.start()
