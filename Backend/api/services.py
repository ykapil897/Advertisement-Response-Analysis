from django.conf import settings
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import plotly.express as px

# Use the Agg backend for Matplotlib
plt.switch_backend('Agg')

def fetch_data_from_mongo(collection_name):
    collection = settings.MONGO_DB[collection_name]
    data = list(collection.find({}, {"_id": 0}))  # Exclude the MongoDB ID from the results
    return data

def create_ad_platform_type_chart():
    data = fetch_data_from_mongo("advertisement_info")
    df = pd.DataFrame(data)

    # Create the stacked bar plot
    pivot_df = df.pivot_table(index='AdPlatformType', columns='AdType', aggfunc='size', fill_value=0)
    pivot_df.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='viridis')
    plt.title('Ad Platform Type and Ad Type')
    plt.xlabel('Ad Platform Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend(title='Ad Type', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf

def create_purchase_location_chart():
    data = fetch_data_from_mongo("purchase_info")
    df = pd.DataFrame(data)

    # Create the stacked bar plot
    pivot_df = df.pivot_table(index='PurchaseLocation', columns='InfluenceFactor', aggfunc='size', fill_value=0)
    pivot_df.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='viridis')
    plt.title('Purchase Location and Influence Factor')
    plt.xlabel('Purchase Location')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend(title='Influence Factor', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf

def create_engagement_time_chart():
    data = fetch_data_from_mongo("responses_to_ads")
    df = pd.DataFrame(data)

    # Create the stacked bar plot
    pivot_df = df.pivot_table(index='Engagement_Time', columns='Rating', aggfunc='size', fill_value=0)
    pivot_df.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='viridis')
    plt.title('Engagement Time and Rating')
    plt.xlabel('Engagement Time')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend(title='Rating', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf

def create_response_type_chart():
    data = fetch_data_from_mongo("responses_to_ads")
    df = pd.DataFrame(data)

    # Create the stacked bar plot
    pivot_df = df.pivot_table(index='ResponseType', columns='PurchaseIntent', aggfunc='size', fill_value=0)
    pivot_df.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='viridis')
    plt.title('Response Type and Purchase Intent')
    plt.xlabel('Response Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend(title='Purchase Intent', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf

def create_response_date_chart():
    data = fetch_data_from_mongo("responses_to_ads")
    df = pd.DataFrame(data)

    # Convert date to datetime
    df['Response_Date'] = pd.to_datetime(df['Response_Date'])

    # Create the line chart
    df.set_index('Response_Date').resample('D').size().plot(kind='line', figsize=(12, 8))
    plt.title('Number of Responses Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Responses')
    plt.xticks(rotation=45)
    plt.legend('')

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf

def create_age_range_pie_chart():
    data = fetch_data_from_mongo("survey_respondents")
    df = pd.DataFrame(data)

    # Create the pie chart using Plotly
    fig = px.pie(df, names='Age', title='Number of Respondents in Various Age Ranges', color_discrete_sequence=px.colors.sequential.Viridis)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    fig.write_image(buf, format='png')
    buf.seek(0)
    return buf

def create_income_range_chart():
    data = fetch_data_from_mongo("survey_respondents")
    df = pd.DataFrame(data)

    # Create the stacked bar plot
    pivot_df = df.pivot_table(index='Income Level', columns='Location', aggfunc='size', fill_value=0)
    pivot_df.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='viridis')
    plt.title('Income Level and Location')
    plt.xlabel('Income Level')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend(title='Location', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf

def create_all_charts():
    charts = [
        {"title": "Ad Platform Type and Ad Type", "image": base64.b64encode(create_ad_platform_type_chart().getvalue()).decode('utf-8')},
        {"title": "Purchase Location and Influence Factor", "image": base64.b64encode(create_purchase_location_chart().getvalue()).decode('utf-8')},
        {"title": "Engagement Time and Rating", "image": base64.b64encode(create_engagement_time_chart().getvalue()).decode('utf-8')},
        {"title": "Response Type and Purchase Intent", "image": base64.b64encode(create_response_type_chart().getvalue()).decode('utf-8')},
        {"title": "Number of Responses Over Time", "image": base64.b64encode(create_response_date_chart().getvalue()).decode('utf-8')},
        {"title": "Number of Respondents in Various Age Ranges", "image": base64.b64encode(create_age_range_pie_chart().getvalue()).decode('utf-8')},
        {"title": "Income Level and Location", "image": base64.b64encode(create_income_range_chart().getvalue()).decode('utf-8')}
    ]
    return charts