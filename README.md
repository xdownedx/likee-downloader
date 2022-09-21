# Likee Downloader
A script for downloading videos from Likee

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
> *This will install tqdm and selenium*
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
| *-d/--debug* | enable debug mode |
| *-v/--version*   | show program's version number and exit |
