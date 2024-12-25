# Bedrock-Cost-Allocation-Tags

### This repository demonstrates how to use cost allocation tags in Amazon Bedrock. It includes a demo app that shows this in practice. If you found this repo useful, please :star:  it. Thx.

## The what
Amazon Bedrock recently introduced cross-region inference, enabling automatic routing of inference requests across AWS Regions. This feature uses system-defined inference profiles (predefined by Amazon Bedrock), which configure different model Amazon Resource Names (ARNs) from various Regions and unify them under a single model identifier (both model ID and ARN). While this enhances flexibility in model usage, it doesn’t support attaching custom tags for tracking, managing, and controlling costs across workloads and tenants.

To bridge this gap, Amazon Bedrock now introduces application inference profiles, a new capability that allows organizations to apply custom cost allocation tags to track, manage, and control their Amazon Bedrock on-demand model costs and usage. This capability enables organizations to create custom inference profiles for Bedrock base foundation models, adding metadata specific to tenants, thereby streamlining resource allocation and cost monitoring across varied AI applications.

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

This setup was tested on us-east-1. If you use the AWS Cloudshell you can skip the this part and go striaght to the Depolyment step.

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

1. clone the repo
```bash
git clone https://github.com/adija1/Bedrock-Cost-Allocation-Tags
```
2. Change dir
```bash
cd Bedrock-Cost-Allocation-Tags/
```

3. The following will create two Application Inference Profiles - TravelChatBot using Claude Sonnet 3.5 & InsuranceChatBot using Amazon Titan-text-lite-v1
```bash
aws cloudformation deploy --template-file bedrock-inference-profiles.yaml --stack-name BedrockChatBots
```

4. The following will create two Application Inference Profiles - TravelChatBotNova & InsuranceChatBotNova both using Amazon Nova Pro models.
```bash
aws cloudformation deploy --template-file bedrock-inference-profiles-nova.yaml --stack-name BedrockChatBotsNova
```

### Additional AWS Commands

To list the Inference profiles created using the first CF Stack (Claude & Titan)
```bash
aws bedrock list-inference-profiles --type-equals APPLICATION --query 'inferenceProfileSummaries[?inferenceProfileName==`BedrockChatBots-TravelChatBot`]'
```
or
```bash
aws bedrock list-inference-profiles --type-equals APPLICATION --query 'inferenceProfileSummaries[?inferenceProfileName==`BedrockChatBots-InsuranceChatBot`]'
```

To list the Inference profiles created using the second CF Stack (Nova)
```bash
aws bedrock list-inference-profiles --type-equals APPLICATION --query 'inferenceProfileSummaries[?inferenceProfileName==`BedrockChatBotsNOVA-InsuranceChatBot`]'
```
or
```bash
aws bedrock list-inference-profiles --type-equals APPLICATION --query 'inferenceProfileSummaries[?inferenceProfileName==`BedrockChatBotsNOVA-TravelChatBot`]'
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

### Cleanup
To delete the CloudFormation stack, use:

```bash
aws cloudformation delete-stack --stack-name BedrockChatBots
```

```bash
aws cloudformation delete-stack --stack-name BedrockChatBotsNova
```


### Documentation

A very well written [blog](https://aws.amazon.com/blogs/machine-learning/track-allocate-and-manage-your-generative-ai-cost-and-usage-with-amazon-bedrock/) about the feature.

Amazon Bedrock [documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles.html) on Inference Profile.

Creating [Application Inference Profile](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-create.html)

### For vieweing the results in Cost Explorer
1. After Application Inference Profiles are created it takes roughly 48 hours for the tags to appear in [Cost Allocation Tags](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html)
2. Once these tags appear in CAT they need to be activated. Once activated it takes roughly 48 hours to appear in Cost explorer.

![image](https://github.com/user-attachments/assets/a8971558-e805-4a8d-b7c2-b80e9242ee0b)

