# Before we begin, we setup the IAM user (in aws console). Uugh this is boring, but necessary. You need to set up a
# root user (one you signed in with) and an IAM user which you will use to run your programs with. You need to
# download the access id and access key as we will be using it with the command line tools. We install aws-cli using
# pip install aws-cli.  We then configure the aws-cli using the command: aws-configure. This will typically ask you
# for the access id, the key and the region. We install boto3 library which allows easier integration of python with
# AWS ... and all boring parts are done. Now lets dive into code.

import boto3
# You might be wondering what is boto and boto3? Boto has become the official AWS SDK for Python. Boto is a Portuguese
# name given to several types of dolphins in the Amazon river. You might wonder what are dolphins doing in a river!?
# Indeed they exist!! Check: https://en.wikipedia.org/wiki/Boto#:~:text=Boto%20is%20a%20Portuguese%20name,are%20often%20considered%20primitive%20dolphins.
# Boto3 replaced Boto2 which lacks compatibility with latest versions of Python. Anyhow...

s3r = boto3.resource('s3')  # create a handle to S3 resource
s3c = boto3.client('s3')  # create a handle to the S3 client


def show_cors_info():
    cors = s3c.get_bucket_cors(Bucket='abhay.s3.documents.test1')
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

    # After you create S3 bucket, re-run the same program, and you should get to see your bucket name. In my case it's
    # OUTPUT: abhay.s3.documents.test1

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
        s3c.put_bucket_cors(Bucket='abhay.s3.documents.test1', CORSConfiguration=cors_configuration)

    # Now lets print the cors info again.
    try:
        show_cors_info()
    except:
        # and yet an error again: An error occurred (NoSuchBucket) when calling the GetBucketCors operation: The
        # specified bucket does not exist. We know for sure that the bucket exists (else why would it print it),
        # but something is causing it to report NoSuchBucket. That has got to be the ACL! That was confirmed when I
        # logged back into AWS Console and saw it with my eyes:

        # So how do we fix this? If there was a create command, there's got to be something of update as well! Let's
        # check the aws s3api help menu... and what do you know!? :) we do have a put-bucket-acl command. So now we
        # can update the permissions by issuing: aws s3api put-bucket-acl ... But wait, even the aws s3api is finally
        # an API call to AWS. So why not do it the 'python way'? In fact, everything that you do via mouse clicks on
        # the browser can be done by command line and whatever that you can do via command line can be done
        # programmatically! So let's assign the permissions via an IAM policy to the bucket via our python script
        # itself. Here is a policy that will permit basic
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AddPerm",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:*"],
                    "Resource": ["arn:aws:s3:::abhay.s3.documents.test1/*"]
                }
            ]
        }
        # But this is a dictionary, and we need a JSON string version of this policy. Enter:
        import json

        bucket_policy_json = json.dumps(bucket_policy)
        print(bucket_policy_json)
        s3c.put_bucket_policy(Bucket='abhay.s3.documents.test1', Policy=bucket_policy_json)
        print('Policy applied!')

        # OUTPUT:
        # abhay.s3.documents.test1
        # CORS Config set: False
        # {"Version": "2012-10-17", "Statement": [{"Sid": "AddPerm", "Effect": "Allow", "Principal": "*", "Action": ["s3:*"], "Resource": ["arn:aws:s3:::abhay.s3.documents.test1/*"]}]}
        # Policy applied!

        # PRODUCTIVITY TIP!! When you copy-paste a sample from the internet, try NOT to be over-smart like me! :|
        # I referenced a stack-overflow sample in order to set the policy and very naively, I changed the "Version" to
        # 2022-11-27.1 thinking that maybe this the version of the policy that gets applied to my bucket and BAM!! -

        # This is what I got: date botocore.exceptions.ClientError: An error occurred (MalformedPolicy) when
        # calling the PutBucketPolicy operation: The policy must contain a valid version string

        # After scratching head for some time and then looking at few more posts, one good soul had mentioned that the
        # Version I changed so proactively was in fact NOT SUPPOSED TO BE CHANGED!! The Version is the current version
        # of the policy language and not what I was thinking. Look no further amigo!
        # https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_version.html

    # Once the policy is correctly set, this is what I see as CORS Info:
    # OUTPUT:
    # {
    #   'ResponseMetadata': {
    #     'RequestId': 'MPKV6QTQ3KDQRYD7',
    #     'HostId': 'sJ6iV/vzgAB8Sm/FKH0kv/sZm8C5vcWyo9bPZOywntr08nm3bac6Pc+zRmkGDd76wXusCdUEzyQ=',
    #     'HTTPStatusCode': 200,
    #     'HTTPHeaders': {
    #       'x-amz-id-2': 'sJ6iV/vzgAB8Sm/FKH0kv/sZm8C5vcWyo9bPZOywntr08nm3bac6Pc+zRmkGDd76wXusCdUEzyQ=',
    #       'x-amz-request-id': 'MPKV6QTQ3KDQRYD7',
    #       'date': 'Sun, 27 Nov 2022 16:13:02 GMT',
    #       'transfer-encoding': 'chunked',
    #       'server': 'AmazonS3'
    #     },
    #     'RetryAttempts': 0
    #   },
    #   'CORSRules': [{
    #     'AllowedHeaders': ['Authorization'],
    #     'AllowedMethods': ['GET', 'PUT'],
    #     'AllowedOrigins': ['*'],
    #     'ExposeHeaders': ['GET', 'PUT'],
    #     'MaxAgeSeconds': 3000
    #   }]
    # }

    # So far so good? :)
    # Now lets print the ACL for the same bucket:
    acl = s3c.get_bucket_acl(Bucket="abhay.s3.documents.test1")
    print (acl)
    # OUTPUT:
    # {
    #   'ResponseMetadata': {
    #     'RequestId': 'VNKV25JYJ8VE151F',
    #     'HostId': '5yxbm9W4X209CE2aL9SMZULCNggNz6ybDEthTl8O/Pj0a4SgaOIZwMCbrYHnlOsGyEDDn5Aw/H4=',
    #     'HTTPStatusCode': 200,
    #     'HTTPHeaders': {
    #       'x-amz-id-2': '5yxbm9W4X209CE2aL9SMZULCNggNz6ybDEthTl8O/Pj0a4SgaOIZwMCbrYHnlOsGyEDDn5Aw/H4=',
    #       'x-amz-request-id': 'VNKV25JYJ8VE151F',
    #       'date': 'Sun, 27 Nov 2022 16:19:56 GMT',
    #       'content-type': 'application/xml',
    #       'transfer-encoding': 'chunked',
    #       'server': 'AmazonS3'
    #     },
    #     'RetryAttempts': 0
    #   },
    #   'Owner': {
    #     'ID': '96e311bdf06256aaec43b579440674903d6558222d4a7ac8eadd24ded3111e01'
    #   },
    #   'Grants': [{
    #     'Grantee': {
    #       'ID': '96e311bdf06256aaec43b579440674903d6558222d4a7ac8eadd24ded3111e01',
    #       'Type': 'CanonicalUser'
    #     },
    #     'Permission': 'FULL_CONTROL'
    #   }]
    # }
