from locust import HttpUser, task, between

class RecommendationUser(HttpUser):
    wait_time = between(0.5, 2)

    @task(3)
    def query_fast(self):
        self.client.get("/recommend?q=fast")

    @task(1)
    def query_long(self):
        self.client.get("/recommend?q=machine+learning+recommendation")
