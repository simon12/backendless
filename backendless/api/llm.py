import openai

def call_llm(api_key, model, prompt, max_tokens):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
    )
    return response.choices[0].text.strip()
