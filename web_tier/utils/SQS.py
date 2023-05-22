import boto3
import time

def get_queue_length():
    session = boto3.session.Session()
    sqs_resource = session.resource('sqs', aws_access_key_id = 'AKIATTC5BJZ5W7LLBG6B', aws_secret_access_key = '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', region_name='us-east-1')
    sqs_queue = sqs_resource.get_queue_by_name(QueueName='input_queue')
    return int(sqs_queue.attributes.get('ApproximateNumberOfMessages'))

def get_output_queue_length():
    session = boto3.session.Session()
    sqs_resource = session.resource('sqs', aws_access_key_id = 'AKIATTC5BJZ5W7LLBG6B', aws_secret_access_key = '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', region_name='us-east-1')
    sqs_queue = sqs_resource.get_queue_by_name(QueueName='output_queue')
    return int(sqs_queue.attributes.get('ApproximateNumberOfMessages'))

def enqueue(msg):
    session = boto3.session.Session()
    sqs_resource = session.resource('sqs', aws_access_key_id = 'AKIATTC5BJZ5W7LLBG6B', aws_secret_access_key = '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', region_name='us-east-1')
    sqs_queue = sqs_resource.get_queue_by_name(QueueName='input_queue')
    response = sqs_queue.send_message(MessageBody=msg)
    return response.get('MessageId')

def dequeue():
    if get_queue_length() == 0:
        return
    session = boto3.session.Session()
    sqs_resource = session.resource('sqs', aws_access_key_id = 'AKIATTC5BJZ5W7LLBG6B', aws_secret_access_key = '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', region_name='us-east-1')
    sqs_queue = sqs_resource.get_queue_by_name(QueueName='input_queue')
    for msg in sqs_queue.receive_messages():
        out = msg.body
        msg.delete()
        return out
    return ""

def get_result_to_send(filename):
    print('Fetching results for' + str(filename))
    sqs_resource = boto3.resource('sqs',aws_access_key_id = 'AKIATTC5BJZ5W7LLBG6B', aws_secret_access_key = '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', region_name='us-east-1')
    sqs_queue = sqs_resource.get_queue_by_name(QueueName = 'output_queue')
    while(True):
        print('Queue')
        for m in sqs_queue.receive_messages():
            print(m.body)

        time.sleep(2)
        if get_output_queue_length() == 0:
            continue
        for msg in sqs_queue.receive_messages(MaxNumberOfMessages=1):
            out = msg.body
            if(out.split(' ')[0] == filename):
                msg.delete()
                return out

def get_messages():
    result = {}
    session = boto3.session.Session()
    sqs_resource = session.resource('sqs', aws_access_key_id = 'AKIATTC5BJZ5W7LLBG6B', aws_secret_access_key = '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', region_name='us-east-1')
    sqs_queue = sqs_resource.get_queue_by_name(QueueName='output_queue')
    for msg in sqs_queue.receive_messages(MaxNumberOfMessages=2):
        out = msg.body
        result[out.split(' ')[0]] = out
        msg.delete()

    return result
