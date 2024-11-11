from django.conf import settings
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

def fetch_data_from_mongo(collection_name="survey_respondents"):
    collection = settings.MONGO_DB[collection_name]
    data = list(collection.find({}, {"_id": 0}))  # Exclude the MongoDB ID from the results
    return data

def create_ad_topic_percentage_plot():
    data = fetch_data_from_mongo(collection_name="advertisement_info")
    df = pd.DataFrame(data)

    # Calculate the percentage of each ad topic per platform
    topic_counts = df.groupby(['AdPlatformName', 'AdTopic']).size().reset_index(name='counts')
    platform_counts = df['AdPlatformName'].value_counts().reset_index()
    platform_counts.columns = ['AdPlatformName', 'total_counts']
    merged_df = pd.merge(topic_counts, platform_counts, on='AdPlatformName')
    merged_df['percentage'] = (merged_df['counts'] / merged_df['total_counts']) * 100

    # Pivot the data for plotting
    pivot_df = merged_df.pivot(index='AdPlatformName', columns='AdTopic', values='percentage').fillna(0)

    # Create the stacked bar plot
    pivot_df.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='viridis')
    plt.title('Percentage of Ad Topics by Platform')
    plt.xlabel('Platform Name')
    plt.ylabel('Percentage')
    plt.xticks(rotation=45)
    plt.legend(title='Ad Topic', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf