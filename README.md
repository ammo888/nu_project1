
### Project overview
We are currently working on creating an investment robo advisor that chooses the most optimal portfolio based on the answers asked during determining wants and needs of a potential investor 


The tool takes into consideration following factors:

    Age

    Risk level: (low, moderate, medium, aggressive) 
   
    Level of concern of a potential market crash
    
    What would you do if the market went up 10% in Month 1 and moved down 10% in Month 2? 
    (1 = Sold, 2 = Held Steady, 3 = Bought More, 4 = Bought more and hoped for further declines

    Willingness to invest in foreign markets, emerging economies, crypto, REIT’s
    
 Based on the answers given to the above questions, the tool starts filtering out assets from our database leaving the most suitable choices for further consideration. The main goal for the advisor is to build a reasonable portfolio which balances risk vs. reward by taking into account the client's needs.    

### Limitations and future development
Due to the time limitation, we were not able include factors that play a big role in making an even better investment decision. Such factors are:
    Job position
    Salary fluctuation
    Student loans 
    Willingness to make monthly/annual contributions
    Number of dependents



### Data pre-processing 
 Initially, we started cleaning the data in the pandas dataframe. We got rid of all the excess information, irrelevant columns and NaN’s. Next, we   started categorizing the data by creating tables that display daily returns of each ETF. We decided that we didn't need leverage and inverse ETF's. We also got rid of all the trading vehicles that were included in the data. We grouped different ETF's and bonds based on their betas We also used sharpe ratio to understand the return of an investment compared to its risk. 



### Usage and installation instructions of libraries/tools that are used
    Pandas 
    Csv 
    Numpy
    Path
    Matplotlib 
    Sqlalchemy


### Additional explanations
Initially, we wanted to focus on creating simple ETF portfolios. However, after a multiple team discussions, we decided to include crypto and bonds in order to make it a bit more 

### References used
    https://smartasset.com/investing/asset-allocation-calculator#dGIetOVSrl
    https://www.optimizedportfolio.com/asset-allocation/#asset-allocation-by-age-calculation
    https://www.kaggle.com/datasets/stefanoleone992/mutual-funds-and-etfs


### Team members:
    Minh
    Drew
    Alejandro 
    Bek


