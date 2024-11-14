import pandas as pd
import random
from datetime import datetime, timedelta

# Constants for random data generation
AGE_RANGES = ["<18", "18-30", "30-45", "45-60", ">60"]
GENDER_OPTIONS = ["Male", "Female", "Other"]
LOCATION_OPTIONS = ["Urban", "Rural", "Sub-urban"]
INCOME_LEVEL_WEIGHTS = {
    "Urban": {">100k": 0.4, "50k-100k": 0.3, "20k-50k": 0.2, "<20k": 0.1},
    "Sub-urban": {">100k": 0.2, "50k-100k": 0.4, "20k-50k": 0.3, "<20k": 0.1},
    "Rural": {">100k": 0.15, "50k-100k": 0.2, "20k-50k": 0.4, "<20k": 0.25}
}
INCOME_LEVELS = [">100k", "50k-100k", "20k-50k", "<20k"]
EDUCATION_LEVELS = ["High School", "Bachelors", "Masters", "PhD"]
OCCUPATIONS = ["Teacher", "Engineer", "Doctor", "Artist", "Marketing Manager", "Salesperson"]

PLATFORM_TYPES = {
    "TV": ["News Channel", "Movie Channel", "Sports Channel", "Music Channel", "Kids Channel"],
    "Search Engine": ["Google", "Bing", "Yahoo"],
    "Social Media": ["Facebook", "YouTube", "Instagram", "Twitter", "LinkedIn", "Snapchat", "Threads"],
    "Streaming": ["Netflix", "Amazon Prime", "Hotstar", "JioTV", "Zee5"],
}
AD_TYPES = ["Video", "Banner", "Text"]
TOPICS = ["Education", "Healthcare", "Finance", "Entertainment", "Sports", "Technology", "Fashion", "Food", "Travel", "Automobile", "Real Estate", "Political"]
RESPONSE_TYPES = ["Clicked", "Ignored"]
PURCHASE_INTENT = ["Yes", "No"]
RELEVANT = ["Yes", "No"]
DEVICE_TYPES = ["Mobile", "Desktop", "Tablet"]
INFLUENCE_FACTORS_ONLINE = ["Brand Value", "Discount", "Peer Recommendations", "Past Experience"]
INFLUENCE_FACTORS_INSTORE = ["Peer Recommendations", "Past Experience", "Brand Value", "Discount"]
PURCHASE_LOCATIONS = ["Online", "In-store"]
AD_INFLUENCE = ["Yes", "No"]
AGE_GROUPS = ["<18", "18-30", "30-45", "45-60", ">60"]
RATINGS = [1, 2, 3, 4, 5]

# Helper functions
def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

# Generate Survey_Respondents data with skew towards younger ages and income levels
def generate_survey_respondents(num=1000):
    data = []
    for i in range(1, num + 1):
        gender = "Other" if random.random() < 0.05 else random.choice(["Male", "Female"])
        location = random.choices(LOCATION_OPTIONS, weights=[0.5, 0.3, 0.2])[0]
        age = random.choices(range(12, 99), weights=[5] * 20 + [3] * 20 + [1] * 47, k=1)[0]
        
        # Select income level based on location probabilities
        income_level_choices, income_weights = zip(*INCOME_LEVEL_WEIGHTS[location].items())
        income_level = random.choices(income_level_choices, weights=income_weights, k=1)[0]
        
        respondent = {
            "RespondentID": i,
            "Age": age,
            "Gender": gender,
            "Location": location,
            "Income Level": income_level,
            "Education Level": random.choice(EDUCATION_LEVELS),
            "Occupation": random.choice(OCCUPATIONS)
        }
        data.append(respondent)
    return pd.DataFrame(data)

# Generate Advertisement_Info data with probabilistic platform types and names
def generate_advertisement_info(num=100):
    data = []
    for i in range(1, num + 1):
        platform_type = random.choices(list(PLATFORM_TYPES.keys()), weights=[0.2, 0.2, 0.3, 0.3])[0]
        platform_name = random.choice(PLATFORM_TYPES[platform_type])
        
        ad_info = {
            "AdID": i,
            "AdPlatformType": platform_type,
            "AdPlatformName": platform_name,
            "AdType": random.choice(AD_TYPES),
            "AdTopic": random.choice(TOPICS),
            "AdDuration": random.randint(10, 600),
            "AdCost": random.uniform(100.0, 1000.0),
            "PurchaseAmount": random.uniform(500.0, 5000.0)
        }
        data.append(ad_info)
    return pd.DataFrame(data)

# Function to generate responses_to_ads data with probabilistic purchase intent and conditional ratings
def generate_responses_to_ads(advertisement_info, num=10000, respondents=1000):
    data = []
    ads = advertisement_info['AdID'].unique()
    
    for _ in range(num):
        respondent_id = random.randint(1, respondents)
        ad_id = random.choice(ads)
        
        # Get the ad details from advertisement_info
        ad_details = advertisement_info[advertisement_info['AdID'] == ad_id].iloc[0]
        ad_cost = ad_details['AdCost']
        purchase_amount = ad_details['PurchaseAmount']
        
        # Determine the response type based on ad cost and purchase amount
        if ad_cost > 500 and purchase_amount < 500:
            response_type = random.choices(RESPONSE_TYPES, weights=[0.8, 0.2])[0]
        elif ad_cost < 500 and purchase_amount > 500:
            response_type = random.choices(RESPONSE_TYPES, weights=[0.3, 0.7])[0]
        else:
            response_type = random.choices(RESPONSE_TYPES, weights=[0.5, 0.5])[0]
        
        relevant = random.choice(RELEVANT)
        engagement_time = random.choices([random.randint(300, 600), random.randint(10, 299)], weights=[0.4, 0.6])[0]
        
        rating = random.choices(RATINGS, weights=[0.1, 0.1, 0.2, 0.3, 0.3] if engagement_time >= 300 else [0.4, 0.3, 0.2, 0.05, 0.05])[0]
        purchase_intent = "Yes" if response_type == "Clicked" and random.random() < 0.75 else "No"

        response = {
            "RespondentID": respondent_id,
            "AdID": ad_id,
            "Response_Date": random_date(datetime(2024, 1, 1), datetime(2024, 10, 31)),
            "ResponseType": response_type,
            "PurchaseIntent": purchase_intent,
            "Relevant": relevant,
            "Engagement_Time": engagement_time,
            "Rating": rating,
            "DeviceType": random.choice(DEVICE_TYPES)
        }
        data.append(response)
    
    return pd.DataFrame(data)


# Generate Ad_Demographic_link data
def generate_ad_demographic_link(ads=100, demographics=20):
    data = []
    for ad_id in range(1, ads + 1):
        num_links = random.randint(1, 3)
        demographic_ids = random.sample(range(1, demographics + 1), num_links)
        for demo_id in demographic_ids:
            link = {
                "AdID": ad_id,
                "DemographicID": demo_id
            }
            data.append(link)
    return pd.DataFrame(data)

# Generate Demographic_Data with mostly male/female genders
def generate_demographic_data(num=20):
    data = []
    for i in range(1, num + 1):
        gender = "Other" if random.random() < 0.05 else random.choice(["Male", "Female"])
        demographic = {
            "DemographicID": i,
            "AgeGroup": random.choice(AGE_GROUPS),
            "Gender": gender,
            "Location": random.choice(LOCATION_OPTIONS),
            "IncomeLevel": random.choice(INCOME_LEVELS),
            "Education": random.choice(EDUCATION_LEVELS),
            "Occupation": random.choice(OCCUPATIONS)
        }
        data.append(demographic)
    return pd.DataFrame(data)

# Generate Purchase_Info data with influence factor probabilities
def generate_purchase_info(responses_df, num=1000):
    clicked_responses = responses_df[responses_df["ResponseType"] == "Clicked"]
    data = []
    for _ in range(num):
        response = clicked_responses.sample(1).iloc[0]
        purchase_location = random.choice(PURCHASE_LOCATIONS)
        influence_factors = INFLUENCE_FACTORS_ONLINE if purchase_location == "Online" else INFLUENCE_FACTORS_INSTORE
        influence_factor = random.choices(influence_factors, weights=[0.35, 0.4, 0.15, 0.1])[0]
        
        purchase_info = {
            "RespondentID": response["RespondentID"],
            "AdID": response["AdID"],
            "InfluenceFactor": influence_factor,
            "PurchaseLocation": purchase_location,
            "AdInfluence": random.choice(AD_INFLUENCE)
        }
        data.append(purchase_info)
    return pd.DataFrame(data)

# Create dataframes
survey_respondents_df = generate_survey_respondents()
advertisement_info_df = generate_advertisement_info()
responses_to_ads_df = generate_responses_to_ads()
ad_demographic_link_df = generate_ad_demographic_link()
demographic_data_df = generate_demographic_data()
purchase_info_df = generate_purchase_info(responses_to_ads_df)

# Save to Excel
with pd.ExcelWriter("advertisement_response_data.xlsx") as writer:
    survey_respondents_df.to_excel(writer, sheet_name="Survey_Respondents", index=False)
    advertisement_info_df.to_excel(writer, sheet_name="Advertisement_Info", index=False)
    responses_to_ads_df.to_excel(writer, sheet_name="Responses_to_Ads", index=False)
    ad_demographic_link_df.to_excel(writer, sheet_name="Ad_Demographic_Link", index=False)
    demographic_data_df.to_excel(writer, sheet_name="Demographic_Data", index=False)
    purchase_info_df.to_excel(writer, sheet_name="Purchase_Info", index=False)

print("Data generation complete. File saved as advertisement_response_data.xlsx")
