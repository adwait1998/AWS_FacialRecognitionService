import boto3

def upload_file(file, filename):
    session = boto3.session.Session()
    s3_resource = session.resource('s3', aws_access_key_id = 'AKIATTC5BJZ5W7LLBG6B', aws_secret_access_key = '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', region_name='us-east-1')
    bucket = s3_resource.Bucket('inputbucket117')
    try:
        bucket.upload_fileobj(file, filename)
    except:
        print('Error occured while uploading')

def download_file(filename):
    session = boto3.session.Session()
    s3_resource = boto3.resource('s3', aws_access_key_id = 'AKIATTC5BJZ5W7LLBG6B', aws_secret_access_key = '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', region_name='us-east-1')
    bucket = s3_resource.Bucket('outputbucket117')
    try:
        with open(filename, 'wb') as f:
            bucket.download_fileobj(filename, f)
    except:
        print('Error while downloading')
