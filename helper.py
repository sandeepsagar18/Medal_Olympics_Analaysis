import numpy as np


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values(
            by=['Gold', 'Silver', 'Bronze'], ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

def data_over_time(df,col):

    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    if 'index' in nations_over_time.columns:
        nations_over_time = nations_over_time.sort_values('index')
        nations_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    else:
        nations_over_time = nations_over_time.sort_values('Year')
        nations_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)
    return nations_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    counts = temp_df['Name'].value_counts().reset_index().head(15)
    name_col = 'Name' if 'count' in counts.columns else 'index'
    count_col = 'count' if 'count' in counts.columns else 'Name'

    x = counts.merge(df, left_on=name_col, right_on='Name', how='left')[
        [name_col, count_col, 'Sport', 'region']].drop_duplicates(name_col)
    x.rename(columns={name_col: 'Name', count_col: 'Medals'}, inplace=True)
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    counts = temp_df['Name'].value_counts().reset_index().head(10)
    name_col = 'Name' if 'count' in counts.columns else 'index'
    count_col = 'count' if 'count' in counts.columns else 'Name'

    x = counts.merge(df, left_on=name_col, right_on='Name', how='left')[
        [name_col, count_col, 'Sport']].drop_duplicates(name_col)
    x.rename(columns={name_col: 'Name', count_col: 'Medals'}, inplace=True)
    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df = athlete_df.copy()
    athlete_df['Medal'] = athlete_df['Medal'].fillna('No Medal')
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final


def compare_countries(df, country1, country2):
    df1 = yearwise_medal_tally(df, country1)
    df2 = yearwise_medal_tally(df, country2)
    merged = df1.merge(df2, on='Year', how='outer', suffixes=(f'_{country1}', f'_{country2}'))
    merged = merged.sort_values('Year').fillna(0)
    merged[f'Medal_{country1}'] = merged[f'Medal_{country1}'].astype(int)
    merged[f'Medal_{country2}'] = merged[f'Medal_{country2}'].astype(int)
    return merged
