# Let's upload a text file on AWS
import boto3

ACCESS_KEY_ID='' # not to be used. Read further
ACCESS_KEY_SECRET='' # not to be used. Read further

# First we need to create a session with boto3
session1 = boto3.Session(aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_KEY_SECRET)

# Now I could hard code the secret and the access key id in the code itself, but what kind of programmer do you take
# me for? Huh? Any child 1-year-old could tell you we need to externalize such things ;) So we have to store this
# into a properties file. So let's create a properties file 'aws_keys.properties' and then add the access key and
# secret in there. But how do I read the properties file?

# Enter - jproperties. You need to install the jproperties module first using the command: pip install jproperties

from jproperties import Properties

# The Properties object is very similar to a Dictionary Object.
aws_config = Properties()

# We read the properties file into the aws_config properties Object
with open('aws_keys.properties', 'rb') as config_file:
    aws_config.load(config_file)

# and now reading those properties is peanuts. However, know that - the value part is stored in a named tuple of data
# and metadata. This Object is called PropertyTuple. We will look into metadata later on.
ACCESS_KEY_ID = aws_config.get("aws.access.key.id").data # we extract only the data part of it
ACCESS_KEY_SECRET = aws_config.get("aws.access.key.secret").data

# if you forget the '.data' you will get the following error:
# TypeError: sequence item 0: expected str instance, PropertyTuple found

# Now lets properly create the boto3 session object:
session = boto3.Session(aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_KEY_SECRET)

# Create a resource from the session
s3r = session.resource('s3')

data = b"Hello S3!!"

s3_object = s3r.Object('abhay.s3.documents.test1', 'hello_s3.txt')

result = s3_object.put(Body=data)

response = result.get('ResponseMetadata')
if response.get('HTTPStatusCode') == 200:
    print('File uploaded Successfully')
else:
    print('File Not Uploaded')

# OUTPUT:
# File uploaded Successfully

