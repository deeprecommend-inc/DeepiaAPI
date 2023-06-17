# https://dev.classmethod.jp/articles/openai-api-gpt-update-ver-0613/
import openai

def exec_gpt(prompt):
    openai.api_key = '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'
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()
