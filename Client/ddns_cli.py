import requests
import time
import socket


class Domain:
    def __init__(self, domain_name, domain_key=None, ttl_value=None, record_type=None):
        self.domain_name = domain_name
        self.domain_key = domain_key
        self.ttl_value = ttl_value
        self.record_type = record_type

    def __str__(self):
        return self.domain_name


class UpdaterClient(Domain):
    def __init__(self, server_url, server_port, username=None, password=None,
                 domain_name=None, domain_key=None, ttl_value=None, record_type=None):
        self.server_url = server_url
        self.server_port = server_port
        self.username = username
        self.password = password
        Domain.__init__(self, domain_name, domain_key, ttl_value, record_type)
        if self.domain_key is None:
            self.domain_key = self.get_domain_key()

    def __str__(self):
        return self.server_url + ':' + str(self.server_port)

    def is_super_updater(self):
        if self.username and self.password:
            return True
        else:
            return False

    def get_domain_key(self):
        if self.is_super_updater():
            secret = self.post(url_param='get_secret',
                              data={'username': self.username, 'password': self.password})
            if secret:
                return secret.get('secret', None)
        else:
            raise TypeError("Check your username and password to get domain's secret key")

    def update_ip(self):
        if self.domain_key is not None:
            data={
                'secret': self.domain_key,
                'Client_LAN': get_lan_ip(),
                'Client_Type': "egemeric's ddns client,EDDC,1.0",
            }
            self.post(url_param='update',data=data)

    def post(self, url_param, data):
        url = self.server_url + ':' + str(self.server_port) + '/dns/updater/' + self.domain_name + '/' + url_param + '/'
        print(url)
        try:
            req = requests.post(url, data=data)
            time.sleep(0.1)
        except requests.exceptions.ConnectionError:
            print('Connection Error')
            return False
        if req.status_code == 200:
            data = req.json()
            return data
        elif req.status_code == 401:
            raise Exception('your username or password is not matched')


def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]


if __name__ == '__main__':
    Updater_Server_Url = "http://127.0.0.1"
    Updater_Server_Port = 8000
    Updater_Server_User = "test"
    Updater_Server_Password = "test1234."
    Domain_Name = "home.egemeric.gen.tr"
    print(get_lan_ip())
    cli = UpdaterClient(
                        server_url=Updater_Server_Url,
                        server_port=Updater_Server_Port,
                        username=Updater_Server_User,
                        password=Updater_Server_Password,
                        domain_name=Domain_Name,
                        )
    cli.update_ip()


