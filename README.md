
We are currently working on creating an investment robo advisor that chooses the most optimal portfolio based on the answers asked during determining 
wants and needs of a potential investor.

The tool takes into consideration following factors:

    Age
    Risk level: (low, moderate, medium, aggressive) 
   
    Level of concern of a potential market crash
    
    What would you do if the market went up 10% in Month 1 and moved down 10% in Month 2? 
    (1 = Sold, 2 = Held Steady, 3 = Bought More, 4 = Bought more and hoped for further declines

    Willingness to invest in foreign markets, ESG’s, emerging economies,  Crypto, REIT’s
    


Based on the answers given to the above questions, the tool starts filtering out assets from our database leaving the most suitable choices for further 
consideration. The main goal for the advisor is to build a reasonable portfolio which balances risk vs. reward by taking into account the client's needs. 

Initially, we started cleaning the data in the pandas dataframe. We got rid of all the excess information, irrelevant columns and NaN’s. Next, we started 
categorizing the data by creating tables that display daily returns of each ETF. Then we used sharpe ratio understand the return of an investment compared 
to its risk.

References used:
    https://smartasset.com/investing/asset-allocation-calculator#dGIetOVSrl
    https://www.optimizedportfolio.com/asset-allocation/#asset-allocation-by-age-calculation
    https://www.kaggle.com/datasets/stefanoleone992/mutual-funds-and-etfs

Team members:
Minh
Drew
Alejandro 
Bek


