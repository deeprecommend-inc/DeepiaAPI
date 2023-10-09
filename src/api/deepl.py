import requests
from const.is_japanese import is_japanese

def exec_deepl(text):
    url = 'https://api-free.deepl.com/v2/translate'
    api_key = '505f71dd-aa18-c5d4-828d-2c2157e8a36d:fx'
    
    params = {
        'auth_key': api_key,
        'text': text,
        'source_lang': 'JA',
        'target_lang': 'EN'
    }

    if is_japanese(text):
        try:
            response = requests.post(url, data=params)
            data = response.json()
            translations = data.get('translations', [])
            translated_text = translations[0].get('text', '') if translations else ''
            return translated_text
        except requests.exceptions.RequestException as e:
            print('Error:', e)
            return text
    else:
        return text
