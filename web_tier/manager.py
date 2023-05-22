import math
from utils import EC2, SQS
import time


def auto_scale():
    queue_length = SQS.get_queue_length()

    if queue_length == 0:
        if EC2.get_running_count() == 0:
            print('No app-tier instances running. Down-scaling not needed !')
            return
        print('Scaling down and Shutting down all instances')
        EC2.stop_all_instances()
        return
    
    count_running = EC2.get_running_count()
    scale_parameters = math.ceil((queue_length / 5))
    
    if scale_parameters > count_running:
        print('UPSCALING!!!')
        upscale(min(scale_parameters - count_running, 10 - count_running))



def upscale(count):
    if count == 0:
        return
    print('Adding more instances.')
    EC2.start_instances(count)

if __name__ == '__main__':

    while(True):
        print('Checking for auto-scaling')
        auto_scale()
        time.sleep(30)
