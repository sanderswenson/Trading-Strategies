#port opt
library(tidyquant) # To download the data
library(plotly) # To create interactive charts
library(timetk) # To manipulate the data series
library(tidyverse)

tick <- c('BTC-USD', 'GOLD')

price_data <- tq_get(tick, from='2016-9-11', to='2021-9-10', get = 'stock.prices')

log_ret_tidy <- price_data %>%
  group_by(symbol) %>%
  tq_transmute(select = adjusted,
               mutate_fun = periodReturn,
               period = 'daily',
               col_rename = 'ret',
               type = 'log')
head(log_ret_tidy)

log_ret_xts <- log_ret_tidy %>%
  spread(symbol, value = ret) %>%
  tk_xts()

log_ret_xts


mean_ret <- colMeans(log_ret_xts, na.rm=T)
print(round(mean_ret, 5))
