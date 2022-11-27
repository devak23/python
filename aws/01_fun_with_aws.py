# Before we begin, we setup the IAM user (in aws console). Uugh this is boring, but necessary. You need to set up a
# root user (one you signed in with) and an IAM user which you will use to run your programs with. You need to
# download the access id and access key as we will be using it with the command line tools. We install aws-cli using
# pip install aws-cli.  We then configure the aws-cli using the command: aws-configure. This will typically ask you
# for the access id, the key and the region. We install boto3 library which allows easier integration of python with
# AWS ... and all boring parts are done. Now lets dive into code.

import boto3

s3r = boto3.resource('s3')  # a handle to S3 resource
s3c = boto3.client('s3')  # a handle to the S3 client


def show_cors_info():
    cors = s3c.get_bucket_cors(Bucket='abhay.s3.documents.test')
    print(cors)


if __name__ == '__main__':
    # let's see the buckets we have configured in S3
    for bucket in s3r.buckets.all():
        print(bucket.name)

    # This doesn't print anything! :(... Correctly so. Because we didn't configure anything with S3 yet. So we can go
    # back to the AWS page and very quickly create a S3 bucket, OR we can show off our command line skills and try to
    # create a bucket from the command line. The command line is way cool when you have people (especially who don't
    # know stuff) around you. That way you establish your intellectual superiority over them by showing off how much
    # of a "unix-person" you really are. When you are alone, go to the damn page and create a simple bucket if you like.

    # If you have aws-cli, then we will use s3api to create a bucket. Type 'aws s3api help' and see that you get a
    # "create-bucket option". So the command would intuitively be:
    # aws s3api create-bucket --bucket abhay.s3.documents.test1 --region ap-south-1
    # ================================================================================================================
    # OUTPUT: An error occurred (IllegalLocationConstraintException) when calling the CreateBucket operation: The
    # unspecified location constraint is incompatible for the region specific endpoint this request was sent to.
    # ================================================================================================================

    # Okay, what went wrong ? Well, if you don't specify a region, the bucket will be created by default in US East (N.
    # Virginia). For any other region that you specify, you need to specify a LocationConstraint. So let's modify our
    # command:
    # aws s3api create-bucket --bucket abhay.s3.documents.test1 --create-bucket-configuration LocationConstraint=ap-south-1

    # OUTPUT:
    # ~ aws s3api create-bucket --bucket abhay.s3.documents.test1 --create-bucket-configuration LocationConstraint=ap-south-1
    # {
    #    "Location": "http://abhay.s3.documents.test1.s3.amazonaws.com/"
    # }
    # Congratulations you are now a command-line guru!! Well done!

    # After you create the S3 bucket re-run the same program and you should get to see your bucket name. In my case it's
    # OUTPUT: abhay.s3.documents.test

    # Now let's try to print some CORS info.
    try:
        show_cors_info()
        cors_config_set = True
    except:
        cors_config_set = False

    print(f"CORS Config set: {cors_config_set}")
    # OUTPUT:
    # (NoSuchCORSConfiguration) when calling the GetBucketCors operation: The CORS configuration does not exist.

    # INTERVIEW QUESTION: So what is CORS configuration? and why do we need it?

    # The purpose of an AWS S3 bucket is to allow people to access the files that you store. CORS is short for:
    # Cross-Origin Resource Sharing - A HTTP header based mechanism that allows a server to indicate the browser that
    # any domain other than its own is sending resources and that it should permit loading those resources. What
    # resources are we talking about? Oh, these could be anything like images, CSS, fonts or a file too. Before
    # making the CORS request, a "preflight request" is automatically issued by the browser to check if the CORS
    # protocol is understood and the server is aware of using specific methods and headers. This is generally an
    # "OPTIONS request" if you peep into the browser console

    # So lets set up the CORS Configuration. A CORS Configuration consists of specifying AllowedHeaders,
    # AllowedMethods, AllowedOrigins, ExposeHeaders and MaxAgeSeconds. Let's define it like so:

    if not cors_config_set:
        cors_configuration = {
            'CORSRules': [{
                'AllowedHeaders': ['Authorization'],
                'AllowedMethods': ['GET', 'PUT'],
                'AllowedOrigins': ['*'],
                'ExposeHeaders': ['GET', 'PUT'],
                'MaxAgeSeconds': 3000
            }]
        }
        s3c.put_bucket_cors(Bucket='abhay.s3.documents', CORSConfiguration=cors_configuration)

    # Now lets print the cors info again.
    show_cors_info()
