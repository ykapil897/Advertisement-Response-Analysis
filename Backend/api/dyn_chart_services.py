from django.conf import settings
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io 
import base64
import plotly.express as px

def get_chart_names_list():
    chart_names = [
        {"value": "ad_platform_type_vs_ad_type", "label": "Ad Platform Type and Ad Type"},
        {"value": "ad_platform_type_vs_ad_cost_efficiency", "label": "Ad Platform Type vs Ad Cost Efficiency"},
        {"value": "income_level_vs_engagement_time", "label": "Income Level vs Engagement Time"},
        {"value": "response_type_by_ad_platform", "label": "Response Type by Ad Platform"},
        # Add more chart names as needed
    ]
    return chart_names

def fetch_data_from_mongo(collection_name):
    collection = settings.MONGO_DB[collection_name]
    data = list(collection.find({}, {"_id": 0}))  # Exclude the MongoDB ID from the results
    return data

def generate_summary_from_metrics(data_description, metrics):
    """Generate a summary from metrics using a hard-coded template."""
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
    plt.close()

    # Generate metrics and summary
    columns = ['AdPlatformType', 'AdType']
    metrics = create_analysis_metrics(df, columns)
    summary = generate_summary_from_metrics('Ad Platform Type and Ad Type', metrics)
    return buf, summary

def create_custom_chart(chart):
    chart = [
        {"title": "Ad Platform Type and Ad Type", "image": base64.b64encode(create_ad_platform_type_chart()[0].getvalue()).decode('utf-8'), "summary": create_ad_platform_type_chart()[1]},
    ]
    return chart