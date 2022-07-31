from boto3 import client, resource
from botocore.exceptions import ClientError
from util.functions.imagefunctions import get_env


def get_resource():
    """make a connection to s3 resource"""
    return resource(
        's3',
        'us-west-2',
        aws_access_key_id=get_env('AWS_ID'),
        aws_secret_access_key=get_env('AWS_KEY')
    )


def get_object(key):
    """make a connection with s3 object"""
    s3 = get_resource()
    return s3.Object(
        get_env('S3_BUCKET'),
        key
    )


def get_client():
    """make client connection to the s3 account"""
    return client(
        's3',
        'us-west-2',
        aws_access_key_id=get_env('AWS_ID'),
        aws_secret_access_key=get_env('AWS_KEY')
    )


def get_file(path):
    """get binary file object from s3 in the filetype it was stored in"""
    obj=get_object(path)
    res = obj.get()
    return res['Body']


def get_file_url(path):
    """get a presigned url from s3 to the object"""
    try:
        s3_client = get_client()
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': get_env('S3_BUCKET'),
                'Key': path
            },
            ExpiresIn=3600,
        )
        return url
    except:
        return ''


def upload_file(path, file):
    """Inserts a file to the given path within the s3 bucket"""
    s3_client = get_client()
    try:
        s3_client.upload_fileobj(file, get_env('S3_BUCKET'), path)
    except ClientError as client_error:
        raise ClientError from client_error
    return True


def delete_file(path):
    """deletes file from s3 bucket"""
    try:
        obj=get_object(path)
        obj.delete()
    except FileNotFoundError as file_404:
        raise FileNotFoundError from file_404


def delete_directory(dir):
    """delete directory from s3 bucket"""
    res = get_resource()
    bucket = res.Bucket(get_env('S3_BUCKET'))
    response = bucket.objects.filter(Prefix=dir).delete()
    for resp in response:
        if resp.get('ResponseMetadata').get('HTTPStatusCode') != 200:
            raise TypeError


def create_or_update_file(instance, file, file_path):
    """
    Handles the creation and update of an Image model instance
    """
    from display.serializers import ImageAllSerializer
     # create photo
    if instance is None and file:
        profile_photo_serializer = ImageAllSerializer(data={'file_path': file_path}, context=file)
        profile_photo_serializer.is_valid(raise_exception=ValueError)
        created_photo = profile_photo_serializer.save()
        instance = created_photo
    # update photo
    elif instance:
        instance.update_s3_repo(file, file_path)

    return instance
