import os

from locust import HttpUser, between, task


class OdooPerformanceUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.base_path = "/web/login"

    @task(5)
    def open_login_page(self):
        with self.client.get(
            self.base_path,
            name="GET /web/login",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(
                    f"Unexpected status: {response.status_code}"
                )
            elif not response.text:
                response.failure("Empty response body")
            else:
                response.success()

    @task(2)
    def check_server_response(self):
        with self.client.get(
            "/web/webclient/version_info",
            name="GET /web/webclient/version_info",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(
                    f"Unexpected status: {response.status_code}"
                )