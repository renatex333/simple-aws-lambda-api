# lambda-aws-api

Welcome to this ML project, in which AWS Lambda and API Gateway are used to provide functions as API's on a cloud infrastructure!

If any changes are made to the lambda functions locally, they must be zipped:

```bash
zip data/my_lambda.zip my_lambda.py
```

When deploying the function, run:

```bash
python3 src/main.py
```

or if the API and Function already exists, update the existing instances with:

```bash
python3 src/main.py update
```

To test and ensure everything is working as intended, run:

```bash
python3 tests/test.py
```

# References

[Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)