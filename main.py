import os
import socket
from datetime import datetime
from subprocess import getstatusoutput
import boto3
from botocore.exceptions import ClientError


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')

if not (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_S3_BUCKET):
    raise Exception('set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and '
                    'AWS_S3_BUCKET environment vars')


def _get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    result = s.getsockname()[0]
    s.close()
    return result


AWS_S3_CLIENT = boto3.client('s3')
LOCAL_IP_ADDRESS = _get_ip()
HOSTNAME = os.uname().nodename


def get_metadata():
    result = {  # noqa
        'local_ip_address': LOCAL_IP_ADDRESS,
        'hostname': HOSTNAME,
        'date_day': datetime.utcnow().strftime('%Y%m%d'),
        'upload_timestamp': str(int(datetime.utcnow().timestamp() * 1000000)),
    }
    return result


def take_a_picture():
    filepath = f"/home/pi/camera_service/images/image_{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}.jpg"
    command = f"raspistill --mode 0 -o {filepath} --nopreview --exposure sports --timeout 1"
    error, output = getstatusoutput(command)

    if error:
        raise OSError(error, output)

    return filepath


def upload_aws(filepath):
    file_basename = os.path.basename(filepath)
    s3_path = f'{file_basename}'
    try:
        AWS_S3_CLIENT.upload_file(filepath, AWS_S3_BUCKET, s3_path,
            ExtraArgs={'Metadata': get_metadata()})  # noqa
    except ClientError as e:
        print(f'> error: {e}')
        return False

    print(f'> uploaded {s3_path}')

    return s3_path


def main():
    while True:
        filepath = take_a_picture()
        upload_aws(filepath)


if __name__ == '__main__':
    main()
