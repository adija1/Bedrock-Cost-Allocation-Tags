# Bedrock-Cost-Allocation-Tags

## The what
Amazon Bedrock supports the creation and tagging of Application Inference Profiles, enabling better cost management for your AI workloads.
Inference profile is a set of configuration settings that control how a foundation model is used 

## The Why
By tagging Application Inference profiles it is easier to track and monitor costs & usage of specific workloads in Bedrock

## The How
This project contains the following files for ease of deployment of several application inference profiles and chatbots for testing the profiles.
*bedrock-inference-profiles.yaml* - cloudformation stack for creating two Application Inference Profiles:
1. Travel Application Inference profile using Claude Sonnet 3.5, tagged with Key: Application, Value: TravelChatBot, Key: CostCenter, Value: Travel
2. Insurance Application Inference Profile using Amazon Titan Lite V1, tagged with Key: Application, Value: InsuranceChatBot, Key: CostCenter, Value: Insurance 

*bedrock-inference-profiles-nova.yaml* - cloudformation stack for creating Travel & Insurance Application Inference Profile using Nova Pro model.
1. Travel Application Inference profile using Amazon Nova Pro, tagged with Key: Application, Value: TravelChatBotNOVA, Key: CostCenter, Value: Travel
2. Insurance Application Inference Profile using Amazon Nova pro, tagged with Key: Application, Value: InsuranceChatBotNOVA, Key: CostCenter, Value: Insurance
   
*converse_bot.py* - chat app that will send prompts to the Sonnet & Titan Application Inference Profiles.
*converse_bot_NOVA.py* - chat app that will send prompts to the Nova Application Inference Profiles.

### Prerequisites

This setup was tested on us-east-1 

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
For testing the Sonnet & Titan Application Inference Profiles:

```bash
python converse_bot.py
```
For testing the Nova Application Inference Profiles:

```bash
python converse_bot_NOVA.py 
```

## Cleanup
To delete the CloudFormation stack, use:

```bash
aws cloudformation delete-stack --stack-name BedrockChatBots
```

```bash
aws cloudformation delete-stack --stack-name BedrockChatBotsNova
```


## Documentation

A very well written [blog](https://aws.amazon.com/blogs/machine-learning/track-allocate-and-manage-your-generative-ai-cost-and-usage-with-amazon-bedrock/) about the feature.

Amazon Bedrock [documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles.html) on Inference Profile.

Creating [Application Inference Profile](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-create.html)

## For vieweing the results in Cost Explorer
1. After Application Inference Profiles are created it takes roughly 48 hours for the tags to appear in [Cost Allocation Tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html)
2. Once these tags appear in CAT they need to be activated. Once activated it takes roughly 48 hours to appear in Cost explorer.
