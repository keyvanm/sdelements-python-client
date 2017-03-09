import os

from client import SDElementsClient, SDElementsAPIException

# You can set the SDE_API_TOKEN in the environment variables
API_TOKEN = os.environ['SDE_API_TOKEN']

if __name__ == '__main__':
    client = SDElementsClient(API_TOKEN)

    try:
        print client.create_business_unit("Test BU")
    except SDElementsAPIException as e:
        print e.readable_error_message
