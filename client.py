import requests


class SDElementsAPIException(Exception):
    def __init__(self, response, *args, **kwargs):
        super(SDElementsAPIException, self).__init__(*args, **kwargs)
        self.response = response

    @property
    def readable_error_message(self):
        return "{r.status_code} {r.reason}: {r.text}".format(r=self.response)


def make_request(request_url, request_body, request_headers, request_method="GET"):
    request_function = requests.get
    if request_method == "POST":
        request_function = requests.post
    elif request_method == "PUT":
        request_function = requests.put

    response = request_function(request_url, json=request_body, headers=request_headers)
    if not response.ok:
        # Request did not go through because of an error, throw an exception with the response to be analyzed later
        raise SDElementsAPIException(response)
    return response.json()


class SDElementsClient(object):
    business_units_api_path = "/api/v2/business-units/"
    applications_api_path = "/api/v2/applications/"

    def __init__(self, api_token, sde_server="cd.sdelements.com"):
        self.api_token = api_token
        self.server = sde_server

    @property
    def authorization_header_dict(self):
        # In order to authenticate with SDE server the Authorization header needs to be present with API token
        return {'Authorization': "Token " + self.api_token}

    @property
    def default_headers(self):
        """Return a default set of headers (Authorization, Accept, and Content-Type) to be used in API requests"""
        header_dict = {'Accept': "application/json", 'Content-Type': "application/json"}
        header_dict.update(self.authorization_header_dict)
        return header_dict

    def build_url(self, path):
        """Return a url to be used in an API request with path"""
        return "https://" + self.server + path

    def create_business_unit(self, name, users=None, groups=None, default_users=None, default_groups=None,
                             all_users=False):
        """
        Create a new business unit in the SDElements server.

        Check API docs at https://sdelements.github.io/slate/#create-a-new-business-unit for more info

        :rtype: dict
        :param name: The name of the new business unit.
        :param users: A list of users (emails) who are part of the business unit.
        :param groups: A list of group ids of the groups which are part of the business unit
        :param default_users: A list of dictionaries representing the default user roles for the users in the business
            unit. Each dictionary has an email field and a role field where the role is the role id. The users specified
            here should be members of the business unit unless all_users is true.
        :param default_groups: A list of dictionaries representing the default group roles for the users in the
            business unit. Each dictionary has an id field which is the group id and a role field where the role is the
            role id. The groups specified here should be members of the business unit unless all_users is true.
        :param all_users: Whether the business unit includes all users. Trying to create a business unit with this field
            set to True and specific users/groups specified is an error. Default is false.
        :return: A dictionary representing the newly created business unit
        """
        request_url = self.build_url(self.business_units_api_path)

        request_body = {'name': name}
        if users:
            # SDE API needs this field in the format: [{"email": "test@example.com"}, {"email": "test2@example.com"}]
            request_body['users'] = [{'email': user} for user in users]
        if groups:
            # SDE API needs this field in the format: [{"id": "G1"}, {"id": "G2"}]
            request_body['groups'] = [{'id': group_id} for group_id in groups]
        if default_users:
            request_body['default_users'] = default_users
        if default_groups:
            request_body['default_groups'] = default_groups
        if all_users:
            request_body['all_users'] = all_users

        return make_request(request_url, request_body, self.default_headers, "POST")

    def create_application(self, business_unit_id, name, priority=None):
        """
        Create a new application in the SDElements server.

        Check API docs at https://sdelements.github.io/slate/#create-a-new-business-unit for more info

        :rtype: dict
        :param business_unit_id: The ID of the business unit the application belongs to
        :param name: The name of the new application
        :param priority: Specifies the priority of the application to be either '0-none', '1-high', '2-medium' or
            '3-low'
        :return: A dictionary representing the newly created application
        """
        request_url = self.build_url(self.applications_api_path)
        request_body = {'business_unit': business_unit_id, 'name': name}
        if priority:
            request_body['priority'] = priority

        return make_request(request_url, request_body, self.default_headers, "POST")
