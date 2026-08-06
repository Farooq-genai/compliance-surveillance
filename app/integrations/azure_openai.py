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

    def chat(self, prompt: str) -> str:
        """
        Send a prompt to Azure OpenAI and return the response text.
        """

        logger.info("Sending prompt to Azure OpenAI")

        response = self.client.chat.completions.create(
            model=settings.azure_openai_deployment_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are an Enterprise Compliance Surveillance AI."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        return response.choices[0].message.content