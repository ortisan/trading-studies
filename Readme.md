# Trading Studies

## Installation

Installing python 3.10
```sh
sudo apt-get -y install gcc build-essential python3-dev
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
sudo apt install python3.10-venv
```

Installing virtual env
```sh
python3 -m pip install --user virtualenv
python3 -m venv env
sudo chmod -R a+rwx env
source env/bin/activate
```

Installing ta-lib
```sh
wget https://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
&& tar -xvf  ta-lib-0.4.0-src.tar.gz \
&& cd ta-lib \
&& sudo ./configure --prefix=/usr \
&& sudo make \
&& sudo make install \
&& cd ~ \
&& sudo rm -rf ta-lib/ \
&& python3 -m pip install install ta-lib
```
