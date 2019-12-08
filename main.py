import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Getting the username parameter from ssm
def get_username(session):
    logger.info('Fetching UserName parameter from SSM parameter store')
    username = None
    try:
        ssm = session.client('ssm')
        parameter_value = ssm.get_parameter(Name='UserName')
        username = parameter_value['Parameter']['Value'] if 'Parameter' in parameter_value and 'Value' in parameter_value['Parameter'] else None
        logger.info('Fetching UserName parameter successful')
    except Exception as e:
        logger.error('Error in fetching parameter')
        raise e
    
    return username

#Writting parameter value to S3 bucket object
def put_username(session, username):
    
    #Getting BUCKET_NAME environment variable 
    try:
        bucket = os.environ['BUCKET_NAME']
        if bucket is None:
            raise Exception('BUCKET_NAME environment variable not available')
    except Exception as e:
        logger.error('BUCKET_NAME environment variable not available')
        raise e
    
    logger.info('Creating/Updating UserName.txt file to S3 bucket')
    try:
        s3 = session.client('s3')
        s3.put_object(Bucket=bucket, Body = str.encode(username), 
                      Key='UserName.txt', ServerSideEncryption = 'AES256')
        logger.info('Successfully created/updated UserName.txt file to S3 bucket')
    except Exception as e:
        logger.error('Error in S3 object creation/update')
        raise e

#Main handler function 
def lambda_handler(event, context):
    
    session = boto3.Session()
    
    try:
        username = get_username(session)
        if username is not None:
            put_username(session, username)
        else:
            logger.error('UserName parameter not available')
    except Exception as e:
        logger.error(str(e))
        return False
    
    return True
