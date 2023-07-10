import openai

def exec_gpt4(prompt):
    openai.api_key = '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'
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()