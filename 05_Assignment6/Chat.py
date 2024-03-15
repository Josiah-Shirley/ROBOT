
from openai import OpenAI
client = OpenAI(
    api_key=''
)

baseString = "For the following prompt: "
tokenLimitingString = "please respond in a maximum of ten words; "
personalityString = "please respond how Joe Rogan would respond; "

# Change the value of this variable for the prompt given
prompt = "tell me a joke"

toDeliver = baseString + tokenLimitingString + personalityString + prompt

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": toDeliver},
  ]
)

print(response.choices[0].message.content)


