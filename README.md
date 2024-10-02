# Lambda AWS API

Welcome to this machine learning project, where AWS Lambda and API Gateway are used to create and expose serverless functions via a cloud infrastructure. This project allows you to deploy, manage, and update Lambda functions through API Gateway, enabling easy and scalable API development.

## Project Overview

This project provides a Python script that performs the following tasks:
- **Create a new Lambda function**: Deploy a Lambda function from a ZIP file containing the function code.
- **Create a new API Gateway**: Set up an API Gateway to expose the Lambda function as an API endpoint.
- **Update existing resources**: If needed, it can delete and replace existing Lambda functions or API Gateways.

### Key Components:
1. **Lambda Functions**: Functions deployed to AWS Lambda using a ZIP file.
2. **API Gateway**: Exposes Lambda functions as APIs with defined routes.
3. **AWS Boto3**: The AWS SDK for Python used to interact with AWS Lambda and API Gateway.

## Deployment Instructions

### 1. Zipping Lambda Functions

If you have made any changes to your Lambda function locally, zip the file before deploying:

```bash
zip data/my_lambda.zip my_lambda.py
```

### 2. Deploying the Lambda Function and API Gateway

To create and deploy a new Lambda function and API Gateway, run the following command:

```bash
python3 src/main.py <path_to_zip_file> <handler_function>
```

For example:

```bash
python3 src/main.py data/my_lambda.zip word_count
```

### 3. Updating Existing Resources

If the Lambda function or API Gateway already exists and you need to update them, add the `update` argument:

```bash
python3 src/main.py <path_to_zip_file> <handler_function> update
```

This command will delete the existing resources and redeploy them with the updated configuration.

### 4. Testing the Deployment

Once the Lambda function and API Gateway are deployed, you can verify that everything is working by running:

```bash
python3 tests/test.py
```

You can enable verbose mode for more detailed output:

```bash
python3 tests/test.py -v
```

## References

- [AWS Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
