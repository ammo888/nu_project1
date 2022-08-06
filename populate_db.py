import sqlalchemy as db
from sqlalchemy.dialects.postgresql import insert

def recreate_db():
    global engine
    global metadata
    
    # Establish connection to database
    db_url = "postgresql+psycopg2://postgres:postgres@localhost:5432/nu_project1"
    engine = db.create_engine(db_url)
    metadata = db.MetaData()

    # Recreate tables
    print("Recreating tables")
    with open("db_create_tables.sql") as f:
        query = db.text(f.read())
        engine.execute(query)

    # Read database metadata
    metadata.reflect(engine)
    
# RISK TOLERANCE
# Values (int): 1, 2, 3, 4
# Higher value indicates higher risk tolerance
def populate_risk_tolerance():
    print("Populating RiskTolerance")
    RiskTolerance = db.Table('RiskTolerance', metadata, autoload=True, autoload_with=engine)
    for risk_tolerance in range(1,5):
        ins = insert(RiskTolerance).values(RiskToleranceId=risk_tolerance).on_conflict_do_nothing()
        engine.execute(ins)
        
# FUND CATEGORY
# Values (string): BOND, EQUITY
def populate_fund_category():
    print("Populating FundCategory")
    FundCategory = db.Table('FundCategory', metadata, autoload=True, autoload_with=engine)
    for category_id, category in enumerate(["BOND", "EQUITY"]):
        engine.execute(insert(FundCategory).values(FundCategoryId=category_id, Category=category).on_conflict_do_nothing())
        
# BOND RISK CATEGORY
# Values (string): LOW_RISK, MID_RISK, HIGH_RISK
def populate_bond_risk_category():
    print("Populating BondRiskCategory")
    BondRiskCategory = db.Table('BondRiskCategory', metadata, autoload=True, autoload_with=engine)
    for category_id, category in enumerate(["LOW_RISK", "MID_RISK", "HIGH_RISK"]):
        engine.execute(insert(BondRiskCategory).values(BondRiskCategoryId=category_id, Category=category).on_conflict_do_nothing())

# BOND ALLOCATION
# Values (rows = risk tolerance, columns = bond risk category):
#     LOW_RISK  MID_RISK  HIGH_RISK
# 1     85%       10%        5%
# 2     75%       15%       10%
# 3     65%       20%       15%
# 4     55%       25%       20%
def populate_bond_allocation():
    print("Populating BondAllocation")
    BondAllocation = db.Table('BondAllocation', metadata, autoload=True, autoload_with=engine)
    allocations = [(1, 0, 0.85), (1, 1, 0.10), (1, 2, 0.05), 
                   (2, 0, 0.75), (2, 1, 0.15), (2, 2, 0.10),
                   (3, 0, 0.65), (3, 1, 0.20), (3, 2, 0.15),
                   (4, 0, 0.55), (4, 1, 0.25), (4, 2, 0.20)]
    for allocation_id, (risk_tolerance_id, bond_risk_category_id, allocation) in enumerate(allocations):
        engine.execute(insert(BondAllocation).values(BondAllocationId=allocation_id,
                                                     RiskToleranceId=risk_tolerance_id,
                                                     BondRiskCategoryId=bond_risk_category_id,
                                                     Allocation=allocation).on_conflict_do_nothing())
        
# EQUITY RISK CATEGORY
# Values (string): LOW, LOW_MEDIUM, MEDIUM, MEDIUM_HIGH, HIGH
def populate_equity_risk_category():
    print("Populating EquityRiskCategory")
    EquityRiskCategory = db.Table('EquityRiskCategory', metadata, autoload=True, autoload_with=engine)
    for category_id, category in enumerate(["LOW", "LOW_MEDIUM", "MEDIUM", "MEDIUM_HIGH", "HIGH"]):
        engine.execute(insert(EquityRiskCategory).values(EquityRiskCategoryId=category_id, Category=category).on_conflict_do_nothing())

# EQUITY ALLOCATION
# Values (rows = risk tolerance, columns = equity risk category):
#     LOW  LOW_MEDIUM  MEDIUM  MEDIUM_HIGH  HIGH
# 1   40%      30%       20%       5%         5%     
# 2   20%      40%       20%      10%        10%
# 3   10%      10%       20%      40%        20%
# 4    5%       5%       20%      30%        40%
def populate_equity_allocation():
    print("Populating EquityAllocation")
    EquityAllocation = db.Table('EquityAllocation', metadata, autoload=True, autoload_with=engine)
    allocations = [(1, 0, 0.40), (1, 1, 0.30), (1, 2, 0.20), (1, 3, 0.05), (1, 4, 0.05),
                   (2, 0, 0.20), (2, 1, 0.40), (2, 2, 0.20), (2, 3, 0.10), (2, 4, 0.10),
                   (3, 0, 0.10), (3, 1, 0.10), (3, 2, 0.20), (3, 3, 0.40), (3, 4, 0.20),
                   (4, 0, 0.05), (4, 1, 0.05), (4, 2, 0.20), (4, 3, 0.30), (4, 4, 0.40)]
    for allocation_id, (risk_tolerance_id, equity_risk_category_id, allocation) in enumerate(allocations):
        engine.execute(insert(EquityAllocation).values(EquityAllocationId=allocation_id,
                                                       RiskToleranceId=risk_tolerance_id,
                                                       EquityRiskCategoryId=equity_risk_category_id,
                                                       Allocation=allocation).on_conflict_do_nothing())

def populate_db():
    recreate_db()
    populate_risk_tolerance()
    populate_fund_category()
    populate_bond_risk_category()
    populate_bond_allocation()
    populate_equity_risk_category()
    populate_equity_allocation()
        
if __name__ == '__main__':
    populate_db()