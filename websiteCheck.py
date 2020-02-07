#!/usr/bin/env python3
import os
import urllib.request
import re
import boto3

client = boto3.client('cloudwatch')


def fetch_url(url):
    ''' Fetch a URL and return the body '''
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')
    return html


def request_match(body, string):
#    print(body)
    body_new = body.replace('\n', ' ').replace('\r', '')
#    print(body_new, string)
    if re.match(".*" + string + ".*", body_new):
        return True
    else:
        return False


def send_result_to_cloudwatch(url, value):
    response = client.put_metric_data(
        Namespace='site_monitoring',
        MetricData=[
            {
                'MetricName': 'site_monitoring',
                'Dimensions': [
                    {
                        'Name': 'site',
                        'Value': url
                    }
                ],
                'Value': value
            }
        ]
    )

def main():
    try:
        url= os.environ['url']
        string= os.environ['string']
    except:
        print("url or string environment variable not set")
        raise
    try:
        body= fetch_url(url)
    except:
        print("unable to fetch url")
        send_result_to_cloudwatch(url, 0)
        raise
    print("Checking " + url + " for \"" + string + "\"")
    match= request_match(body, string)
    print(match)
    if match:
        print('we have a match')
        print('send a 1 to cloudwatch')
        send_result_to_cloudwatch(url, 1)
    else:
        print('we don\'t have a match')
        print('send a 0 to cloudwatch')
        send_result_to_cloudwatch(url, 0)

def lambda_handler(event, context):
    main()

if __name__ == "__main__":
    main()
