#Market trading bot with a built in simulator.

## Project Structure
The project will be organized as follows:
- `src/`: Main source code
  - `strategies/`: Trading strategy modules
  - `indicators/`: Technical indicator modules
  - `data/`: Data handling and processing
  - `simulation/`: Backtesting and simulation engine
  - `gui/`: Graphical user interface
- `tests/`: Unit and integration tests
- `docs/`: Documentation files
- `config/`: Configuration files

## MVP

Python

Modular

Multiple assets

Multiple indicators

Multiple strategies

Simulator

Historical data

Performance evaluation via account balance (cash + value of assets)





## Ideas

It will be written in Python.

It will handle multiple assets and able to compare multiple assets against each other.

Using a variety of indicators and trading strategies, each contained in their own modules.

It will be able to run simulations of past data. 

It will utilize multiple methods to evaluate strategy performance, including:
    Account balance (cash + value of assets)
    Position (long, short, flat)
    Profit/Loss per trade
    Maximum Drawdown
    Sharpe Ratio

It will have a cohesive API between modules.
    API will be tracked in an API.md file.

It will be designed to be easily extensible and modular.

It will have multiple modes of output with relevant trading signals and figures.
    Y/N prompts will offer generating a CSV file of the data, with a prompt to name the file after.
    Y/N prompts will offer generating a .png file of the figures after.
    Rudementary data will be outputted to the console after each run.

