import openai

def exec_gpt3(text):
    openai.api_key = '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'
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text
