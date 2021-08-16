## setup the browser driver
curl https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-macos.tar.gz -o geckodriver.tar.gz
tar -zxvf geckodriver.tar.gz
xattr -d com.apple.quarantine $PWD/geckodriver

## install selenium
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
pip install selenium

