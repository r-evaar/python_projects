from utils import get_api_data

Q_EP = "https://opentdb.com/api.php"
Q_PARAMS = {'amount': 20, 'type': 'boolean', 'category': 18}

question_data = get_api_data(endpoint=Q_EP, p=Q_PARAMS)['results']
question_data = question_data
