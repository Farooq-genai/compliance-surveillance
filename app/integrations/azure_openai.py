from openai import AzureOpenAI
from app.core.config import settings
from app.core.logger import logger


class AzureOpenAIClient:

    logger.info("AzureOpenAIClient called")
    def __init__(self):
        self.client=AzureOpenAI(
            api_key=settings.azure_openai_api_key,
            api_version=settings.azure_openai_api_version,
            azure_endpoint=settings.azure_openai_endpoint
        )

    def test_connection(self):
        logger.info("AzureOpenAIClient :: test_connection called")
        response = self.client.chat.completions.create(
            model=settings.azure_openai_deployment_name,
            messages=[
                {
                    "role": "system",
                    "content": "you are a helpful assistance"
                },
                {
                    "role": "user",
                    "content": "Reply with only: Azure OpenAI connection successful."
                }
            ],
            temperature = 0
        )

        return response.choices[0].message.content