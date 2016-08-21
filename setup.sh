## install python, pip, mongodb, ratebeer, scipy, pymongo, git?
sudo -su

# install scipy distro
sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose

# install mongodb
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927

sudo apt-get update
sudo apt-get install -y mongodb-org

pip install ratebeer
pip install pymongo

# run mongo daemon
mongod
