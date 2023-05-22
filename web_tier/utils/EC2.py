import boto3

def get_running_count():
    ec2 = boto3.resource('ec2', aws_access_key_id = 'AKIATTC5BJZ5W7LLBG6B', aws_secret_access_key = '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', region_name='us-east-1')
    return len([instance for instance in ec2.instances.all() if instance.state['Name'] == 'running' or instance.state['Name'] == 'pending'])-1

def get_instances():
    instIDs = []
    ec2 = boto3.resource('ec2', aws_access_key_id = 'AKIATTC5BJZ5W7LLBG6B', aws_secret_access_key = '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', region_name='us-east-1')
    for instance in ec2.instances.all():
        instIDs.append(instance.id)
    return instIDs

def get_instance_state(instID):
    ec2 = boto3.resource('ec2', aws_access_key_id = 'AKIATTC5BJZ5W7LLBG6B', aws_secret_access_key = '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', region_name='us-east-1')
    inst = ec2.Instance(instID)
    return inst.state

def start_instances(cnt):
    instIDs = get_instances()
    client = boto3.client('ec2', aws_access_key_id = 'AKIATTC5BJZ5W7LLBG6B', aws_secret_access_key = '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', region_name='us-east-1')
    for instance in instIDs:
        if get_instance_state(instance)['Name'] == 'stopped':
            cnt -= 1
            run = []
            run.append(instance)
            print('Instance started with id : ' + instance)
            client.start_instances(InstanceIds=run)
            if cnt == 0:
                return

def stop_all_instances():
    if get_running_count() == 0:
        print('No app-tier instances running')
        return
    instanceIDs = get_instances()
    client = boto3.client('ec2', aws_access_key_id = 'AKIATTC5BJZ5W7LLBG6B', aws_secret_access_key = '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', region_name='us-east-1')
    for inst in instanceIDs:
        if get_instance_state(inst)['Name'] == 'running':
            if(inst == 'i-0c4ae20c2a9cdbace'):
                print('Web Tier')
                continue
            stop = []
            stop.append(inst)
            print('Instance stopped with id : ' + inst)
            client.stop_instances(InstanceIds=stop)
