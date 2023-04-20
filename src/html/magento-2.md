## Installation

See [[Ref]].

Summary:

```

 mysql -u magento2 -p




16  sudo systemctl restart apache2
   19  sudo systemctl reload apache2


83  sudo a2ensite localhost.com.conf
   84  systemctl reload apache2

102  sudo vim /etc/php/8.1/apache2/php.ini
 111  sudo cat /var/log/apache2/error.log
 112  sudo cat /var/log/apache2/access.log
 113  sudo vim /etc/apache2/sites-available/localhost.com.conf 
 119  sudo chown -R james:www-data oops.html
```


```
sudo apt install ssl-cert
sudo make-ssl-cert /usr/share/ssl-cert/ssleay.cnf /etc/ssl/private
# -- Created ssl-cert-snakeoil.key in /etc/ssl/private and put 
                     /etc/ssl/certs/ssl-cert-snakeoil.pem

Add a virtual host for this and you're setl

https://superuser.com/questions/1740221/can-i-make-firefox-automatically-trust-self-signed-certs-for-a-given-hostname-ip


apache2ctl status # needs lynx installed
apache2ctl start

```



```
php bin/magento setup:install --base-url=https://localhost.com --db-host=localhost --db-name=magento2 --db-user=magento2 --db-password=james --admin-firstname=Admin --admin-lastname=Admin --admin-email=admin@admin.com --admin-user=admin --admin-password=james123 --language=en_US --currency=USD --timezone=America/Chicago --backend-frontname=admin --search-engine=elasticsearch7 --elasticsearch-host=localhost --elasticsearch-port=9200


sudo php bin/magento cache:clean config

```


```
cd /var/www/html/magento2
php bin/magento admin:user:create --admin-user=admin --admin-password=admin123
```


```


    1. After Magento Installation, you should set the developer mode by this command

php bin/magento deploy:mode:set developer

By setting Developer Mode, Errors are displayed in the browser and can be seen by users.

    2. You can check the errors for var/log and var/reports folder

```