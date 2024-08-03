# Blitz Serverless

Migrating flask Spotify application to AWS.

## Pipeline creation

Go here to get CloudFormation template to set up CodePipeline: https://github.com/Thudles/codepipeline_template, cannot be here. Strctly for code that will get deployed.

```shell
aws cloudformation create-stack \
    --stack-name cf-deploy-pipeline \
    --template-body file://pipeline_template.yaml \
    --capabilities CAPABILITY_NAMED_IAM
```

## Application deployment

Deployment will be managed by the pipeline at each push
