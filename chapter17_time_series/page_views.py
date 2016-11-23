import urllib, json, pandas as pd, numpy as np, \
    sklearn.linear_model, statsmodels.api as sm \
    matplotlib.pyplot as plt

START_DATE = "20131010"
END_DATE = "20161012"
WINDOW_SIZE = 7
TOPIC = "Cat"
URL_TEMPLATE = ("https://wikimedia.org/api/rest_v1"     
    "/metrics/pageviews/per-article"
    "/en.wikipedia/all-access/"
    "allagents/%s/daily/%s/%s")

def get_time_series(topic, start, end):
    url = URL_TEMPLATE % (topic, start, end)
    json_data = urllib.urlopen(url).read()
    data = json.loads(json_data)
    times = [rec['timestamp']
        for rec in data['items']]
    values = [rec['views'] for rec in data['items']]
    times_formatted = pd.Series(times).map(
        lambda x: x[:4]+'-'+x[4:6]+'-'+x[6:8])
    time_index = times_formatted.astype('datetime64')
    return pd.DataFrame(
        {'views': values}, index=time_index)

def line_slope(ss):
    X=np.arange(len(ss)).reshape((len(ss),1))
    linear.fit(X, ss)
    return linear.coef_

# LinearRegression object will be
# re-used several times
linear = sklearn.linear_model.LinearRegression()

df = get_time_series(TOPIC, START_DATE, END_DATE)

# Visualize the raw time series
df['views'].plot()
plt.title("Page Views by Day")
plt.show()

# Blunt-force way to remove outliers
max_views = df['views'].quantile(0.95)
df.views[df.views > max_views] = max_views

# Visualize decomposition
decomp = sm.tsa.seasonal_decompose(df['views'].values, freq=7)
decomp.plot()
plt.suptitle("Page Views Decomposition")
plt.show()

# For each day, add features from previous week
df['mean_1week'] = pd.rolling_mean(
    df['views'], WINDOW_SIZE)
df['max_1week'] = pd.rolling_max(
    df['views'], WINDOW_SIZE)
df['min_1week'] = pd.rolling_min(
    df['views'], WINDOW_SIZE)
df['slope'] = pd.rolling_apply(
    df['views'], WINDOW_SIZE, line_slope)
df['total_views_week'] = pd.rolling_sum(
    df['views'], WINDOW_SIZE)
df['day_of_week'] = df.index.astype(int) % 7
day_of_week_cols = pd.get_dummies(df['day_of_week'])
df = pd.concat([df, day_of_week_cols], axis=1)

# Make target variable that we
# want to predict: views NEXT week.
# Must pad w NANs so dates line up
df['total_views_next_week'] = list(df['total_views_week'][WINDOW_SIZE:]) + \
    [np.nan for _ in range(WINDOW_SIZE)]

INDEP_VARS = ['mean_1week', 'max_1week',
    'min_1week', 'slope'] + range(6)
DEP_VAR = 'total_views_next_week'

n_records = df.dropna().shape[0]
test_data = df.dropna()[:n_records/2]
train_data = df.dropna()[n_records/2:]

linear.fit(
    train_data[INDEP_VARS], train_data[DEP_VAR])

test_preds_array = linear.predict(
    test_data[INDEP_VARS])
test_preds = pd.Series(
    test_preds_array, index=test_data.index)
print "Corr on test data:", \
    test_data[DEP_VAR].corr(test_preds)
