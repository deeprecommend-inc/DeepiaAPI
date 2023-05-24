import openai

def exec_gpt(prompt):
    openai.api_key = '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'
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text
