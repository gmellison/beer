## install python, pip, mongodb, ratebeer, scipy, pymongo, git?
sudo -su

# install scipy distro
apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose

# install mongodb
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list

apt-get update
apt-get install -y mongodb-org

# install pip
apt-get install python-pip python-dev build-essential
pip install --upgrade pip
pip install --upgrade virtualenv

# install ratebeer (& depens) and pymongo
apt-get install -y libffi-dev
apt-get install -y libssl-dev

pip install requests
pip install beautifulsoup4
pip install lxml
git clone https://github.com/alilja/ratebeer
python ratebeer/setup.py install
pip install pymongo
