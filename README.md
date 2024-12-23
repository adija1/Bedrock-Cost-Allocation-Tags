# Bedrock-Cost-Allocation-Tags

## The what
Amazon Bedrock recently released the ability to create Application Inference Profiles and to tag them.

## The Why
By tagging Application Inference profiles it is easier to track and monitor costs & usage of specific workloads in Bedrock

## The How

### Prerequisites

1. Ensure you have Python 3.10 installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).
2. Install AWS CLI [AWS CLI installation guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
3. Configure AWS Credentials
After installing the AWS CLI, configure your AWS credentials by running the following command and following the prompts:

```bash
aws configure
```
4. Ensure you have `pip` installed, then install the required Python packages by running:

```bash
pip install boto3
```
### Deployment

The following will create two Application Inference Profiles - TravelChatBot using Claude Sonnet 3.5 & InsuranceChatBot using Amazon Titan-text-lite-v1
```bash
aws cloudformation deploy --template-file bedrock-inference-profiles.yaml --stack-name BedrockChatBots
```

The following will create two Application Inference Profiles - TravelChatBotNova & InsuranceChatBotNova both using Amazon Nova Pro models.
```bash
aws cloudformation deploy --template-file bedrock-inference-profiles-nova.yaml --stack-name BedrockChatBotsNova
```

### Additional AWS Commands

To retrieve resources tagged with a specific key and value, use:
```bash
aws resourcegroupstaggingapi get-resources --tag-filters Key=Application,Values=InsuranceChatBot
```
or
```bash
aws resourcegroupstaggingapi get-resources --tag-filters Key=Application,Values=InsuranceChatBotNova
```

### Usage
For testing the Sonnet & Titan:

```bash
python converse_bot.py
```
For testing the Nova:

```bash
python converse_bot_NOVA.py 
```
