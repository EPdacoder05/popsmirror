from locust import HttpUser, task, between  # 1: Import Locust classes for user simulation and timing

# App Developers: Use this class to simulate user workflows and test app endpoints under load.
class AppWorkflowUser(HttpUser):  # 2: Simulates an application user workflow
    wait_time = between(1, 5)  # 3: Waits 1-5 seconds between tasks

    @task
    def login(self):  # 4: Simulates a login POST request (customize endpoint/payload as needed)
        self.client.post("/login", json={"username": "testuser", "password": "password"})  # 5: Replace with your app's login endpoint and payload

    @task
    def submit_form(self):  # 6: Simulates submitting a form (customize endpoint/payload as needed)
        self.client.post("/form", json={"field1": "value1", "field2": "value2"})  # 7: Replace with your app's form endpoint and payload

# Data Engineers: Use this class to simulate data ingestion or ETL workflows.
class DataWorkflowUser(HttpUser):  # 8: Simulates a data ingestion workflow
    wait_time = between(1, 5)

    @task
    def ingest_data(self):  # 9: Simulates posting data for ingestion (customize endpoint/payload as needed)
        self.client.post("/data-ingestion", json={"data": "sample_data"})  # 10: Replace with your data ingestion endpoint and payload