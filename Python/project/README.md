# Daily Stock News
#### Description:
This project is Python-based stock analysis tool that help identify potential trading opportunity by comparing current stock prices against historical medians and moving averages.
The program imports stock data, processes it into and Excel table and calculates various metrics such as percent changes, medians, moving averages and rankings.
The result allow investors or analysts to evaluate sotcks across different sectors and industries, highlighting companiues that may be undervalued or overpriced.


## Features
- Loads data from companies.json. It is pre-made json file holding 1000 biggest companies with their Ticker, Sector etc.
- Fetches stock price data (last close, pre-market price, history)
- Calcualtes key metrics - Percent change vs 1-year median, percent change vs 50-day SMA, Custom ranking scores across metrics
- Outputs results into a structured Excel fiel with clear column descriptions
- Provides sector and industry classification
- Flags if a company belongs to a major index (S&P 500)

## Functions

### load_companies()
- Load the companies list from a JSON file into a normalized DataFrame
- Args: Path to a JSON file  with shape {"companies": [{"ticker": "...", "sector": "...", ...}, ...]}
- Returns: pandas.DataFrame one row per company with a cleaned uppercase ticker

### fetch_prices_and_history()
- Fetch live-ish price fields and historical adjusted closes via yahooquery
- Args: Symbols to query, time period for history, optional interval for history
- Returns: tuple[pandas.DataFrame, pandas.DataFrame] prices_df and hist_df
- Missing fields and invalid values become NaN

### last_year_median_history()
- Compute per-ticker median closing price from history
- Args: history DataFrame
- Returns: pandas.Series

### sma_from_history()
- Compute per-ticker simple moving average over last window days
- Args: history DataFrame, optional window
- Returns: pandas.Series

### pct_change()
- Compute percentage change
- Args: New value, Baseline value
- Returns: pandas.Series

### build_dashboard
- Assemble the final ranking table by joining metadata, prices and signals
- Start from companies DataFrame, Adds live prices, compute percent changes, median, sma, ranking
- Args: Companies, prices, history dataframes, optional window
- Returns: DataFrame final dashboard table

### export_to_excel()
- Write the final DataFrame to an Excel workbook
- Args: DataFrame, path

### main()
- Orchestrate the end-to-end flow: load -> fetch -> compute -> export
- Args: Input JSON filename, Output Excel filename, SMA length
- Steps - Resovle paths, load Tickers, fetch current price fields and historical prices, build the dashboard, export results to Excel and print a short summary

## How to run
- Clone repository
- Install dependencies
- Place companies.json in the project directory
- Run the main script
- Open the generated Excel file to view results


