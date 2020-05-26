# CoinAPI Demo Andela Challenge

A simple web app that displays volume of coins trades for each of BTC, LTC, ETH and XRP

Live url here >>>>> https://coinapichart.imfast.io/

### Tech

Technologies used:

* HTML/JS 
* Python/Flask 
* PostgreSql 
* Google Analytics

### Installation

Application requires [Python3](https://www.python.org/download/releases/3.0/) and [PostgreSql](https://www.postgresql.org/) to run.

clone the repository
```sh
git clone https://github.com/ayomidearo/andela-code-challenge-app && cd andela-code-challenge
```
run `pip3 install -r requirements.txt` to install the dependencies of the project

Kindly create a database in your postgres instance with any name of your choice as it would be used in your `.env` file

Inside the project directory, there is a `sample.env` file, kindly copy the content and create a new `.env` inside the directory and replace `db_host`, `db_user`, `db_name`, `db_pass` with your credentials

`db_name` is the database you created earlier.

Once this is setup, kindly run `python3 setup.py` to create the necessary tables.

After that, you run the script to fetch data from CoinAPI.co and save to database. 
Allowed coins  - BTC, LTC, XRP, ETH

run `python3 fetcher.py --apikey [YOUR_COINAPI_KEY] --crypto [CRYPTO ASSET ID FROM ANY ABOVE]`

e.g `python3 fetcher.py --apikey myapikey --crypto BTC` to get data for BTC and save.

DO the same for the remaining coins. Once that is set, we can now run our mini flask api with `python3 app.py`

Your flask app should run on port `5000` and the api can be accessed with `http://localhost:5000/get_historical_data?asset_id=` any of BTC, LTC, ETH and XRP

The api returns the data for any of the crypto currency.

Still in the project directory, run `cd frontend` and you'd see two files; `index.html` and `index.js`, inside the `index.js` file, replace the url at the top of the file with your api url running. Also, replace the tracking number for GA inside the `index.html` file with your own trackiig number to enable GA event tracking

Once that is replaced, you can open the `index.html` in any browser of your choice to select each coin and view respective charts.


## Any questions?

You can reach me on <skilashiaro@gmaill.com>
