
def categorizeBeers(x): #helper function for goodBeer()
    if x > 4.25:
        return "Good"
    elif x > 3:
        return "Okay"
    else:
        return "Bad"

def avgIBU(df): # gets the middle value of the Max and Min IBU's 
    df["avg_IBU"] = df.apply(lambda x: (x['Max IBU'] + x['Min IBU'])/2, axis = 1)
    return df

def goodBeer(df): # this function assigns either, Good Okay or Bad to a beer based on it's rating score
    df["good_beer"] = df.apply(lambda x: categorizeBeers(x['review_overall']), axis=1)
    return df

def cleanAllData(df): # does all cleaning methods at once for ease of use
    return goodBeer(avgIBU(df))
