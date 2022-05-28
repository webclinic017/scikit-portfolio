#!/usr/bin/env python

"""Tests for `skportfolio` package."""
import pytest
import numpy as np
import pandas as pd  # type: ignore
from skportfolio.backtest.backtester import Strategy
from skportfolio import EquallyWeighted, InverseVariance, InverseVolatility
from sklearn.base import clone  # type: ignore
from skportfolio.datasets import load_dataset


from skportfolio import PortfolioEstimator

from .datasets_fixtures import prices, returns, log_returns
from skportfolio.backtest.backtester import Backtester


def test_strategy(prices):
    strategy = Strategy(
        initial_weights=EquallyWeighted().fit(prices).weights_,
        initial_portfolio_value=10000,
        estimator=EquallyWeighted(),
        rebalance_frequency="M",
        lookback_periods=(40, 126),
        transaction_costs=(0.05, 0.05),  # buy and sell costs
    )
    return strategy


def test_backtester():
    # For readability, use only 15 of the 30 DJI component stocks.
    asset_symbols = [
        "AA",
        "CAT",
        "DIS",
        "GM",
        "HPQ",
        "JNJ",
        "MCD",
        "MMM",
        "MO",
        "MRK",
        "MSFT",
        "PFE",
        "PG",
        "T",
        "XOM",
    ]

    prices = load_dataset("dowportfolio").loc[:, asset_symbols]
    prices.index = pd.to_datetime(prices.index)
    # prices.index.freq = pd.offsets.Day()
    # prices.index.freqstr = "D"
    # prices = prices.resample("B").mean()

    strategy = test_strategy(prices)
    backtester = Backtester(strategy=strategy, warmup_period=40).fit(prices)

    return