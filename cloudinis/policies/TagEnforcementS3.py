from .validator import validator
from .object_resources import S3

def TagEnforcementS3(user, activatedPolicy):
    # regionList = ["us-east-2", "us-east-1", "us-west-1", "us-west-2", "ap-east-1", "ap-south-1", "ap-northeast-3", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-northeast-1", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "eu-north-1", "me-south-1", "sa-east-1"]
    regionList = ["us-east-1"]

    for region in regionList:
        response = S3.list_all_of_a_kind(user, region)

        for bucket in response["Buckets"]:
            tags = S3.list_tags(bucket, user, region)
            if tags is False:
                validator(bucket["Name"], activatedPolicy, user, region)
            else:
                try:
                    if not set(activatedPolicy.metadata).issubset(list(tags.keys())):
                        validator(bucket["Name"], activatedPolicy, user, region)
                except KeyError:
                    validator(bucket["Name"], activatedPolicy, user, region)

    return True