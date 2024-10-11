MATH 460: MCM 2022 Problem C
--
* main.py or main1.py: primary scripts. main.py runs the SMA strategy for one asset at a time. main1.py runs the dynamically-weighted strategy.
* data/
  + data_handler.py: Handles loading and preprocessing of financial data from CSV files.
  + 
* strategies/
  + strategy_base.py: Base class and implementation of trading strategies like Moving Average Crossover.
  + balancer.py: Weight optimization function strategies using SciPy.
* simulation/
  + simulator.py: unweighted simulation engine that executes trades for one asset at a time based solely on signals.
  + simulator1.py: simulation engine implemented for weighted assets.
