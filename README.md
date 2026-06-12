# Financial Performance Analysis Engine

## Overview

The Financial Performance Analysis Engine is a Python-based financial benchmarking and analytics system designed to evaluate company performance relative to industry peers.

The project dynamically retrieves financial statement data using the Yahoo Finance API (`yfinance`) and performs profitability, operational, and cash-flow analysis by calculating metrics such as:

- Revenue
- Net Income
- EBITDA
- Operating Cash Flow
- Free Cash Flow

The engine groups companies by GICS sector, compares user-entered company data against industry benchmarks, and generates rankings using binary-search positioning algorithms.

---

## Features

- Dynamic Yahoo Finance API integration
- Sector-based peer benchmarking
- Revenue ranking system
- Net income ranking system
- EBITDA ranking system
- Decision-tree classification engine
- Cash-flow and liquidity analysis
- Financial metric visualization using Matplotlib
- Pandas DataFrame architecture
- Binary-search ranking algorithms

---

## Technologies Used

- Python
- pandas
- yfinance
