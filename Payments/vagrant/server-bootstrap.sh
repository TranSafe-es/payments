sudo apt-get update
sudo apt-get install -y python python-pip python-dev python-lxml
sudo apt-get install -y libpq-dev
sudo pip install requests
sudo apt-get install -y redis-server
# sudo vim /etc/redis/redis.conf
#uncomment next lines and change the second to:
# unixsocket /var/run/redis/redis.sock
# unixsocketperm 770
#then:
# sudo usermod -a -G redis vagrant
# sudo service redis-server restart
cd /vagrant/Payments/src/
sudo pip install -r requirements.txt
