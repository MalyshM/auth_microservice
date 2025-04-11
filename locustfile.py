from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 1)

    @task
    def load_test_endpoint(self):
        print(f"{self.host}/auth/pkce")
        self.client.get("/auth/pkce")
