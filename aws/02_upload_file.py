# Let's upload a text file on AWS
import io

import boto3
from boto3.resources.base import ServiceResource

ACCESS_KEY_ID = ''  # Read further
ACCESS_KEY_SECRET = ''  # Read further

# First we need to create a session with boto3
session1 = boto3.Session(aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_KEY_SECRET)


# Now I could hard code the secret and the access key id in the code itself, but what kind of programmer do you take
# me for? Huh? Any child 1-year-old could tell you we need to externalize such things ;) So we have to store this
# into a properties file. So let's create a properties file 'aws_keys.properties' and then add the access key and
# secret in there. But how do I read the properties file?

# Enter - jproperties - a module that allows us easy reading from properties files. You need to install the
# jproperties module first using the command: pip install jproperties

def read_aws_keys() -> tuple[str, str]:
    global ACCESS_KEY_ID, ACCESS_KEY_SECRET
    from jproperties import Properties
    # The Properties object is very similar to a Dictionary Object.
    aws_config = Properties()
    # We read the properties file into the aws_config properties Object
    with open('aws_keys.properties', 'rb') as config_file:
        aws_config.load(config_file)
    # and now reading those properties is peanuts. However, know that - the value part is stored in a named tuple of
    # data and metadata. This Object is called PropertyTuple. We will look into metadata later on.
    ACCESS_KEY_ID = aws_config.get("aws.access.key.id").data  # we extract only the data part of it
    ACCESS_KEY_SECRET = aws_config.get("aws.access.key.secret").data

    # if you forget the '.data' you will get the following error:
    # TypeError: sequence item 0: expected str instance, PropertyTuple found

    return ACCESS_KEY_ID, ACCESS_KEY_SECRET


def upload_data(user_data: bytes, s3_file_name: str):
    s3r = initialize_s3_resource()

    # We then create an S3 Object into our bucket which points to a file called hello_s3.txt
    s3_object = s3r.Object('abhay.s3.documents.test1', s3_file_name)
    # and we then put the data into the S3 object.
    result = s3_object.put(Body=user_data)

    response = result.get('ResponseMetadata')
    if response.get('HTTPStatusCode') == 200:
        print('Data uploaded Successfully')
    else:
        print('Data Not Uploaded')


def upload_file(f: io.TextIOWrapper, s3_file_name: str) -> None:
    pass

def initialize_s3_resource() -> ServiceResource:
    access_key_id, access_key_secret = read_aws_keys()
    # Now lets properly create the boto3 session object:
    session = boto3.Session(aws_access_key_id=access_key_id, aws_secret_access_key=access_key_secret)
    # Create a resource from the session
    s3r = session.resource('s3')
    return s3r


if __name__ == '__main__':
    # the data could come from anywhere. For simplicity, lets hard code.
    data = b"Hello S3!!"
    upload_data(data, 'hello_s3.txt')
    upload_data(open('quotes.txt','rb'), "quotes-data.txt")

# OUTPUT:
# File uploaded Successfully

# What if you had a file that you wanted to upload? I have here a set of beautiful quotes that I want to upload. So here goes:

def upload_file(file: str) -> None:
    pass
