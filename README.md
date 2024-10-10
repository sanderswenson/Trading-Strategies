Market Trading Bot with Built-In Simulator
Introduction
Have you ever wondered how traders decide when to buy or sell assets like Bitcoin or gold? The financial markets are complex and ever-changing, making it challenging to make informed decisions. This project aims to simplify this process by creating a market trading bot with an integrated simulation engine.
In simple terms, this software:
Analyzes historical market data for multiple assets.
Applies trading strategies to generate buy or sell signals.
Simulates trades based on these signals to see how strategies would have performed in the past.
Evaluates performance using key financial metrics.
Note: This project is in the early stages and is unpolished. Many features are incomplete or under development.
---
Project Overview
Features
Multiple Assets Support: Handles and compares multiple assets simultaneously, such as Bitcoin and gold.
Modular Design: Components like strategies and indicators are modular, allowing for easy extension and customization.
Trading Strategies: Implements various trading strategies, each in its own module.
Simulation Engine: Runs backtests on historical data to simulate trading performance.
Performance Evaluation: Assesses strategies using metrics like account balance and portfolio value over time.
Extensible API: Provides a cohesive API between modules for integration and scalability.
Current Focus
Portfolio Weight-Based Trading: Transitioning from raw buy/sell signals to strategies that trade based on target portfolio weights.
Rebalancing Logic: Implementing functions to rebalance the portfolio according to target weights while considering transaction costs.
Risk Management: Incorporating risk metrics and constraints into trading strategies.
Enhanced Performance Metrics: Developing tools to evaluate strategies more comprehensively.
---
Project Structure
The project is organized as follows:
main.py or main1.py: Entry point scripts to run the simulation.
data/
data_handler.py: Handles loading and preprocessing of financial data from CSV files.
strategies/
strategy_base.py: Base class and implementation of trading strategies like Moving Average Crossover.
balancer.py: Functions related to portfolio optimization (currently using SciPy for optimization).
simulation/
simulator.py or simulator1.py: Contains the simulation engine that executes trades based on signals or target weights.
utils/
performance_evaluator.py: Placeholder for future performance evaluation metrics.
indicators/
indicator_base.py: Base class for technical indicators (e.g., Simple Moving Average).
config.yaml: Configuration file for data sources, strategies, simulation parameters, and assets.
README.md: Project description and guidelines.
todo.md: Task list and future enhancements.