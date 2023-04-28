## Intro

An almost Raspberry Pi 3 replacement. Notably no WiFi, but at least I could buy one at the moment,
as rPi's are like gold dust...

![High level board diagram with pinout for Le Potatoe SBC](##IMG_DIR##/le-potatoe-board-diagram-pinouts.png)
[[Ref]](https://docs.google.com/spreadsheets/d/1U3z0Gb8HUEfCIMkvqzmhMpJfzRqjPXq7mFLC-hvbKlE/edit#gid=0)

## Installing Ubuntu 18 (Bionic)

Download the file [`libre-computer-aml-s905x-cc-ubuntu-bionic-headless-4.19.55+-2019-06-24.zip`](http://share.loverpi.com/board/libre-computer-project/libre-computer-board-aml-s905x-cc/image/ubuntu/).

Use `gnome-disks` [[Ref]](https://support.endlessos.org/en/installation/flash-gnome-disks) or any other program of your choosing to write to an SD card, then insert into
the board. Power up.

Default login should be [[Ref]](http://wiki.loverpi.com/tutorial:sbc:libre-aml-s905x-getting-started):

```
Username: libre
Password: computer
```

## GPIO

Examples taken from [Libre Computer Tutorial](https://hub.libre.computer/t/how-to-control-gpio-via-python-3/601).


