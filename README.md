# Trading Automaton Project

## Overview
This project implements a simple trading automaton that analyzes historical price data, makes trading decisions, and tracks account balance. The system is designed to be modular and extensible.

## Components

### 1. Data Loader
The data loader is responsible for importing historical price data.

#### Features:
- Loads data from CSV files
- Handles date and price information
- Simple and efficient

### 2. Analysis Framework
This module provides a structure for implementing various analysis techniques.

#### Features:
- Supports multiple analysis strategies
- Easily extendable for new analysis methods
- Processes historical data to generate trading signals

### 3. Account Balance Tracker
Keeps track of the account's financial status.

#### Features:
- Monitors cash balance
- Tracks owned assets
- Calculates total portfolio value

### 4. Trading Module
Executes buy and sell orders based on analysis results and account status.

#### Features:
- Implements buying logic
- Implements selling logic
- Interacts with the Account Balance Tracker to update positions

## Usage

1. Prepare your historical data in CSV format with columns for date and price.
2. Implement your desired analysis strategy in the Analysis Framework.
3. Configure the Account Balance Tracker with initial balance.
4. Set up the Trading Module with your risk management parameters.
5. Run the main script to start the trading simulation.

## Future Improvements

- Implement more sophisticated analysis techniques
- Add support for multiple assets
- Integrate with real-time data feeds
- Implement backtesting capabilities
- Add performance metrics and visualization tools

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
