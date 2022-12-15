# So we have managed to get our files on S3, how do we download? Ofcourse there will be something elementary about it!
# with boto3, there always is... so without me yapping too much, lets go and see for ourselves.

import datetime
import os.path
from typing import Final

import boto3

# We declare a global variable which gets accessed everywhere.
BUCKET_NAME: Final[str] = 'abhay.s3.documents.test1'
# did you see this? :) This is equivalent to writing: public static final String BUCKET_NAME = "..."
# Now you would think this will make the field final, but NO! :D :D You can still do this:

BUCKET_NAME = 'MY BUCKET'  # Lol!!! What the heck?? :) :) Well what line# 9 depicts is a "type hint", i.e. it informs
# the IDE (IntelliJ or linters) that this field was NOT supposed to be overridden. This re-assignment does NOT
# fail during Runtime! :) Remember python is inclined towards the "You know what you are doing" thought process :)
# So if you are not supposed to modify these things, well then DONT modify it :) :) Type checks are not strong for
# precisely this reason. This is a gentleman's club :P. I know what you're thinking... SO LAME!!! :D and I agree!

# so lets reset the bucket value back...:)
BUCKET_NAME: Final[str] = 'abhay.s3.documents.test1'


# let's create a download function that we will invoke from the main method
def download_file(file_name: str, bucket_name: str) -> None:
    """
    This method takes in a file pointer and a bucket name to download the file from.
    """
    # Initialize the client
    s3c = boto3.client('s3')

    # let's create a local file by
    # 1. splitting the filename and extension
    # 2. Appending the datetime MMDDYYY_HHMMSS to the filename
    # 3. Appending the file extension
    fname, fext = os.path.splitext(file_name)  # this is a cute function which returns a tuple of filename and extn!
    local_filename = fname \
                     + str(datetime.datetime.now().strftime("_%m%d%Y_%H%M%S")) \
                     + fext

    # You can split a single statement in python by inserting a backslash "\" to improve readability.
    print(f"Local filename: {local_filename}")
    s3c.download_file(bucket_name, file_name, local_filename)
    # and just like that file gets downloaded! :) How much simpler can it get?


# let's also define a method to delete a file from S3 bucket
def delete_file(file_name: str, bucket_name: str) -> None:
    # let's create a boto3 resource this time.
    s3r = boto3.resource('s3')
    s3r.Object(bucket_name, file_name).delete()  # and Bob's your uncle! :)


# and now the main program
def main() -> None:
    file_name = "quotes-data.txt"
    download_file(file_name, BUCKET_NAME)
    delete_file(file_name, BUCKET_NAME)


if __name__ == '__main__':
    main()
