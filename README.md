## Assignment 9 (Sessions 9 & 10)
The assignment consists of the following files:

## 1- Data : two datasets have been used 
 # chess_games_clean.csv (cleaned version of chess dataset)
 # who_life_expectancy.csv :(WHO_URL = 'https://github.com/Priyankkoul/Life-Expectancy-WHO---Data-Analytics/blob/master/DATASET.csv?raw=true'
)

## 2-The main script : session_10.py
Which uses the above datasets to answer the  questions (Q1-Q5) which will be detailed later

## 3-Requirements :  requirements.txt
numpy==2.2.6
pandas==2.3.3
python-dateutil==2.9.0.post0
pytz==2026.2
scipy==1.15.3
six==1.17.0
tzdata==2026.2

## 4-README file : README.md

## 5-.gitignore file

## Assignment Brief — Q1 through Q5

# Q1 Descriptive statistics profile of chess turns & rating_diff
From turns profile we can find that games typically last 37-79 turns (middle 50%) and Average game length is 60.5 turns, with most games are of moderate length. Some very short and very long games exist.
From the rating_diff  profile most games are reasonably balanced (differences under 241 points), Some extreme mismatches exist (up to 1,605 points) and the distribution is heavily right-skewed
Result :   
             turns              rating_diff
---------------------------------------------------------------
 dtype       float64               float64
count      20058.000000           20058.000000
mean        60.465999              173.091435
std         33.570585              179.214854
min          1.000000              0.000000
25%         37.000000              45.000000
50%         55.000000              115.000000
75%         79.000000              241.000000
max        349.000000               1605.000000
Mean          60.5                    173.1
Median        55.0                    115.0
IQR            42.0                   196.0
Skew           0.90                    1.95

# Q2  Distribution analysis — normality tests, log-transform
In order to test normality we used :Shapiro-Wilk — best for n < 5000
The null hypothesis is that the data is normally distributed. but the p-value is very small nearly: 0.000000, sowe reject the null hypothesis, our data is significantly non-normal.so Transformations are needed. We used two transformations:Square Root Transformation and Log Transformation.
Results:
                             turns                rating_diff
________________________________________________________________                             
Shapiro-Wilk             p = 0.000000              p = 0.000000
Original skew              0.90                      1.95
Square root skew            -0.062                   0.618
Log skew                    -1.37                    -0.90 

conclusion: For turns the Square root transformation is better than log , the rating difference is strongly right-skewed and also Square root transformation is better than log.

# Q3 WHO correlation matrix + one confounder discussion
Positive correlation: As one variable increases, the other tends to increase, while 
Negative correlation: As one variable increases, the other tends to decrease
TOP POSITIVE CORRELATES :Schooling,ncome Composition of Resources and BMI are all indicators of development
TOP NEGATIVE CORRELATES : Adult Mortality ,HIV/AIDS and Thinness are all indicators of deprivation
Results: 
Name: life_expectancy, dtype: float64
Top POSITIVE:
schooling                          0.752
income_composition_of_resources    0.725
bmi                                0.568

Top NEGATIVE:
adult_mortality                    -0.696
hiv/aids                           -0.557
thinness__1-19_years               -0.477

# Q4 Chi-squared test — rating group vs win rate, with effect size
Black rating has a slightly stronger effect (Cramer's V = 0.144) than White rating (0.119).
Win rates increase  with rating – for both colors, players in the lowest rating group win about 30-36% of games, while top-rated players win nearly 70%.

Results:
===========================================================
COMPARISON: White vs Black Rating Effect
============================================================

White Rating vs White Win:
  chi2 = 284.049, p = 0.000000, Cramer's V = 0.119
                     Win rates:
  white_group
(782.084, 1263.0]      36.2
(1263.0, 1742.0]       49.8
(1742.0, 2221.0]       54.4
(2221.0, 2700.0]       68.6
dtype: float64

Black Rating vs Black Win:
  chi2 = 415.034, p = 0.000000, Cramer's V = 0.144
                     Win rates:
  black_group
(787.066, 1272.5]       30.7
(1272.5, 1756.0]        45.0
(1756.0, 2239.5]        52.2
(2239.5, 2723.0]        69.9
dtype: float64

# Q5 95% CIs for rated vs unrated turns — parametric + bootstrap
Results:
95% CI for rated turns: (61.44, 62.48)
Bootstrap 95% CI for rated turns: (61.43, 62.50)
95% CI for unrated turns: (53.26, 55.28)
Bootstrap 95% CI for unrated turns: (53.20, 55.30)

# Conclusion:
rated games are significantly longer – the entire confidence interval for rated turns (61.4–62.5) is well above unrated turns (53.2–55.3), with no overlap.
Bootstrapped CIs confirm the findings – both traditional and bootstrap intervals are nearly identical, validating the statistical reliability.
