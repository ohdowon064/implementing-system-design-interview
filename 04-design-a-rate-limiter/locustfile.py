from locust import HttpUser, constant, task


class RequestUser(HttpUser):
    wait_time = constant(1)

    @task
    def index(self):
        self.client.get("/posts")
