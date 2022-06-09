from common.config import MarketAssumptions

class Assets:
    def __init__(self, **kwargs) -> None:
        self.ticker = kwargs["ticker"]
        self.name = kwargs["name"]
        self.number_of_shares = kwargs["number_of_shares"]
        self.current_assets = kwargs["current_assets"]
        self.non_current_assets = kwargs["non_current_assets"]
        self.current_liabilities = kwargs["current_liabilities"]
        self.non_current_liabilities = kwargs["non_current_liabilities"]
        self.total_equity = kwargs["total_equity"]
        self.r_and_d = kwargs["r_and_d"]
        self.admin_expenses = kwargs["admin_expenses"]
        self.tangibles = kwargs["tangibles"]
        self.depreciation_and_amortization = kwargs["depreciation_and_amortization"]

    @property
    def adjusted_r_and_d(self, replication_adjustment=2) -> float:
        return self.r_and_d * replication_adjustment

    @property
    def adjusted_sga(self, replication_adjustment=2) -> float:
        return self.admin_expenses  * replication_adjustment

    @property
    def value_of_assets(self) -> float:
        return self.current_assets\
                + self.non_current_assets\
                - self.admin_expenses\
                + self.adjusted_sga\
                + self.adjusted_r_and_d

    @property
    def value_of_liabilities(self) -> float:
        return self.current_liabilities\
                + self.non_current_liabilities

    @property
    def asset_value_per_share(self):
        return (self.value_of_assets - self.value_of_liabilities) / self.number_of_shares


class EPV:
    def __init__(self, **kwargs) -> None:
        self.ticker = kwargs["ticker"]
        self.name = kwargs["name"]
        self.number_of_shares = kwargs["number_of_shares"]
        self.turnover = kwargs["turnover"]
        self.operating_margin_5y_av = kwargs["operating_margin_5y_av"]
        self.ebit_5y_av = kwargs["ebit_5y_av"]
        self.tax_rate_paid_5y_av = kwargs["tax_rate_paid_5y_av"]
        self.non_current_assets_5_y_av = kwargs["non_current_assets_5_y_av"]
        self.turnover_5y_av = kwargs["turnover_5y_av"]
        self.turnover_perc_chg = kwargs["turnover_perc_chg"]
        self.borrowing = kwargs["borrowing"]
        self.leases = kwargs["leases"]
        self.debt = kwargs["debt"]
        self.total_equity = kwargs["total_equity"]
        self.beta = kwargs["beta"]
        self.capex_5y_av = kwargs["capex_5y_av"]
        self.r_and_d_5y_av = kwargs["r_and_d_5y_av"]
        self.admin_expenses_5y_av = kwargs["admin_expenses_5y_av"]
        self.depreciation_and_amortization = kwargs["depreciation_and_amortization"]

    # EARNINGS
    @property
    def operating_margin(self, growth_adjustment=0.2):
        operating_expenses = (self.r_and_d_5y_av + self.admin_expenses_5y_av) / self.turnover_5y_av
        return (self.operating_margin_5y_av / 100) + (operating_expenses * growth_adjustment)

    @property
    def normalized_ebit(self):
        return self.turnover * self.operating_margin
    
    @property
    def average_tax_rate(self):
        if (avg_tax:=self.tax_rate_paid_5y_av / 100) > 0:
            return avg_tax
        else:
            return MarketAssumptions.average_tax_rate

    # CAPEX
    @property
    def maintainance_capex(self):
        return (self.capex_5y_av / self.turnover_5y_av) * self.normalized_ebit

    # WACC
    @property
    def total_debt(self):
        return self.borrowing + self.leases + self.debt
    
    @property
    def cost_of_debt(self):
        return MarketAssumptions.cost_of_debt - (MarketAssumptions.cost_of_debt * self.average_tax_rate)

    @property
    def cost_of_equity(self):
        base_case = MarketAssumptions.risk_free_rate + 1 * MarketAssumptions.equity_risk_premium
        if (coe:=MarketAssumptions.risk_free_rate + self.beta * MarketAssumptions.equity_risk_premium) > base_case:
            return coe
        else:
            return base_case


    @property
    def total_capital(self):
        return  self.total_debt + self.total_equity

    def adjusted_capital_ratios(self):
        if (d:=self.total_debt / self.total_capital) < 0.3:
            return d, (self.total_equity / self.total_capital)
        else:
            return 0.3, 0.7

    @property
    def wacc(self):
        debt_to_capital, equity_to_capital = self.adjusted_capital_ratios()
        return (debt_to_capital * self.cost_of_debt) + (equity_to_capital * self.cost_of_equity)
    
    @property
    def nopat(self):
        return self.normalized_ebit - (self.normalized_ebit * self.average_tax_rate) 
    
    # EPV
    @property
    def earnings_power(self):
        return self.nopat + (self.depreciation_and_amortization * self.average_tax_rate) - self.maintainance_capex
    
    @property
    def earnings_power_value(self):
        return self.earnings_power / self.wacc

def business_category(assets, epv):
    if (epv_to_assets:=(epv - assets) / epv) >= 0.25:
        return "advantage"
    elif epv_to_assets <= -0.2:
        return "decline"
    else:
        return "balance"

def valuation(data: dict):

    assets = Assets(**data)

    epv = EPV(**data)

    equity_value = epv.earnings_power_value - (epv.total_debt - data["cash"])

    value_per_share = equity_value / data["number_of_shares"]

    margin_of_safety = 1 - data["close"] / value_per_share

    return {
        "company": data["name"],
        "asset_value": round(assets.value_of_assets, 2),
        "earnings_power_value": round(epv.earnings_power_value, 2),
        "wacc": round(epv.wacc * 100, 2) ,
        "value_per_share": round(value_per_share, 2),
        "margin_of_safety": round(margin_of_safety * 100, 2),
        "business_category": business_category(assets.value_of_assets, epv.earnings_power_value)
    }
