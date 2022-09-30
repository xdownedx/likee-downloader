# Likee Downloader
A script for downloading videos from Likee

![screenshot](https://user-images.githubusercontent.com/74001397/191549849-07f151c5-4f42-4c71-ae9c-ceabe24c54d3.png)

# Installation
**1. Clone the project**
```
git clone https://github.com/rly0nheart/Likee-Downloader.git
```

**2. Move to Likee-Downloader directory**
```
cd Likee-Downloader
```

**3. Install dependencies**
## Note
> *This will install tqdm and selenium, and requests*
> > *You will need to have Firefox installed to run the program*
> > > *For user convenience, the program will come with a geckodriver.exe binary*
```
pip install -r requirements.txt
```

# Usage
```
python downloader.py <username>
```

> *Alternatively, you could grant execution permission to the downloader and run it as shown below*

**1. Grant execution permission**
```
chmod +x downloader.py
```

**2. Run downloader**
```
./downloader.py <username>
```

## Note
> Upon run, the downloader will first check for updates. If found, users will be prompted to download the updates


# Optional Arguments
| Flag | Description |
|---------|:-----------:|
| *-s/--screenshot* | capture a screenshot of the target's profile (bonus feature) |
| *-v/--version*   | show program's version number and exit |

# Donations
If you would like to donate, you could Buy A Coffee for the developer using the button below

<a href="https://www.buymeacoffee.com/189381184" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

Your support will be much appreciated!
