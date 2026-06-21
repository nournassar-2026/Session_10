import pandas as pd
import numpy as np 
from scipy import stats
#chess dataset
df=pd.read_csv('data/chess_games.csv')
# Q1 Descriptive statistics profile of chess turns & rating_diff
# Full profile of turns
print(df['turns'].describe())
print(f"Mean: {df['turns'].mean():.1f}") 
print(f"Median: {df['turns'].median():.1f}") 
# IQR
q1 = df['turns'].quantile(0.25) # 36.0
q3 = df['turns'].quantile(0.75) # 77.0
print(f"IQR: {q3 - q1:.1f}") # 41.0
# Skewness
print(f"Skew: {df['turns'].skew():.2f}")
# Full profile of rating_diff
df['rating_diff'] = abs(df['white_rating'] - df['black_rating'])
print(df['rating_diff'].describe())
# Mean vs median
print(f"Mean: {df['rating_diff'].mean():.1f}") 
print(f"Median: {df['rating_diff'].median():.1f}") 
# IQR
q1 = df['rating_diff'].quantile(0.25) 
q3 = df['rating_diff'].quantile(0.75) 
print(f"IQR: {q3 - q1:.1f}") # 41.0
# Skewness
print(f"Skew: {df['rating_diff'].skew():.2f}") 
#################################################
#Q2 Distribution analysis — normality tests, log-transform
# 2. Test normality (Shapiro-Wilk — best for n < 5000) [turns]
stat, p = stats.shapiro(df['turns'].sample(1000, random_state=42))
print(f"Shapiro-Wilk p = {p:.6f}") # p ≈ 0.000000 → NOT normal
# 3. Log transform _ sqrt 
df['sqrt_turns'] = np.sqrt(df['turns'])
df['turns_log'] = np.log1p(df['turns'])
print(f"Original skew: {df['turns'].skew():.2f}") 
print(f"Square root skew: {df['sqrt_turns'].skew():.3f}")
print(f"Log skew: {df['turns_log'].skew():.2f}") 
#rating_diff
df['rating_diff'] = abs(df['white_rating'] - df['black_rating'])
# 2. Test normality (Shapiro-Wilk — best for n < 5000) 
stat, p = stats.shapiro(df['rating_diff'].sample(1000, random_state=42))
print(f"Shapiro-Wilk p = {p:.6f}") # p ≈ 0.000000 → NOT normal
# 3. Log transform -sqrt
df['sqrt_rating_diff'] = np.sqrt(df['rating_diff'])
df['rating_diff_log'] = np.log1p(df['rating_diff'])
print(f"Original skew: {df['rating_diff'].skew():.2f}") 
print(f"Square root skew: {df['sqrt_rating_diff'].skew():.3f}")
print(f"Log skew: {df['rating_diff_log'].skew():.2f}") 

# Q3 WHO correlation matrix + one confounder discussion
# For reading who dataset from url do not comment the following lines
#WHO_URL = 'https://github.com/Priyankkoul/Life-Expectancy-WHO---Data-Analytics/blob/master/DATASET.csv?raw=true'
#who = pd.read_csv(WHO_URL)
# Clean column names
#who.columns = who.columns.str.strip().str.lower().str.replace(' ', '_')
# Save locally (optional)
#who.to_csv('who_life_expectancy.csv', index=False)
#print("Dataset saved as 'who_life_expectancy.csv'")
who = pd.read_csv('data/who_life_expectancy.csv') #reading data from file
# Correlations with life expectancy
corrs = who.select_dtypes('number').corr()['life_expectancy'].drop('life_expectancy')
top_pos = corrs.nlargest(3)
top_neg = corrs.nsmallest(3)
print('Top POSITIVE:')
print(top_pos.round(3))
# schooling 0.753
# income_composition_of_resources 0.723
# bmi 0.567
print('Top NEGATIVE:')
print(top_neg.round(3))

#Q4 Chi-squared test — rating group vs win rate, with effect size
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

# Create rating groups for both players
df['white_group'] = pd.cut(df['white_rating'], bins=4)
df['black_group'] = pd.cut(df['black_rating'], bins=4)

# Create win indicators
df['white_win'] = (df['winner'] == 'White').astype(int)
df['black_win'] = (df['winner'] == 'Black').astype(int)

# Run both tests
ct_w = pd.crosstab(df['white_group'], df['white_win'])
ct_b = pd.crosstab(df['black_group'], df['black_win'])

chi2_w, p_w, _, _ = chi2_contingency(ct_w)
chi2_b, p_b, _, _ = chi2_contingency(ct_b)

cramers_v_w = np.sqrt(chi2_w / (ct_w.sum().sum() * (min(ct_w.shape) - 1)))
cramers_v_b = np.sqrt(chi2_b / (ct_b.sum().sum() * (min(ct_b.shape) - 1)))

print("=" * 60)
print("COMPARISON: White vs Black Rating Effect")
print("=" * 60)
print(f"\nWhite Rating vs White Win:")
print(f"  chi2 = {chi2_w:.3f}, p = {p_w:.6f}, Cramer's V = {cramers_v_w:.3f}")
print(f"  Win rates:\n  {(ct_w[1] / ct_w.sum(axis=1) * 100).round(1)}")

print(f"\nBlack Rating vs Black Win:")
print(f"  chi2 = {chi2_b:.3f}, p = {p_b:.6f}, Cramer's V = {cramers_v_b:.3f}")
print(f"  Win rates:\n  {(ct_b[1] / ct_b.sum(axis=1) * 100).round(1)}")

#Q5 95% CIs for rated vs unrated turns — parametric + bootstrap
from scipy.stats import t as t_dist
def confidence_interval(data, confidence=0.95):
    n = len(data); mean = data.mean(); se = stats.sem(data)
    h = se * t_dist.ppf((1 + confidence) / 2., n - 1)
    return mean - h, mean + h
rated_turns = df[df['rated'] == True]['turns']
lo, hi = confidence_interval(rated_turns)
print(f"95% CI for rated turns: ({lo:.2f}, {hi:.2f})") 
# Bootstrap CI — no normality assumption required
def bootstrap_ci(data, n_boot=1000, confidence=0.95):
    rng = np.random.default_rng(42)
    means = [rng.choice(data, len(data), replace=True).mean() for _ in range(n_boot)]
    a = (1 - confidence) / 2
    return np.percentile(means, [a*100, (1-a)*100])
lo_b, hi_b = bootstrap_ci(rated_turns.values)
print(f"Bootstrap 95% CI for rated turns: ({lo_b:.2f}, {hi_b:.2f})") 
####################
unrated = df[df['rated'] == False]['turns']
lo_un, hi_un = confidence_interval(unrated)
print(f"95% CI for unrated turns: ({lo_un:.2f}, {hi_un:.2f})") 
# Bootstrap CI — no normality assumption required
lo_b_un, hi_b_un = bootstrap_ci(unrated.values)
print(f"Bootstrap 95% CI for unrated turns: ({lo_b_un:.2f}, {hi_b_un:.2f})") 