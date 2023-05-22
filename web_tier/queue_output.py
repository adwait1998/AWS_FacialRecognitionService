import boto3

sqs = boto3.resource('sqs', aws_access_key_id = 'AKIATTC5BJZ5W7LLBG6B', aws_secret_access_key = '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', region_name='us-east-1')
queue = sqs.get_queue_by_name(QueueName='output_queue')

def process_msg(message_body):
    print(message_body)
    pass

if __name__ == "__main__":
    while True:
        messages = queue.receive_messages()
        for message in messages:
            try:
                process_msg(message.body)
            except Exception as e:
                print("Empty Queue")
                continue

            message.delete()

