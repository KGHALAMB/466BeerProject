import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



top_n = 10

locations = pd.read_csv('beer_with_locations.csv')

    
def city_counts():
    l = locations['City'].value_counts().head(top_n).reset_index()
    l.columns = ['City', 'Review Count']
    l

    plt.figure(figsize=(10, 8))
    sns.barplot(x='Review Count', y='City', data=l, palette='YlOrBr_d', hue='City', legend=False)

    plt.title('Top 10 Cities by Review Count')
    plt.xlabel('Review Count')
    plt.ylabel('City')
    plt.tight_layout()

    plt.show()
    
def city_avg_review():
    l = locations.groupby('City')['review_overall'].agg(['mean', 'count']).reset_index()
    l = l[ l['count'] > 10]
    l = l.groupby('City').head(top_n).reset_index()
    l = l[['City', 'mean', 'count']]
    l = l.sort_values('mean', ascending=[False]).head(10)
    l = l.rename(columns = {"count":'Review Counts'})


    plt.figure(figsize=(10, 8))


    ax = sns.barplot(x='City', y='mean', data=l, palette='YlOrBr_d', hue='Review Counts', legend=True)
    ax.set_ylim(3.5,4.6)

    sns.move_legend(ax, "upper right", fontsize=15)
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f')

    plt.title('Average Review by City')
    plt.xlabel('City')
    plt.ylabel('Average Review')
    plt.tight_layout()

    plt.show()
    
    
def beer_style():
    Style = locations['Style'].value_counts().head(top_n).reset_index()
    Style.columns = ['Style', 'count']


    plt.figure(figsize=(10, 8))
    sns.barplot(x='count', y='Style', data=Style, palette='YlOrBr_r', hue='Style', legend=False)

    plt.title('Top 10 Beer Styles by Review Count')
    plt.xlabel('Review Count')
    plt.ylabel('Beer Style')
    plt.tight_layout()

    plt.show()

# city_counts()
# city_avg_review()
# beer_style()
print("here")
# print(locations.head)
# locations['Review Count'].value_counts()



plt.figure(figsize=(10, 8))

sns.lineplot(y=locations['number_of_reviews'], x=locations['review_overall'], color='#a68268')

plt.axvline(x = 3, color = 'green', label = 'axvline - full height')
plt.axvline(x = 4.25, color = 'green', label = 'axvline - full height')

plt.title('Distribution of Overall Review')
plt.xlabel('Overall Review')
plt.ylabel('Number of Reviews')
plt.show()