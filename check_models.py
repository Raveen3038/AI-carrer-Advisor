import google.generativeai as genai

genai.configure(api_key="AIzaSyC2fNUqnSgqqosP9ZtwhGZv9LPONVy-sjc")

# List available models
models = genai.list_models()
for model in models:
    print(model.name)
