# Shop Bot  
  
## About bot  
It is a telegram bot for searching for items in online shops. Now only three shops are available: Aliexpress, Lamoda and Wildberries. User can see the available shop list and search items in all available shops or only in some of them. Also user can change the number of items in the results of the search. This number can be different for different shops.  
  
## Installation  
1. Clone this repo
```
git remote add origin https://github.com/sivalien/shop_bot
```
2. Install required packages: selenium, pyTelegramBotAPI, BeatifulSoup and requests  
```
pip install selenium
pip install pyTelegramBotAPI  
pip install bs4  
pip install requests
```
3. Set up required fields:
- `TOKEN` - the Telegram Bot Token that you got from @BotFather, you can set up it with the following command:
```
export TOKEN="your token"
```
- `CHROME_DRIVER_PATH` - path to chrome driver that you can install for [chrome](https://sites.google.com/chromium.org/driver/), you can move driver to /usr/bin folder (for MacOS) and remove this variable from config.py and all shop models files or just write your path to chromedriver in this variable in config.py.  
  
## Testing  
- install pytest  
```
pip install pytest
```
- run tests    
```
pytest telegram_bot/tests.py
```  
  
## Running  
For runnig this bot just enter following command  
```
python main.py
```
  
## A few words about implementation  
There is an abstract class shop with absract methods `get_items` which returns results of searching item and `_get_source_page` which returns the source page for searching request in online shop. Every class corresponding to online shop is inherited from abstract class shop, contains link to online shop main page and implementes the singleton pattern. Abstract class shop has method name which returns the name of the class. Shop instance is equal to its name due to the `__eq__` method implementation, also they have the same hash for storing in the dictionary shops and getting the shop instance by its name.
