import os

from client import SDElementsClient, SDElementsAPIException

# You can set the SDE_API_TOKEN in the environment variables
API_TOKEN = os.environ['SDE_API_TOKEN']

if __name__ == '__main__':
    client = SDElementsClient(API_TOKEN)

    try:
        new_business_unit = client.create_business_unit("Test BU")
        print new_business_unit

        new_application = client.create_application(new_business_unit['id'], "Test App")
        print new_application
    except SDElementsAPIException as e:
        print e.readable_error_message
