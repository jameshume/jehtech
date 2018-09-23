# JEH Tech
Just notes on various subjects.

Ignore the Git history and commit messages. I'm using this more as shared storage than source
control!

---

You will need NodeJS. On Ubuntu:

```
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs
```

Next install the package manager
```
sudo apt-get install -y npm
```

Then install the `mathjax-node-page` module so that we can pre-render
mathjax.

```
sudo npm install mathjax-node-page
```

Then I found I needed the latest node version so...

```
sudo npm install -g n
sudo n latest
```

But, then later on I got this error message for some reason:
```
SyntaxError: Block-scoped declarations (let, const, function, class) not yet supported outside strict mode
```

The answer is that you need to upgrade nodejs. Use `sudo apt-get remove nodejs` to uninstall, then
download nodejs from `https://nodejs.org/dist/v9.9.0/` (use the latest), untar somewhere and put the
`bin` directory on your path.

```
# Install NodeJS
cd the-unzipped-nodejs-you-downloaded
sudo cp -R * /usr/local/
sudo npm install mathjax-node-page
```

Also might need to do some other installs:
```
# Install required python packages
sudo pip3 install lxml

# Install Java
sudo add-apt-repository ppa:linuxuprising/java
sudo apt update
sudo apt install oracle-java10-installer
sudo apt install oracle-java10-set-default

# Install fonts (unlikely you'll need to!)
sudo apt-get install ttf-mscorefonts-installer
sudo fc-cache
```
