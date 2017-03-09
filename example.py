import os

from client import SDElementsClient, SDElementsAPIException

API_TOKEN = os.environ['SDE_API_TOKEN']

if __name__ == '__main__':
    client = SDElementsClient(API_TOKEN)

    try:
        print client.create_business_unit("")
    except SDElementsAPIException as e:
        print e.readable_error_message
