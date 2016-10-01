sudo apt-get update
sudo apt-get install -y python python-pip python-dev python-lxml
sudo apt-get install -y libpq-dev
sudo pip install requests
cd /vagrant/Payments/src/
sudo pip install -r requirements.txt
