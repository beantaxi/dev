assume-role ()
{
    # shellcheck disable=SC2016
    (( $# == 3 )) || { printf 'Usage: assume-role $roleArn $serialNumber $tokenCode\n' >&2; return 1; }
    local roleArn=$1
    local serialNumber=$2
    local tokenCode=$3

    local sessionName="session-role-${roleArn##*/}"
    local jql='.Credentials | [.AccessKeyId, .SecretAccessKey, .SessionToken] | @tsv'
    IFS=$'\t' read -r AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN \
    < <(aws sts assume-role --role-arn $roleArn --role-session-name "$sessionName" --serial-number "$serialNumber" --token-code $tokenCode | jq -r "$jql")
    export AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
}


aws-whoami ()
{
    aws sts get-caller-identity    
}


create-role-arn ()
{
    # shellcheck disable=SC2016
    (( $# == 2 )) || { printf 'Usage: create-role-arn $awsAccount roleName\n' >&2; return 1; }
    local awsAccount=$1
    local roleName=$2

    local roleArn="arn:aws:iam::$awsAccount:role/$roleName";
    printf '%s' "$roleArn"
}


get-mfa-serial-number ()
{
    aws iam list-mfa-devices --output text --query MFADevices[0].SerialNumber
}


unset-aws-vars ()
{
    unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
}