import json
import random
import string

from locust import HttpUser, task, between


class LoadTestUser(HttpUser):
    wait_time = between(0, 0)
    baseUrl = "http://127.0.0.1:8000/api/v1/"
    token = ""

    file_content = open("content.txt", "r")
    content = file_content.read()

    def on_start(self):
        url = self.baseUrl + "auth/"
        payload = {'username': 'load-test', 'password': 'user1234'}
        headers = {'Content-Type': 'application/json'}
        response = self.client.post(
            url=url,
            headers=headers,
            data=json.dumps(payload)
        )

        self.token = response.json()['access']

    @task
    def vectors(self):

        url = self.baseUrl + "vectors/fr/"
        payload = {'content': self.content}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        self.client.post(
            url=url,
            headers=headers,
            data=json.dumps(payload)
        )
