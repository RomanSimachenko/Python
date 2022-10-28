import os
import openai
import time
import json

openai.organization = os.getenv("OPENAI_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")

# openai_models = openai.Model.list()
#
# models_ids = [m['id'] for m in openai_models['data'] if m['id'].startswith("text-")]
#
# completions = []
# for id in models_ids:
#     try:
#         c = openai.Completion.create(
#             model=id,
#             prompt="Hello! How's it going?",
#             max_tokens=256,
#             temperature=0,
#             best_of=3
#         )
#     except Exception as error:
#         print(error)
#         with open("completions.json", 'w', encoding='utf-8') as file_obj:
#             file_obj.write(json.dumps(completions, indent=4, ensure_ascii=False))
#         print(id)
#         break
#     completions.append(c)
#     time.sleep(1)
#     # break

# with open("completions.json", 'w', encoding='utf-8') as file_obj:
#     file_obj.write(json.dumps(completions, indent=4, ensure_ascii=False))

# model_2 = openai.Completion.create(
#     model="text-curie-001",
#     prompt="How are you?",
#     max_tokens=512,
#     temperature=0,
#     best_of=5
# )

# model_4 = openai.Completion.create(
#     model="text-babbage-001",
#     prompt="How are you?",
#     max_tokens=512,
#     temperature=0,
#     best_of=5
# )

while True:
    message = input().strip()
    compl = openai.Completion.create(
        model="text-davinci-002",
        prompt=message,
        max_tokens=512,
        temperature=0,
        best_of=5,
        n=3
    )
    print('\n'.join([item['text'].strip() for item in compl["choices"]]))
    print()