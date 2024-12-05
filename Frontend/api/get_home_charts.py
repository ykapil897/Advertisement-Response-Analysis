import json
import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import pymongo
import plotly.express as px

# Use the Agg backend for Matplotlib (no GUI)
plt.switch_backend('Agg')

MONGO_CLIENT = pymongo.MongoClient("mongodb+srv://vivek27:vivek%4027@cluster0.clnya.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0") # for mongodb atlas 
MONGO_DB = MONGO_CLIENT["ad_response_analysis_tf"]

def fetch_data_from_mongo(collection_name):
    collection = MONGO_DB[collection_name]
    data = list(collection.find({}, {"_id": 0}))  # Exclude the MongoDB ID from the results
    return data

# Helper function to create summary (you can modify the logic as needed)
def generate_summary_from_metrics(data_description, metrics):
    summary = f"Summary for {data_description}:\n\n"
    for column, metric in metrics.items():
        summary += f"Column: {column}\n"
        if 'mean' in metric:
            summary += f"  - Mean: {metric['mean']:.2f}\n"
            summary += f"  - Median: {metric['median']:.2f}\n"
            summary += f"  - Standard Deviation: {metric['std']:.2f}\n"
        else:
            summary += f"  - Unique Values: {metric['unique_values']}\n"
            summary += f"  - Value Counts: {metric['value_counts']}\n"
        summary += "\n"
    summary += "Key Insights:\n"
    summary += "  - The data shows significant patterns and trends.\n"
    summary += "  - Further analysis is recommended to derive actionable insights.\n"
    return summary

def create_analysis_metrics(df, columns):
    """Create analysis metrics based on column types"""
    metrics = {}
    
    for col in columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            metrics[col] = {
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std()
            }
        else:
            metrics[col] = {
                'value_counts': df[col].value_counts().to_dict(),
                'unique_values': len(df[col].unique())
            }
    
    return metrics

# The serverless function entry point
def handler(request):

    def create_income_vs_engagement_time_box_plot():
        survey_data = fetch_data_from_mongo("survey_respondents")
        response_data = fetch_data_from_mongo("responses_to_ads")
        survey_df = pd.DataFrame(survey_data)
        response_df = pd.DataFrame(response_data)

        # Merge dataframes on a common key (assuming 'RespondentID' is the common key)
        merged_df = pd.merge(survey_df, response_df, on='RespondentID')

        # Check for missing values
        # print("Merged DataFrame head:\n", merged_df.head())
        # print("Merged DataFrame info:\n", merged_df.info())

        # Drop rows with missing values in the columns used for plotting
        merged_df = merged_df.dropna(subset=['Income Level', 'Engagement_Time'])

        # Ensure Engagement_Time is treated as a categorical variable
        merged_df['Engagement_Time'] = pd.Categorical(merged_df['Engagement_Time'])

        # Create the box plot
        plt.figure(figsize=(12, 8))
        sns.boxplot(x='Income Level', y='Engagement_Time', data=merged_df)
        plt.title('Income Level vs. Engagement Time')
        plt.xlabel('Income Level')
        plt.ylabel('Engagement Time')
        plt.xticks(rotation=45)

        # Save the plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()

        # Generate metrics and summary
        columns = ['Income Level', 'Engagement_Time']
        metrics = create_analysis_metrics(merged_df, columns)
        summary = generate_summary_from_metrics('Income Level vs. Engagement Time', metrics)

        return buf, summary

    def create_response_type_by_ad_platform_grouped_bar_chart():
        ad_data = fetch_data_from_mongo("advertisement_info")
        response_data = fetch_data_from_mongo("responses_to_ads")
        ad_df = pd.DataFrame(ad_data)
        response_df = pd.DataFrame(response_data)

        # Merge dataframes on a common key (assuming 'AdID' is the common key)
        merged_df = pd.merge(ad_df, response_df, on='AdID')

        # Create the grouped bar chart
        pivot_df = merged_df.pivot_table(index='AdPlatformType', columns='ResponseType', aggfunc='size', fill_value=0)
        pivot_df.plot(kind='bar', figsize=(12, 8), colormap='viridis')
        plt.title('Response Type by Ad Platform')
        plt.xlabel('Ad Platform Type')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.legend(title='Response Type', bbox_to_anchor=(1.05, 1), loc='upper left')

        # Save the plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()

        # Generate metrics and summary
        columns = ['AdPlatformType', 'ResponseType']
        metrics = create_analysis_metrics(merged_df, columns)
        summary = generate_summary_from_metrics('Response Type by Ad Platform', metrics)

        return buf, summary

    def create_engagement_time_per_ad_type_box_plot():
        ad_data = fetch_data_from_mongo("advertisement_info")
        response_data = fetch_data_from_mongo("responses_to_ads")
        ad_df = pd.DataFrame(ad_data)
        response_df = pd.DataFrame(response_data)

        # Merge dataframes on a common key (assuming 'AdID' is the common key)
        merged_df = pd.merge(ad_df, response_df, on='AdID')

        # Check for missing values
        # print("Merged DataFrame head:\n", merged_df.head())
        # print("Merged DataFrame info:\n", merged_df.info())

        # Drop rows with missing values in the columns used for plotting
        merged_df = merged_df.dropna(subset=['AdType', 'Engagement_Time'])

        merged_df['Engagement_Time'] = pd.Categorical(merged_df['Engagement_Time'])
        
        # Create the box plot
        plt.figure(figsize=(12, 8))
        sns.boxplot(x='AdType', y='Engagement_Time', data=merged_df)
        plt.title('Engagement Time per Ad Type')
        plt.xlabel('Ad Type')
        plt.ylabel('Engagement Time')
        plt.xticks(rotation=45)

        # Save the plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()

        # Generate metrics and summary
        columns = ['AdType', 'Engagement_Time']
        metrics = create_analysis_metrics(merged_df, columns)
        summary = generate_summary_from_metrics('Engagement Time per Ad Type', metrics)

        return buf, summary

    def create_ctr_by_ad_topic_bar_chart():
        ad_data = fetch_data_from_mongo("advertisement_info")
        ad_metrics_data = fetch_data_from_mongo("ad_metrics")
        ad_df = pd.DataFrame(ad_data)
        ad_metrics_df = pd.DataFrame(ad_metrics_data)

        # Merge dataframes on a common key (assuming 'AdID' is the common key)
        merged_df = pd.merge(ad_df, ad_metrics_df, on='AdID')

        # Create the bar chart
        plt.figure(figsize=(12, 8))
        sns.barplot(x='AdTopic', y='Click_Through_Rate', data=merged_df)
        plt.title('Click-Through Rate by Ad Topic')
        plt.xlabel('Ad Topic')
        plt.ylabel('Click-Through Rate')
        plt.xticks(rotation=45)

        # Save the plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()

        # Generate metrics and summary
        columns = ['AdTopic', 'Click_Through_Rate']
        metrics = create_analysis_metrics(merged_df, columns)
        summary = generate_summary_from_metrics('Click-Through Rate by Ad Topic', metrics)

        return buf, summary

    def create_engagement_time_by_device_and_location_heatmap():
        survey_data = fetch_data_from_mongo("survey_respondents")
        response_data = fetch_data_from_mongo("responses_to_ads")
        survey_df = pd.DataFrame(survey_data)
        response_df = pd.DataFrame(response_data)

        # Merge dataframes on a common key (assuming 'RespondentID' is the common key)
        merged_df = pd.merge(survey_df, response_df, on='RespondentID')

        # Check for missing values
        # print("Merged DataFrame head:\n", merged_df.head())
        # print("Merged DataFrame info:\n", merged_df.info())

        # Drop rows with missing values in the columns used for plotting
        merged_df = merged_df.dropna(subset=['DeviceType', 'Location', 'Engagement_Time'])

        # Convert Engagement_Time to numeric by taking the midpoint of the ranges
        def convert_to_midpoint(time_range):
            start, end = map(int, time_range.split('-'))
            return (start + end) / 2

        merged_df['Engagement_Time_Numeric'] = merged_df['Engagement_Time'].apply(convert_to_midpoint)

        # Create the heatmap
        pivot_df = merged_df.pivot_table(index='DeviceType', columns='Location', values='Engagement_Time_Numeric', aggfunc='mean')
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot_df, annot=True, cmap='viridis')
        plt.title('Engagement Time by Device Type and Location')
        plt.xlabel('Location')
        plt.ylabel('Device Type')

        # Save the plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()

        # Generate metrics and summary
        columns = ['DeviceType', 'Location', 'Engagement_Time_Numeric']
        metrics = create_analysis_metrics(merged_df, columns)
        summary = generate_summary_from_metrics('Engagement Time by Device Type and Location', metrics)

        return buf, summary

    def create_ad_cost_vs_rating_scatter_plot():
        ad_data = fetch_data_from_mongo("advertisement_info")
        response_data = fetch_data_from_mongo("responses_to_ads")
        ad_df = pd.DataFrame(ad_data)
        response_df = pd.DataFrame(response_data)

        # Merge dataframes on a common key (assuming 'AdID' is the common key)
        merged_df = pd.merge(ad_df, response_df, on='AdID')

        # Create the scatter plot
        plt.figure(figsize=(12, 8))
        sns.scatterplot(x='AdCost', y='Rating', data=merged_df)
        plt.title('Ad Cost vs. Rating')
        plt.xlabel('Ad Cost')
        plt.ylabel('Rating')

        # Save the plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()

        # Generate metrics and summary
        columns = ['AdCost', 'Rating']
        metrics = create_analysis_metrics(merged_df, columns)
        summary = generate_summary_from_metrics('Ad Cost vs. Rating', metrics)

        return buf, summary

    def create_ad_platform_type_and_cost_efficiency_bubble_chart():
        ad_data = fetch_data_from_mongo("advertisement_info")
        ad_metrics_data = fetch_data_from_mongo("ad_metrics")
        ad_df = pd.DataFrame(ad_data)
        ad_metrics_df = pd.DataFrame(ad_metrics_data)

        # Merge dataframes on a common key (assuming 'AdID' is the common key)
        merged_df = pd.merge(ad_df, ad_metrics_df, on='AdID')

        # Convert Mode_Engagement_Time to numeric, forcing errors to NaN
        merged_df['Mode_Engagement_Time'] = pd.to_numeric(merged_df['Mode_Engagement_Time'], errors='coerce')

        # Drop rows with NaN values in Mode_Engagement_Time
        merged_df = merged_df.dropna(subset=['Mode_Engagement_Time'])

        # Create the bubble chart using Plotly
        fig = px.scatter(merged_df, x='AdCost', y='Click_Through_Rate', size='Mode_Engagement_Time', color='AdPlatformType',
                        title='Ad Platform Type and Ad Cost Efficiency', labels={'AdCost': 'Ad Cost', 'Click_Through_Rate': 'Click-Through Rate'})
        fig.update_layout(legend_title_text='Ad Platform Type')

        # Save the plot to a BytesIO object
        buf = io.BytesIO()
        fig.write_image(buf, format='png')
        buf.seek(0)
        plt.close()

        # Generate metrics and summary
        columns = ['AdCost', 'Click_Through_Rate', 'Mode_Engagement_Time', 'AdPlatformType']
        metrics = create_analysis_metrics(merged_df, columns)
        summary = generate_summary_from_metrics('Ad Platform Type and Ad Cost Efficiency', metrics)

        return buf, summary

    def create_conversion_rate_by_ad_duration_line_chart():
        ad_data = fetch_data_from_mongo("advertisement_info")
        ad_metrics_data = fetch_data_from_mongo("ad_metrics")
        ad_df = pd.DataFrame(ad_data)
        ad_metrics_df = pd.DataFrame(ad_metrics_data)

        # Merge dataframes on a common key (assuming 'AdID' is the common key)
        merged_df = pd.merge(ad_df, ad_metrics_df, on='AdID')

        # Create the line chart
        plt.figure(figsize=(12, 8))
        sns.lineplot(x='AdDuration', y='Conversion_Rate', data=merged_df)
        plt.title('Conversion Rate by Ad Duration')
        plt.xlabel('Ad Duration')
        plt.ylabel('Conversion Rate')
        plt.xticks(rotation=45)

        # Save the plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()

        # Generate metrics and summary
        columns = ['Conversion_Rate', 'AdDuration']
        metrics = create_analysis_metrics(merged_df, columns)
        summary = generate_summary_from_metrics('Conversion Rate by Ad Duration', metrics)

        return buf, summary

    def create_all_charts():
        charts = [
            # {"title": "Ad Platform Type and Ad Type", "image": base64.b64encode(create_ad_platform_type_chart().getvalue()).decode('utf-8')},
            # {"title": "Purchase Location and Influence Factor", "image": base64.b64encode(create_purchase_location_chart().getvalue()).decode('utf-8')},
            # {"title": "Engagement Time and Rating", "image": base64.b64encode(create_engagement_time_chart().getvalue()).decode('utf-8')},
            # {"title": "Response Type and Purchase Intent", "image": base64.b64encode(create_response_type_chart().getvalue()).decode('utf-8')},
            # {"title": "Number of Responses Over Time", "image": base64.b64encode(create_response_date_chart().getvalue()).decode('utf-8')},
            # {"title": "Number of Respondents in Various Age Ranges", "image": base64.b64encode(create_age_range_pie_chart().getvalue()).decode('utf-8')},
            # {"title": "Income Level and Location", "image": base64.b64encode(create_income_range_chart().getvalue()).decode('utf-8')},

            {"title": "Ad Platform Type and Ad Cost Efficiency", "image": base64.b64encode(create_ad_platform_type_and_cost_efficiency_bubble_chart()[0].getvalue()).decode('utf-8'), "summary": create_ad_platform_type_and_cost_efficiency_bubble_chart()[1]},
            {"title": "Income Level vs. Engagement Time", "image": base64.b64encode(create_income_vs_engagement_time_box_plot()[0].getvalue()).decode('utf-8'), "summary": create_income_vs_engagement_time_box_plot()[1]},
            {"title": "Response Type by Ad Platform", "image": base64.b64encode(create_response_type_by_ad_platform_grouped_bar_chart()[0].getvalue()).decode('utf-8'), "summary": create_response_type_by_ad_platform_grouped_bar_chart()[1]},
            {"title": "Engagement Time per Ad Type", "image": base64.b64encode(create_engagement_time_per_ad_type_box_plot()[0].getvalue()).decode('utf-8'), "summary": create_engagement_time_per_ad_type_box_plot()[1]},
            {"title": "Click-Through Rate by Ad Topic", "image": base64.b64encode(create_ctr_by_ad_topic_bar_chart()[0].getvalue()).decode('utf-8'), "summary": create_ctr_by_ad_topic_bar_chart()[1]},
            {"title": "Engagement Time by Device Type and Location", "image": base64.b64encode(create_engagement_time_by_device_and_location_heatmap()[0].getvalue()).decode('utf-8'), "summary": create_engagement_time_by_device_and_location_heatmap()[1]},
            # {"title": "Ad Cost vs. Rating", "image": base64.b64encode(create_ad_cost_vs_rating_scatter_plot()[0].getvalue()).decode('utf-8'), "summary": create_ad_cost_vs_rating_scatter_plot()[1]},
            {"title": "Conversion Rate by Ad Duration", "image": base64.b64encode(create_conversion_rate_by_ad_duration_line_chart()[0].getvalue()).decode('utf-8'), "summary": create_conversion_rate_by_ad_duration_line_chart()[1]}
        ]
        return charts
    
    images = create_all_charts()
    # response = JsonResponse(images, safe=False)
    # return response
    # Return the plot and summary as JSON response
    return {
        "statusCode": 200,
        "body": json.dumps(images),
        "headers": {
            "Content-Type": "application/json"
        }
    }
