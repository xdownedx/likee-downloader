# Likee Downloader
[![CodeQL](https://github.com/rly0nheart/likee-downloader/actions/workflows/codeql.yml/badge.svg)](https://github.com/rly0nheart/likee-downloader/actions/workflows/codeql.yml)  [![Upload Python Package](https://github.com/rly0nheart/likee-downloader/actions/workflows/python-publish.yml/badge.svg)](https://github.com/rly0nheart/likee-downloader/actions/workflows/python-publish.yml)

A program for downloading videos from Likee, given a username

![screenshot](https://user-images.githubusercontent.com/74001397/191549849-07f151c5-4f42-4c71-ae9c-ceabe24c54d3.png)

# Installation
**Install from PyPI**
```
pip install likee-downloader
```

### Note
> In order to run the program, You will need to have the FireFox browser installed on your pc
> The program is dependent on selenium, so in order to run it, you will have to download and properly setup geckodriver (setup instructions available below)
>> 

# Geckodriver setup
## Linux
**1. Go to the geckodriver [releases page](https://github.com/mozilla/geckodriver/releases/). Find the latest version of the driver for your platform and download it**

**2. Extract the downloaded file**
```
tar -xvzf geckodriver*
```

**3. Make it executable**
```
chmod +x geckodriver
```

**4. Add geckodriver to your system path**
```
export PATH=$PATH:/path/to/downloaded/geckodriver
```

### Note
> If you encounter issues with the above commands, then you should run them as root (with sudo)


## Windows
**1. Go to the geckodriver [releases page](https://github.com/mozilla/geckodriver/releases/). Find the geckodriver.exe binary for your platform and download it**

**2. Move the downloaded executable to** *C:\Users\yourusername\AppData\Local\Programs\Python\Python310*

### Note
> The numbers on the directory 'Python310' will depend on the version of Python you have

## Mac OS
* [Set up Selenium & GeckoDriver (Mac)](https://medium.com/dropout-analytics/selenium-and-geckodriver-on-mac-b411dbfe61bc)


# Usage
```
likee_downloader <username>
```

### Note
> Upon run, the program will first check for updates. If found, users will be notified about the update


# Optional Arguments
| Flag | Description |
|---------|:-----------:|
| *-s/--screenshot* | capture a screenshot of the target's profile (bonus feature) |
| *-c/--videos-count* | number of videos to download (default: 10) |

# Donations
If you would like to donate, you could Buy A Coffee for the developer using the button below

<a href="https://www.buymeacoffee.com/189381184" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

Your support will be much appreciated!
