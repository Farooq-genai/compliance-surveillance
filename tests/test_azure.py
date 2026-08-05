from app.integrations.azure_openai import AzureOpenAIClient


client = AzureOpenAIClient()

print(client.test_connection())