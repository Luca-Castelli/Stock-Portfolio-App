## Stock Porfolio App

Stock Porfolio App is a platform where users can register an account and input buy/sell/dividend transactions. The back-end compiles all transactions to build a portfolio of holdings. Metrics likes cost basis and performance are calculated.

## Technology Used

Full stack application split into 3 docker containers:

- Database: Postgres
- Sever: Python Flask
- Front-end: React.js

Dev and prod environments configured with seperate entrypoint.sh, dockerfiles, and databases ready to go.

- Dev: on startup entrypoint.sh clears, creates, and seeds a dev database.
- Prod: on startup entrypoint.prod.sh does not disrupt existing prod database. Prod uses NGINX to handle proxying.

Data sources:

- IEX API: financial data
- Yahoo Finance scraping: financial data

## GIF Demos

![picture_index](demo/index.PNG)

Users can add buy and sell transactions.
![gif_of_add_trades](demo/add_trades.gif)

Users can add dividend transactions.
![gif_of_add_divdend](demo/add_dividend.gif)

Dyanmic stock ticker search for all US and Canadian-listed securities.
![gif_of_ticker_search](demo/ticker_search.gif)

Handling of multiple accounts, allowing users to track a seperate cost basis for each account.
![gif_of_handling_of_accounts](demo/handling_of_accounts.gif)

Both the Holdings and Trade Log tables are sortable, making it easy for users to view data the way they like.
![gif_of_sorting](demo/sorting.gif)
