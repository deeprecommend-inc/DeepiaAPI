import requests

def exec_deepl(text):
    url = 'https://api-free.deepl.com/v2/translate'
    api_key = 'Your_DeepL_API_Key'
    
    params = {
        'auth_key': api_key,
        'text': text,
        'source_lang': 'JA',
        'target_lang': 'EN'
    }
    
    try:
        response = requests.post(url, data=params)
        data = response.json()
        translations = data.get('translations', [])
        translated_text = translations[0].get('text', '') if translations else ''
        return translated_text
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return ''
