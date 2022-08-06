-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

DROP TABLE IF EXISTS "FundCategory" CASCADE;
DROP TABLE IF EXISTS "EquityRiskCategory" CASCADE;
DROP TABLE IF EXISTS "BondRiskCategory" CASCADE;
DROP TABLE IF EXISTS "RiskTolerance" CASCADE;
DROP TABLE IF EXISTS "ETF" CASCADE;
DROP TABLE IF EXISTS "EquityAllocation" CASCADE;
DROP TABLE IF EXISTS "BondAllocation" CASCADE;


CREATE TABLE "FundCategory" (
    "FundCategoryId" int   NOT NULL,
    "Category" varchar(20)   NOT NULL,
    CONSTRAINT "pk_FundCategory" PRIMARY KEY (
        "FundCategoryId"
     ),
    CONSTRAINT "uc_FundCategory_Category" UNIQUE (
        "Category"
    )
);

CREATE TABLE "EquityRiskCategory" (
    "EquityRiskCategoryId" int   NOT NULL,
    "Category" varchar(20)   NOT NULL,
    CONSTRAINT "pk_EquityRiskCategory" PRIMARY KEY (
        "EquityRiskCategoryId"
     ),
    CONSTRAINT "uc_EquityRiskCategory_Category" UNIQUE (
        "Category"
    )
);

CREATE TABLE "BondRiskCategory" (
    "BondRiskCategoryId" int   NOT NULL,
    "Category" varchar(20)   NOT NULL,
    CONSTRAINT "pk_BondRiskCategory" PRIMARY KEY (
        "BondRiskCategoryId"
     ),
    CONSTRAINT "uc_BondRiskCategory_Category" UNIQUE (
        "Category"
    )
);

CREATE TABLE "RiskTolerance" (
    "RiskToleranceId" int   NOT NULL,
    CONSTRAINT "pk_RiskTolerance" PRIMARY KEY (
        "RiskToleranceId"
     )
);

CREATE TABLE "ETF" (
    "Symbol" varchar(20)   NOT NULL,
    "FundCategoryId" int   NOT NULL,
    "Sharpe" float   NOT NULL,
    "Beta" float   NOT NULL,
    "IsReit" boolean   NOT NULL,
    "IsEsg" boolean   NOT NULL,
    "IsInternational" boolean   NOT NULL,
    "EquityRiskCategoryId" int   NOT NULL,
    "BondRiskCategoryId" int   NOT NULL,
    CONSTRAINT "pk_ETF" PRIMARY KEY (
        "Symbol"
     )
);

CREATE TABLE "EquityAllocation" (
    "EquityAllocationId" int   NOT NULL,
    "RiskToleranceId" int   NOT NULL,
    "EquityRiskCategoryId" int   NOT NULL,
    "Allocation" float   NOT NULL,
    CONSTRAINT "pk_EquityAllocation" PRIMARY KEY (
        "EquityAllocationId"
     )
);

CREATE TABLE "BondAllocation" (
    "BondAllocationId" int   NOT NULL,
    "RiskToleranceId" int   NOT NULL,
    "BondRiskCategoryId" int   NOT NULL,
    "Allocation" float   NOT NULL,
    CONSTRAINT "pk_BondAllocation" PRIMARY KEY (
        "BondAllocationId"
     )
);

ALTER TABLE "ETF" ADD CONSTRAINT "fk_ETF_FundCategoryId" FOREIGN KEY("FundCategoryId")
REFERENCES "FundCategory" ("FundCategoryId");

ALTER TABLE "ETF" ADD CONSTRAINT "fk_ETF_EquityRiskCategoryId" FOREIGN KEY("EquityRiskCategoryId")
REFERENCES "EquityRiskCategory" ("EquityRiskCategoryId");

ALTER TABLE "ETF" ADD CONSTRAINT "fk_ETF_BondRiskCategoryId" FOREIGN KEY("BondRiskCategoryId")
REFERENCES "BondRiskCategory" ("BondRiskCategoryId");

ALTER TABLE "EquityAllocation" ADD CONSTRAINT "fk_EquityAllocation_RiskToleranceId" FOREIGN KEY("RiskToleranceId")
REFERENCES "RiskTolerance" ("RiskToleranceId");

ALTER TABLE "EquityAllocation" ADD CONSTRAINT "fk_EquityAllocation_EquityRiskCategoryId" FOREIGN KEY("EquityRiskCategoryId")
REFERENCES "EquityRiskCategory" ("EquityRiskCategoryId");

ALTER TABLE "BondAllocation" ADD CONSTRAINT "fk_BondAllocation_RiskToleranceId" FOREIGN KEY("RiskToleranceId")
REFERENCES "RiskTolerance" ("RiskToleranceId");

ALTER TABLE "BondAllocation" ADD CONSTRAINT "fk_BondAllocation_BondRiskCategoryId" FOREIGN KEY("BondRiskCategoryId")
REFERENCES "BondRiskCategory" ("BondRiskCategoryId");

