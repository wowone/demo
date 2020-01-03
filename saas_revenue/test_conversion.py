rename_dict = {
    '1month': '1month_trial_old',
    '1month2': '1month_trial',
    'sale1year': '1year_trial_old',
    'sale1year2': '1year_trial',
    'sale1year3': '1year_instant'
}
df_ios = pd.read_csv('recurrent_iphone.csv')
df_ios['product_id'] = df_ios['product_id'].map(rename_dict)
df_ios = df_ios[df_ios['product_id'].notnull()]
df_ios['platform'] = 'iOS'

rename_dict = {
    '1month': '1month_trial',
    '1yearsale': '1year_trial_old',
    '1yearsale2': '1year_trial',
    'instant.1yearsale': '1year_instant'
}
df_and = pd.read_csv('recurrent_android.csv')
df_and['product_id'] = df_and['product_id'].map(rename_dict)
df_and = df_and[df_and['product_id'].notnull()]
df_and['platform'] = 'Android'

df = pd.concat([df_ios, df_and], sort=True)
df = df[['date', 'platform', 'product_id', 'duration', 'billing_cycle', 'purchases']]


def get_max_billing_cycle(group):
    duration = group.name[2]
    min_date, max_date = group['date'].min(), plan_date1
    max_bc = int((len(pd.date_range(min_date, max_date, freq='MS'))) / duration) + 1
    return pd.Series({'max_bc': max_bc, 'launch_date': min_date})
max_bc = df.groupby(['platform', 'product_id', 'duration'])\
           .apply(get_max_billing_cycle)
df = pd.merge(df, max_bc, on=['platform', 'product_id', 'duration'])
df['date'] = pd.to_datetime(df['date'])
df['launch_date'] = pd.to_datetime(df['launch_date'])

def filter_wrong_bc(x): 
    if x['duration'] == 1:
        return x['date'] - pd.DateOffset(months=x['billing_cycle'] - 1) >= x['launch_date']
    if x['duration'] == 12:
        return x['date'] - pd.DateOffset(years=x['billing_cycle'] - 1) >= x['launch_date']
    
df = df[df.apply(filter_wrong_bc, axis=1)].drop(['max_bc', 'launch_date'], axis=1)
df.to_csv('recurrent.csv', index=False)
