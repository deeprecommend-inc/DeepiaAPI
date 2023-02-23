import openai

def exec_gpt3(text):
    openai.api_key = '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'
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=1200,
        temperature=0.7,
        frequency_penalty=1.0,
    )
    return response['choices'][0]['text']
