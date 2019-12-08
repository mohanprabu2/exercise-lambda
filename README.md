# Copy SSM parameter to S3 bucket using Lambda and Lambda deployment using CloudFormation

## 1. Pre-requisites

 #### 1.1 Create S3 bucket
 ```
 $ aws s3api create-bucket --bucket mohan-exercise-lambda --profile mohan
 ```
 #### 1.2 Create SSM parameter
 ```
 $ aws ssm put-parameter --name UserName --value JohnDoe --type String --profile mohan
 ```

## 2 . Steps to test this project:

 #### 2.1 Clone this repository locally
 
 ```
 $ git clone https://github.com/mohanprabu2/exercise-lambda.git
 ```
 
 #### 2.2 Create a zip file incuding main.py file
 
 ```
 $ zip code.zip main.py
 ```
 
 #### 2.3 Upload code.zip and cft.yml files to S3 bucket
 
 ```
 $ aws s3 cp code.zip s3://mohan-exercise-lambda/ --sse --profile mohan
 $ aws s3 cp cft.yml s3://mohan-exercise-lambda/ --sse --profile mohan
 ```
 #### 2.4 Create a CF stack using cft.yml file
 
 Create a stack from cft.yml file with the parameters(bucket name and code.zip file path as key). It will create require resources and give output as resource ARN's.
 
 ```
 CFT S3 URL: https://mohan-exercise-lambda.s3.amazonaws.com/cft.yml
 
 Stack name: exercise-lambda-stack
 Parameters:
  Bucket: mohan-exercise-lambda
  Key: code.zip
  
 Output:
  LambdaFunction:- arn:aws:lambda:us-east-1:1234567890:function:exercise-lambda-stack-LambdaFunction-1AW094W25LNGD		-
  LambdaFunctionRole:- arn:aws:iam::1234567890:role/exercise-lambda-stack-LambdaExecutionRole-6XTS6X0UG7AM
  ```
 #### 2.5 Verify resource creation
 
 Login to console and verify the lambda function and lambda role resources.
 
 #### 2.6 Trigger the lambda function
 
 Use following command to trigger the lambda function
 
 ```
 $ aws lambda invoke --function-name exercise-lambda-stack-LambdaFunction-1AW094W25LNGD outfile.txt --profile mohan
{
    "StatusCode": 200,
    "ExecutedVersion": "$LATEST"
}
 ```
 #### 2.7 Verify UserName.txt file created in S3 bucket
 ```
 $ aws s3 cp s3://mohan-exercise-lambda/UserName.txt . --profile mohan
 download: s3://mohan-exercise-lambda/UserName.txt to .\UserName.txt
 
 $ cat UserName.txt
 JohnDoe
 ```
 
 **Note:**
 - I have used my S3 bucket name (ex: mohan-exercise-lambda), please create your bucket using unique name and replace bucket name.
 - Please replace your AWS profile name in CLI commands
