# Let's upload a text file on AWS
import io

import boto3
import botocore.client
from boto3.resources.base import ServiceResource

BUCKET_NAME = 'abhay.s3.documents.test1'

# First we need to create a session with boto3
session1 = boto3.Session(aws_access_key_id="my_aws_key", aws_secret_access_key="my_aws_secret_key")


# Now I could hard code the secret and the access key id in the code itself, but what kind of programmer do you take
# me for? Huh? Any child 1-year-old could tell you we need to externalize such things ;) So we have to store this
# into a properties file. So let's create a properties file 'aws_keys.properties' and then add the access key and
# secret in there. But how do I read the properties file?

# Enter - jproperties - a module that allows us easy reading from properties files. You need to install the
# jproperties module first using the command: pip install jproperties

def read_aws_keys() -> tuple[str, str]:
    from jproperties import Properties

    # The Properties object is very similar to a Dictionary Object.
    aws_config = Properties()

    # We read the properties file into the aws_config properties Object
    with open('aws_keys.properties', 'rb') as config_file:
        aws_config.load(config_file)

    # and now reading those properties is peanuts. However, know that - the value part is stored in a named tuple of
    # data and metadata. This Object is called PropertyTuple. We will look into metadata later on.
    access_key_id = aws_config.get("aws.access.key.id").data  # we extract only the data part of it
    access_key_secret = aws_config.get("aws.access.key.secret").data

    # if you forget the '.data' you will get the following error:
    # TypeError: sequence item 0: expected str instance, PropertyTuple found

    return access_key_id, access_key_secret


def file_exists(s3_file_name) -> bool:
    s3r = initialize_s3_resource()

    # What we are doing here is a "HEAD" request for a single "key" i.e. our filename. This request is very FAST even
    # if our file is very large. The other way is to do a "get" directly as we might want to use the file
    try:
        s3r.Object(BUCKET_NAME, s3_file_name).load()
        return True
    except botocore.client.ClientError as e:
        return False if e.response['Error']['Code'] == '404' else True


def upload_data(user_data: bytes, s3_file_name: str, overwrite: bool = False):
    s3r = initialize_s3_resource()

    # first we check if the data we are attempting to store exists on S3.
    exists = file_exists(s3_file_name)
    print(f'File exists: {exists}')

    if not exists or (exists and overwrite):
        # We then create an S3 Object into our bucket which points to a file called hello_s3.txt
        s3_object = s3r.Object(BUCKET_NAME, s3_file_name)
        # and we then put the data into the S3 object.
        result = s3_object.put(Body=user_data)

        response = result.get('ResponseMetadata')
        if response.get('HTTPStatusCode') == 200:
            print('Data uploaded Successfully')
        else:
            print('Data Not Uploaded')
    else:
        print(f'The file {s3_file_name} exists already on S3')


def upload_file(f: io.TextIOWrapper, s3_file_name: str) -> None:
    pass


def initialize_s3_resource() -> ServiceResource:
    access_key_id, access_key_secret = read_aws_keys()
    # Now lets properly create the boto3 session object:
    session = boto3.Session(aws_access_key_id=access_key_id, aws_secret_access_key=access_key_secret)
    # Create a resource from the session
    s3r = session.resource('s3')
    return s3r


def upload_my_file(file: str, s3_file_name: str, overwrite: bool = False) -> None:
    s3r = initialize_s3_resource()
    exists = file_exists(s3_file_name)
    print (f"{s3_file_name} exists: {exists}")

    if not exists or (exists and overwrite):
        result = s3r.Bucket(BUCKET_NAME).upload_file(file, s3_file_name)
        print (f"File {s3_file_name} uploaded successfully on S3")
    else:
        print(f'The file {s3_file_name} already exists. Not uploading again.')


if __name__ == '__main__':
    # the data could come from anywhere. For simplicity, lets hard code.
    data = b"Hello S3!!"
    upload_data(data, 'hello_s3.txt', overwrite=True)
    # here is another way if you want to upload contents coming from a file. You open a stream of data with "open"
    # API call and that will pass on the bytes to S3
    upload_data(open('quotes.txt', 'rb'), "quotes-data.txt")

    # OUTPUT:
    # File exists: True
    # Data uploaded Successfully
    # File exists: True
    # The file quotes-data.txt exists already on S3

    # Great! What if you had a file that you wanted to upload? I have here a set of beautiful quotes that I want to
    # upload. So here goes:
    upload_my_file('quotes.txt', "quotes-file.txt", overwrite=True)

    # OUTPUT:
    # quotes-file.txt exists: False
    # File quotes-file.txt uploaded successfully on S3

# Bear in mind that the same operations can be performed using a boto3 client as well. So what's the difference
# between a resource and a client? Well... Resources are higher-level abstractions of AWS services compared to
# clients. Resources are the recommended pattern to use boto3 as you don’t have to worry about a lot of the
# underlying details when interacting with AWS services. As a result, code written with Resources tends to be simpler.
#
# However, Resources aren’t available for all AWS services. In such cases, there is no other choice but to use a
# Client instead.