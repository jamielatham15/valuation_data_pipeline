# Rule One Valuation Calculator
Approximates the intrinsic value of stocks. For use as an initial screener to identify (possibly) undervalued stocks. Uses a number of shorthand valuation techniques to estimate intrinsic value and margin of safety.

Adapted from the following authors:
- Phil Town and Danielle Town
- Aswath Damodaran

## Valuation Formula

### Greenwald, Graham and Dodd Investing
Greenwald's valuation method rejects speculative esitmates of future cashflows in favour of a "Graham and Dodd" approach updated for today's market conditions. It rests on two pillars: the reproduction value of a company's assets and its so-called "sustainable" earnings power. Greenwald looks at the ratio of assets to earnings power in order to identify companies with structural advantages in the market (Buffet's "moat"). Importantly, growth is not considered as a factor and significant adjustments are made to infer what a company's assets and earnings would be if they stopped reinvesting.

Assets are calculated as:

```
Current and non-current assets
+ Research and development costs
+ Administrative expenses
- Total liabilities
```

Earnings power value is calculated as:

```
(Normalized EBIT
- Average tax rate
- "Maintainance Capex")
\ Weighted average cost of capital (WACC)
```

`EPV - nebt debt = value of equity`


### Damodaran, Growth Rates
An implied forward 1 year growth rate derived from the reinvestment rate and return on equity. It makes sense to use an average net income value (e.g. past 5 years) to calculate ROE as this will be a big factor determining the growth.[^1]

```
Reinvestment Rate = Retained Earnings / Current Earnings 

Return on Investment = ROE = Net Income / Book Value of Equity

Implied forward growth = Reinvestment Rate * Return on Investment
```
To be conservative, this will be the growth rate in year 1 only. Years 2-5 will be 5%, and years 6-10 will be 2%.

### Town & Town, 10 Cap Value
Warren Buffet's "ewner earnings" multiplied by 10. The intuition here is that you should pay no more than 10 years of future earnings in order to get a minimum 10% capitalization rate. It takes no account of growth or the present value of future cashflows.[^2]

Owner earnings is calculated as:

```
Net Income
+ Depreciation & Amortization
+ Net Change: Accounts Receivable
+ Net Change: Accounts Payable
+ Income Tax
+ Maintenance Capital Expenditures
= Owner Earnings
```

### Town & Town, Payback Time

The total time to fully recuping the expense of an investment. Here it is the sum of free cash flows compounded by the company's growth rate for eight years. The period of eight years is to provide a margin of safety. According to Charlie Munger, a private company typically sells for half the price of a public one, and public companies sell for between 12 and 20 times their current free cash flow, or 16 on average. Half of 16 is 8, giving the "private" sale price of a company. Accounts for growth but not the present value of future cashflows. Also, growth is assumed to be static. For high growth companies this will produce valuation_metrics going to infinity. [^3]

Free cash flow can be calculated as:
```
Net Cash Provided by Operating Activities
+ Purchase of Property and Equipment (a negative number)
+ Any Other Capital Expenditures for Maintenance and Growth (also negative numbers)
= Free Cash Flow
```

### Town & Town, Margin of Safety
A shorthand approach to discounted cashflow analysis. Puts a price on a company's earnings over 10 years with a minimum acceptable rate of return (MARR) of 15% per annum.

Steps:
1. Find the future value of earnings compounded by the company's growth rate for 10 years. This is a forward 10 year EPS. 
2. Assumes that the market will value the company at 2 times is growth rate. This is the future P/E ratio. 
3. Multiply forward 10 year EPS by future P/E ratio to give future 10 year share price. 
4. Back calculate what the price should be today, assuming a 15% return per annum. 
5. Discount this to the present day, building in our MARR. Future 10 year share price / (1.15^10). 
6. Divide the result by 2 to build in a 50% margin of safety. 

This method does account for growth and for the present value of earnings.

## Data

Data must conform to the following format:

| Column                      | Description                                                                                                                             | Unit             | Period         | Input for        |
|-----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|------------------|----------------|------------------|
| TIDM                        | Tradable Instrument Display Mnemonic, aka Ticker                                                                                        |                  |                |                  |
| Name                        | Name of Share                                                                                                                           |                  |                |                  |
| Market Capitalization       | Latest close price multiplied by the number of shares                                                                                   | m                | Daily          |                  |
| Number of Shares            | Number of shares outstanding, not including employee options. Aggregate into a single number if there is more than one class of shares. | m                | Most recent    |                  |
| Close                       | Yesterday's close price                                                                                                                 | listing currency | Daily          |                  |
| Retained Profit             | Profit minus dividends payed in cash to shareholders                                                                                    | m                | TTM            | Growth rate      |
| Post-tax Profit             | Pre-tax profit from continuing operations                                                                                               | m                | TTM            | Growth rate      |
| Net profit                  | Profit from continuing operations after interest and depreciation, but before tax                                                       | m                | TTM            | Growth rate      |
| Net profit 5y av.           | 5 year average of profit from continuing operations after interest and depreciation, but before tax                                     | m                | 5 year average | Growth rate      |
| NAV                         | Net Asset Value (or Book Value). Total assets - total liabilities                                                                       | m                | TTM            | Growth rate      |
| Net profit                  | Profit from continuing operations after interest and depreciation, but before tax                                                       | m                | TTM            | 10 Cap Value     |
| Depreciation & Amortization | Write-down costs of both tangible and intangible assets                                                                                 | m                | TTM            | 10 Cap Value     |
| Change in debtors           | Change in money owed by the company                                                                                                     | m                | TTM            | 10 Cap Value     |
| Change in creditors         | Change in money owed to the company                                                                                                     | m                | TTM            | 10 Cap Value     |
| Tax paid                    | Net tax paid, including rebates and/or deferred losses (can result in negative figure)                                                  | m                | TTM            | 10 Cap Value     |
| Capex                       | Capital Expenditure: purchase of property, plant, and equipment. Can include software.                                                  | m                | TTM            | 10 Cap Value     |
| Free cash flow 5y av.       | 5 year average of cash available to pay as dividends, i.e. post-tax profit. Operating cash flow - tax paid - interest paid - capex      | m                | 5 year average | Payback Time     |
| EPS                         | Earnings per share                                                                                                                      | m                | TTM            | Margin of Safety |

# Data Pipeline

## AWS Setup

1. Create Amazon RDS instance (postgres), deploy schema using ./resources/sql/model.sql

2. Add s3 extension via psql
```bash
psql --host=<instance> --port=5432 --username=<username> --password=<password> --dbname=valuation_db

CREATE EXTENSION aws_s3 CASCADE;
```

3. Create the appropriate IAM roles for RDS<->S3 access: [Using an IAM role to access an Amazon S3 bucket](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PostgreSQL.S3Import.html#aws_s3.table_import_from_s3)

## Provision EC2 w/ terraform

```bash 
$env:AWS_ACCESS_KEY_ID & $env:AWS_SECRET_ACCESS_KEY before running

# Initialize the directory
terraform init

# Format the config file
terraform fmt

# Validate the config file
terraform validate

# Apply
terraform apply

# Inspect state
terraform show
```



[^1] Damodaran, Aswath. n.d. 'Session 10: Growth Rates - Historical, Analyst and Fundamental - YouTube'. Accessed 24 May 2022. https://www.youtube.com/.

[^2], [^3] Town, Danielle, and Phil Town. 2018. *Invested*, chapter 7.


