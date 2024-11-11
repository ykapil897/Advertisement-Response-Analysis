from django.conf import settings

def fetch_data_from_mongo():
    collection = settings.MONGO_DB["survey_respondents"]
    data = list(collection.find({}, {"_id": 0}))  # Exclude the MongoDB ID from the results
    return data