import json
import logging
import boto3
from botocore.exceptions import ClientError

# Initialize logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class BotError(Exception):
    """Custom exception for bot-related errors."""
    def __init__(self, message):
        self.message = message


def get_bedrock_client(region_name="us-east-1"):
    """Returns a Bedrock client."""
    return boto3.client(service_name="bedrock-runtime", region_name=region_name)


def get_inference_profile_arn(profile_name):
    """
    Retrieves the ARN of a specified inference profile from Parameter Store.
    Args:
        profile_name (str): Name of the profile (e.g., "TravelChatBot").
    Returns:
        str: The ARN of the inference profile.
    """
    ssm = boto3.client("ssm")
    parameter_name = f"/bedrock/inference-profiles/{profile_name}"
    response = ssm.get_parameter(Name=parameter_name)
    return response["Parameter"]["Value"]


def invoke_chat_model(client, model_id, user_message):
    """
    Invokes a chat model using the converse API and retrieves the response.
    Args:
        client: The Bedrock runtime client.
        model_id (str): The inference profile or model ID.
        user_message (str): The user's input message.
    Returns:
        str: The response from the model.
    """
    try:
        messages = [{"role": "user", "content": [{"text": user_message}]}]
        logger.info("Invoking chat model %s with message: %s", model_id, user_message)
        response = client.converse(modelId=model_id, messages=messages)
        return response["output"]["message"]["content"][0]["text"]
    except ClientError as e:
        raise BotError(f"Client error: {e.response['Error']['Message']}")


def test_travel_bot(travel_model_id):
    """Tests TravelBot with predefined examples."""
    client = get_bedrock_client()
    travel_examples = [
        "What are the best tourist attractions in Paris for a 3-day visit?",
        "Can you help me plan a budget-friendly trip to Japan for 10 days?",
        "What are the visa requirements for a U.S. citizen traveling to Vietnam?",
    ]

    print("\n--- Testing TravelBot ---")
    for example in travel_examples:
        try:
            response = invoke_chat_model(client, travel_model_id, example)
            print(f"User: {example}\nBot: {response}\n")
        except BotError as e:
            logger.error("Error testing TravelBot: %s", e.message)
            print(f"Error: {e.message}")


def test_insurance_bot(insurance_model_id):
    """Tests InsuranceBot with predefined examples."""
    client = get_bedrock_client()
    insurance_examples = [
        "What is the difference between term life insurance and whole life insurance?",
        "How does car insurance work if I get into an accident?",
        "Can you explain what a deductible is in health insurance?",
    ]

    print("\n--- Testing InsuranceBot ---")
    for example in insurance_examples:
        try:
            response = invoke_chat_model(client, insurance_model_id, example)
            print(f"User: {example}\nBot: {response}\n")
        except BotError as e:
            logger.error("Error testing InsuranceBot: %s", e.message)
            print(f"Error: {e.message}")


def main():
    """Main function to test both bots."""
    travel_model_id = get_inference_profile_arn("TravelChatBotNOVA")
    insurance_model_id = get_inference_profile_arn("InsuranceChatBotNOVA")
    test_travel_bot(travel_model_id)
    test_insurance_bot(insurance_model_id)


if __name__ == "__main__":
    main()
