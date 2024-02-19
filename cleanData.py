
def categorizeBeers(x):
    if x > 4.5:
        return "Good"
    elif x > 3:
        return "Okay"
    else:
        return "Bad"

def avgIBU(df):
    df["avg_IBU"] = df.apply(lambda x: (x['Max IBU'] + x['Min IBU'])/2, axis = 1)
    return df

def goodBeer(df):
    df["good_beer"] = df.apply(lambda x: categorizeBeers(x['review_overall']), axis=1)
    return df

def cleanAllData(df):
    return goodBeer(avgIBU(df))
