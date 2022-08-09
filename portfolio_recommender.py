import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import questionary as q
import sqlalchemy as db

# Calculates crypto allocation for ages 18-25
def low_age_crypto_allocation(age):
    return ((1/20)*((age-18)/10)**2)+0.025

# Calculates crypto allocation - piecewise function with ranges 18-25, 25-35, 35-100
# 18-25: low_age_crypto_allocation
# 25-35: low_age_crypto_alocation @ 25 - flat line
# 35-100: linearly decreases from 35 until 65
def age_crypto_allocation(age):
        if age in range(18, 25):
            return low_age_crypto_allocation(age)
        elif age in range(25, 35):
            return low_age_crypto_allocation(25)
        else:
            crypto_allocation_max = low_age_crypto_allocation(25)
            return max(crypto_allocation_max - (crypto_allocation_max / (65 - 35)) * (age - 35), 0)

# Calculates crypto allocation taking into account risk tolerance (1 through 4)
# Fractional calculation where 4 is the highest risk, and 1,2,3 are 1/2, 1/3, 1/4 the allocation, respectively
def age_risk_crypto_allocation(age,risk):
    return age_crypto_allocation(age) * (risk/4)

# Bond allocation
# Linearly increases from 18 to 100 - the starting point is determined by risk tolerance
def bond_allocation(age, risk_tolerance):
    return min(1.0, (10.0 * (4 - risk_tolerance) + (age - 18)) / 100)

# User questionnaire
def user_input():
    age = q.select(
        "Please enter your age (18-100):",
        choices=[q.Choice(title=str(x), value=x) for x in range(18, 100 + 1)],
    ).ask()

    risk_tolerance = q.select("What would you do if the market went up 10% in Month 1 and moved down 10% in Month 2?",
                              choices=[q.Choice(title="Sold", value=1),
                                       q.Choice(title="Held Steady", value=2),
                                       q.Choice(title="Bought More", value=3),
                                       q.Choice(title="Bought more and hoped for further declines", value=4)]).ask()

    include_international = q.select("Sometimes, having international companies provides diversification benefits to your portfolio but it also entails an economic risk, would you be willing to have international exposure?",
                                     choices=[q.Choice(title='Yes', value=True), q.Choice(title='No', value=False)]).ask()
    know_reits = q.select("Do you know What REITS are?", choices=[q.Choice(title='Yes', value=True), q.Choice(title='No', value=False)]).ask()
    if know_reits:
        include_reits = q.select("Would you like to add them to your portfolio?",
                                 choices=[q.Choice(title='Yes', value=True), q.Choice(title='No', value=False)]).ask()
    else:
        include_reits = q.select("A REIT is a company that owns and typically operates income-producing real estate or related assets. These may include office buildings, shopping malls, apartments, hotels, resorts, self-storage facilities, warehouses, and mortgages or loans. Would you like to add them to your Portfolio?",
                                 choices=[q.Choice(title='Yes', value=True), q.Choice(title='No', value=False)]).ask()

    crypto = q.select("Would you like to add Cryptocurrencies in your portfolio?",
                      choices=[q.Choice(title='Yes', value=True), q.Choice(title='No', value=False)]).ask()

    crypto_allocation = age_risk_crypto_allocation(age, risk_tolerance) if crypto else 0
    bond_etf_allocation = bond_allocation(age, risk_tolerance)
    stock_etf_allocation = 1 - bond_etf_allocation - crypto_allocation

    print(f"Your Final allocation is: Stocks:{stock_etf_allocation*100:.2f}% Bonds: {bond_etf_allocation*100:.2f}% Crypto:{crypto_allocation*100:.2f}%")

    return risk_tolerance, bond_etf_allocation, stock_etf_allocation, crypto_allocation, include_international, include_reits

def user_input_db_url():
    return q.text(
        "Please enter the database url:",
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/nu_project1",
    ).ask()

# Encapsulation of PostgresSQL database access
class PortfolioDb:
    OutputColumns = ["fund_symbol", "allocation"]

    BondBasketSize = 10
    ReitBasketSize = 7
    InternationalBasketSize = 15
    EquityBasketSize = 10

    ReitAllocation = 0.10
    InternationalAllocation = 0.10

    CryptoEtf = "BITCOIN"

    def __init__(self, risk_tolerance, bond_etf_allocation, stock_etf_allocation, crypto_allocation, include_international, include_reits, db_url):
        self.risk_tolerance = risk_tolerance
        self.bond_etf_allocation = bond_etf_allocation
        self.stock_etf_allocation = stock_etf_allocation
        self.crypto_allocation = crypto_allocation
        self.include_international = include_international
        self.include_reits = include_reits
        self.db_url = db_url

        self.international_allocation = PortfolioDb.InternationalAllocation if include_international else 0
        self.reit_allocation = PortfolioDb.ReitAllocation if include_reits else 0
        self.rest_equity_allocation = 1.0 - self.international_allocation - self.reit_allocation

    def initialize(self):
        self.engine = db.create_engine(self.db_url)
        self.metadata = db.MetaData()
        self.metadata.reflect(self.engine)

        self.RiskTolerance = db.Table('RiskTolerance', self.metadata, autoload=True, autoload_with=self.engine)
        self.FundCategory = db.Table('FundCategory', self.metadata, autoload=True, autoload_with=self.engine)

        self.BondRiskCategory = db.Table('BondRiskCategory', self.metadata, autoload=True, autoload_with=self.engine)
        self.BondAllocation = db.Table('BondAllocation', self.metadata, autoload=True, autoload_with=self.engine)

        self.EquityRiskCategory = db.Table('EquityRiskCategory', self.metadata, autoload=True, autoload_with=self.engine)
        self.EquityAllocation = db.Table('EquityAllocation', self.metadata, autoload=True, autoload_with=self.engine)

        self.ETF = db.Table('ETF', self.metadata, autoload=True, autoload_with=self.engine)

        fund_categories = self.engine.execute(db.select(self.FundCategory)).fetchall()
        self.FundCategoryIdMapping = {category : fund_category_id for (fund_category_id, category) in fund_categories}

    # A simple crypto allocation formula - BITCOIN is the only cryptocurrency available
    def crypto_etfs(self):
        crypto = pd.DataFrame(columns=PortfolioDb.OutputColumns)

        if crypto_allocation > 0:
            crypto = crypto.append({"fund_symbol": PortfolioDb.CryptoEtf, "allocation": crypto_allocation}, ignore_index=True)

        return crypto

    # Bond ETFs Allocation
    # Risk tolerance determines allocation for different bond baskets
    # From each basket only the top select number of ETFs are chosen
    def bond_etfs(self):
        bonds = pd.DataFrame(columns=PortfolioDb.OutputColumns)

        bond_risk_allocation_stmt = db.select(self.BondAllocation).where(self.BondAllocation.c.RiskToleranceId==self.risk_tolerance)
        bond_risk_allocation = self.engine.execute(bond_risk_allocation_stmt).fetchall()

        for _, _, bond_risk_category_id, bond_risk_category_allocation in bond_risk_allocation:
            bond_risk_category_basket_stmt = db.select(self.ETF).where((self.ETF.c.FundCategoryId==self.FundCategoryIdMapping["BOND"])
                & (self.ETF.c.BondRiskCategoryId==bond_risk_category_id)).order_by(self.ETF.c.Sharpe.desc()).limit(PortfolioDb.BondBasketSize)

            for etf in self.engine.execute(bond_risk_category_basket_stmt).fetchall():
                allocation = self.bond_etf_allocation * bond_risk_category_allocation * (1.0 / PortfolioDb.BondBasketSize)
                bonds = bonds.append({"fund_symbol": etf[0], "allocation": allocation}, ignore_index=True)

        return bonds

    # REITs Allocation
    # If chosen, from each basket only the top select number of ETFs are chosen
    def reit_etfs(self):
        reits = pd.DataFrame(columns=PortfolioDb.OutputColumns)

        if self.include_reits:
            reits_basket_stmt =  db.select(self.ETF).where((self.ETF.c.FundCategoryId==self.FundCategoryIdMapping["EQUITY"])
                & (self.ETF.c.IsReit==True)).order_by(self.ETF.c.Sharpe.desc()).limit(PortfolioDb.ReitBasketSize)
            for etf in self.engine.execute(reits_basket_stmt).fetchall():
                allocation = self.stock_etf_allocation * self.reit_allocation * (1.0 / PortfolioDb.ReitBasketSize)
                reits = reits.append({"fund_symbol": etf[0], "allocation": allocation}, ignore_index=True)

        return reits

    # International Allocation
    # If chosen, from each basket only the top select number of ETFs are chosen
    def international_etfs(self):
        internationals = pd.DataFrame(columns=PortfolioDb.OutputColumns)

        if self.include_international:
            international_basket_stmt =  db.select(self.ETF).where((self.ETF.c.FundCategoryId==self.FundCategoryIdMapping["EQUITY"])
                & (self.ETF.c.IsInternational==True)).order_by(self.ETF.c.Sharpe.desc()).limit(PortfolioDb.InternationalBasketSize)
            for etf in self.engine.execute(international_basket_stmt).fetchall():
                allocation = self.stock_etf_allocation * self.international_allocation * (1.0 / PortfolioDb.InternationalBasketSize)
                internationals = internationals.append({"fund_symbol": etf[0], "allocation": allocation}, ignore_index=True)

        return internationals

    # International Allocation
    # Risk tolerance determines allocation for different equity baskets
    # From each basket only the top select number of ETFs are chosen
    def equities_etfs(self):
        equities = pd.DataFrame(columns=PortfolioDb.OutputColumns)

        equity_risk_allocation_stmt = db.select(self.EquityAllocation).where(self.EquityAllocation.c.RiskToleranceId==self.risk_tolerance)
        equity_risk_allocation = self.engine.execute(equity_risk_allocation_stmt).fetchall()

        for _, _, equity_risk_category_id, equity_risk_category_allocation in equity_risk_allocation:
            equity_risk_category_basket_stmt = db.select(self.ETF).where((self.ETF.c.FundCategoryId==self.FundCategoryIdMapping["EQUITY"])
                & (self.ETF.c.IsReit==False)
                & (self.ETF.c.IsInternational==False)
                & (self.ETF.c.EquityRiskCategoryId==equity_risk_category_id)).order_by(self.ETF.c.Sharpe.desc()).limit(PortfolioDb.EquityBasketSize)

            for etf in self.engine.execute(equity_risk_category_basket_stmt).fetchall():
                allocation = self.stock_etf_allocation * self.rest_equity_allocation * equity_risk_category_allocation * (1.0 / PortfolioDb.EquityBasketSize)
                equities = equities.append({"fund_symbol": etf[0], "allocation": allocation}, ignore_index=True)

        return equities

    def recommended_portfolio(self):

        return pd.concat([self.crypto_etfs(),
                          self.bond_etfs(),
                          self.reit_etfs(),
                          self.international_etfs(),
                          self.equities_etfs()])

def print_recommended_portfolio(recommended_portfolio):
    print("Your recommended portfolio:")
    print(f"Fund Symbol | Allocation ")

    for row in recommended_portfolio.itertuples():
        print(f"{row.fund_symbol: <14}{row.allocation}")

def user_input_show_risks():
    return q.select("Show recommend portfolio risk parameters? (Slow operation)",
                      choices=[q.Choice(title='Yes', value=True), q.Choice(title='No', value=False)]).ask()

def print_risk_parameters(recommended_portfolio):
    etf_prices_full = pd.read_csv("data/ETF prices.csv", parse_dates=True, infer_datetime_format=True)
    etf_prices_full = etf_prices_full[["fund_symbol", "price_date", "adj_close"]]
    etf_prices_full = etf_prices_full[etf_prices_full.price_date >= "2016"]

    # Could not figure out how the mean TNX return is positive despite TNX decreasing in value from 2016 to end of 2021

    etf_prices_full = etf_prices_full.pivot_table(index = ["price_date"], columns = "fund_symbol", values = "adj_close")

    etf_prices_custom = etf_prices_full.loc[:, etf_prices_full.columns.isin(recommended_portfolio.fund_symbol)].copy()
    etf_prices_custom.dropna(axis='columns', inplace=True)
    etf_prices_custom["net"] = etf_prices_custom.dot(recommended_portfolio[recommended_portfolio.fund_symbol != PortfolioDb.CryptoEtf].set_index("fund_symbol").allocation)
    etf_returns = etf_prices_custom.pct_change().dropna()

    custom_returns = etf_returns.net
    spy_returns = etf_prices_full.SPY.pct_change().dropna()

    sharpe = etf_returns.net.mean() / etf_returns.net.std() * np.sqrt(252)

    s = pd.concat([spy_returns, custom_returns], axis=1, join='inner')
    s.columns = ["spy", "custom"]
    beta = s.cov()["spy"]["custom"] / s.cov()["spy"]["spy"]

    print("Risk Parameters:")
    print(f"Sharpe={sharpe}")
    print(f"Beta={beta}")

def user_input_show_visual():
    return q.select("Show overall portfolio allocation in pie chart?",
                      choices=[q.Choice(title='Yes', value=True), q.Choice(title='No', value=False)]).ask()

def visual(bond, stock, crypto):
    portfolio_allocation_df_w_crypto = pd.DataFrame({'Percentage': [stock, bond, crypto]}, index = ['Stocks', 'Bonds', 'Crypto'])
    portfolio_allocation_df_w_crypto.plot.pie(subplots = True, figsize = (5, 5), autopct='%1.0f%%')
    plt.show()

if __name__ == '__main__':
    risk_tolerance, bond_etf_allocation, stock_etf_allocation, crypto_allocation, include_international, include_reits = user_input()

    db_path = user_input_db_url()
    portfolio_db = PortfolioDb(risk_tolerance, bond_etf_allocation, stock_etf_allocation, crypto_allocation, include_international, include_reits, db_path)
    portfolio_db.initialize()

    recommended_portfolio = portfolio_db.recommended_portfolio()
    print_recommended_portfolio(recommended_portfolio)

    if user_input_show_risks():
        print_risk_parameters(recommended_portfolio)

    if user_input_show_visual():
        visual(bond_etf_allocation, stock_etf_allocation, crypto_allocation)


