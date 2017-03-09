import requests


class SDElementsAPIException(Exception):
    def __init__(self, response, *args, **kwargs):
        super(SDElementsAPIException, self).__init__(*args, **kwargs)
        self.response = response

    @property
    def readable_error_message(self):
        return "{r.status_code} {r.reason}: {r.text}".format(r=self.response)


class SDElementsClient(object):
    def __init__(self, api_token, sde_server="cd.sdelements.com"):
        self.api_token = api_token
        self.server = sde_server

    @property
    def authorization_header_dict(self):
        return {'Authorization': "Token " + self.api_token}

    @property
    def default_headers(self):
        header_dict = {'Accept': "application/json", 'Content-Type': "application/json"}
        header_dict.update(self.authorization_header_dict)
        return header_dict

    def build_url(self, path):
        return "https://" + self.server + path

    def create_business_unit(self, name, users=None, groups=None, default_users=None, default_groups=None,
                             all_users=False):
        request_headers = self.default_headers
        request_url = self.build_url("/api/v2/business-units/")
        request_body = {'name': name}
        if users:
            request_body['users'] = [{'email': user} for user in users]
        if groups:
            request_body['groups'] = [{'id': group_id} for group_id in groups]
        if default_users:
            request_body['default_users'] = default_users
        if default_groups:
            request_body['default_groups'] = default_groups
        if all_users:
            request_body['all_users'] = all_users

        response = requests.post(request_url, headers=request_headers, json=request_body)
        if not response.ok:
            raise SDElementsAPIException(response)
        return response.json()
