from openai import OpenAI
client = OpenAI(
    api_key='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'
)

response = client.chat.completions.create(
  model="babbage-002",
  messages=[
    {"role": "user", "content": "What is a good book to read?"},
  ]
)

print(response.choices[0].message.content)

# api_key = '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'

