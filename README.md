 
### Project overview
The basis of our project is to create an algorithm that acts as a robo-financial-advisor. Our goal is to have an input user answer a series of questions and then use our algorithm to push out a portfolio of various ETFs. Our algorithm takes into account typical financial advising factors such as age, risk tolerance, and asset allocation preferences. From these preferences our algorithm will push out a portfolio of specific ETFs and list what each ETF allocation should consist of. 
The tool takes into consideration following factors:
    Age

    Risk level: (low, moderate, medium, aggressive) 

    Level of concern of a potential market crash

    What would you do if the market went up 10% in Month 1 and moved down 10% in Month 2? 
    (1 = Sold, 2 = Held Steady, 3 = Bought More, 4 = Bought more and hoped for further declines

    Willingness to invest in foreign markets, emerging economies, crypto, REIT’s
 
Based on the answers given to the above questions, the tool starts filtering out assets from our database leaving the most suitable choices for further consideration. The main goal for the advisor is to build a reasonable portfolio which balances risk vs. reward by taking into account the client's needs.

### Limitations and future development
Due to the time limitation, we were not able to include factors that play a big role in making an even better investment decision. Such factors are: Job position Salary fluctuation Student loans Willingness to make monthly/annual contributions Number of dependents

### Data pre-processing
A large part of our project was filtering out the correct data in order to fit it into a database with which we could create portfolios with. This was a multi-step process. We decided as a group that we only wanted to select ETFs that have developed an extensive track record over a longer period of time. Since ETFs are created every day, we chose to exclude those with which there wasn’t much price history. From this, we filtered out every ETF that didn’t have a minimum of five years of existence. In addition to this, we decided that since we are focusing on portfolio management, we are only suggesting products that are meant to be bought and held for a minimum time period of multiple years. This eliminated ETFs that were more short-term trade oriented such as leveraged ETFs, inverse ETFs, ultrashort ETFs. Once these steps were completed we had a general sense of the ETFs that would be included in the basket. 
The next step in our portfolio selection process was to divide the ETF’s into their special interest categories. The basis of our project is to have a consumer insert their list of investing desires, and we would then push back a portfolio that meets their needs. Among these potential needs are a desire to invest in foreign equities, real estate vehicles, cryptocurrencies, as well as stocks and bonds. From our previous broad-based basket, we separated our ETF’s into these special interests groups. From this, we created a basket of ETFs that included Equity ETFs, Bond ETFs, Foreign Equity ETFs, and Real Estate ETFs. 
A major part of portfolio optimization is taking the appropriate risk tolerance of the input consumer and giving back a specific portfolio that meets their desired risk tolerances. Based on our consumer surveys, we will be able to determine what level of risk our consumer desires. Due to this, we need to match the input user with a portfolio that matches their risk tolerance desires. For this, we needed to divide our equity ETFs and bond ETFs into various baskets based on how much risk exposure each ETF takes on. 
To find out the risk levels of each ETF, we took the betas of each ETF into consideration. ETFs that have lower betas would, in turn, contain less risk than ETFs that have high betas. From here, we separated our equity ETFs into five different baskets that ranged in risk levels. These baskets included “low beta”, “low-medium beta”, “medium beta”, “high-medium beta”, and “high beta.” The risk of each ETF increases as you go from low-to-high beta. Input users who are “risk-seeking” will have higher exposure to the “high-medium beta” and “high beta” baskets than input consumers who are less risk-seeking. 
For our bond ETF risk determinants, we broke the bond ETFs into three separate categories. These categories included “low-risk bonds”, “mid-risk bonds”, and “high-risk bonds.” We were able to determine the proper annotation based on the makeup of the bond ETF. Generally, bonds are graded on a scale that measures how risky the bond is. This scale contains highly safe and secure bonds, rated AAA, AA, and A, to less safe but moderately secure rated BBB bonds, to high-risk but high-reward bonds BB, B, and CCC grades. We determined that bond ETFs that were rated AAA, AA, or A would be considered “low-risk bonds”, while bond ETFs with a large exposure to BBB graded bonds would be considered “mid-risk bonds”, and bond ETFs with large exposures to BB, B, or CCC would be considered “high-risk bonds.” 
From the above data cleaning, we created baskets that will make up the entire exposure of an input user’s desired investment goals. This will give the input user a portfolio that meets their investing goals. 

 
### Usage and installation instructions of libraries/tools that are used
    Pandas 
    Csv 
    Numpy
    Path
    Matplotlib 
    Sqlalchemy
 
### Additional explanations
A major part of portfolio optimization is determining the allocation of different asset classes within a portfolio. The most basic form of this is determining the allocation of assets into equities and bonds. We have decided to implement this allocation into our portfolio, while also giving the input user a choice to add allocation exposure to foreign equity ETFs, real estate ETFs, and cryptocurrencies. The role of a portfolio advisor is  to calculate the proper allocation percentage to each asset class. Their are several factors that go into determining allocation percentages such as age, risk tolerance, and investing goals. For our model, we lean heavy into the age and risk tolerance input factors. 
The first major allocation to determine is the equity-to-bond allocation percentage. To determine this we took the age and risk tolerance of the input user. The following function allows for the calculation of equity-to-bond allocation:

![](../Capture.PNG)


The function where “r” is the risk tolerance level and x is the input user’s age will give the proper equity-to-bond exposure. Our model takes into account four separate risk categories. Based on this, an input user will have a equity-to-bond exposure somewhere along this function line:

![](../Capture2.PNG)

The x-axis in this chart is the input-users age and the y-axis is the input user’s exposure to bonds. As the user increases in age the less exposure they need to equities. The shades of blue in the diagram are dependent upon the risk tolerance of the input user. The more risk-seeking they are, the more exposure to equities they will have. 
 
 
 
### References used
    https://smartasset.com/investing/asset-allocation-calculator#dGIetOVSrl
    https://www.optimizedportfolio.com/asset-allocation/#asset-allocation-by-age-calculation
    https://www.kaggle.com/datasets/stefanoleone992/mutual-funds-and-etfs
    
### Team members:
    Minh
    Drew
    Alejandro 
    Bek

