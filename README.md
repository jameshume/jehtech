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