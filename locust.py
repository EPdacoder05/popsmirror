from locust import HttpUser, task, between  # Import Locust classes for user simulation and timing

# App Developers: Use this class to simulate user workflows and test app endpoints under load.
class AppWorkflowUser(HttpUser):  # Simulates an application user workflow
    wait_time = between(1, 5)  # Waits 1-5 seconds between tasks

    @task
    def login(self):  # Simulates a login POST request (customize endpoint/payload as needed)
        self.client.post("/login", json={"username": "testuser", "password": "password"}) # Replace with your app's login endpoint and payload

    @task
    def submit_form(self):  # Simulates submitting a form (customize endpoint/payload as needed)
        self.client.post("/form", json={"field1": "value1", "field2": "value2"})  # Replace with your app's form endpoint and payload

# Data Engineers: Use this class to simulate data ingestion or ETL workflows.
class DataWorkflowUser(HttpUser):  # Simulates a data ingestion workflow
    wait_time = between(1, 5)

    @task
    def ingest_data(self):  # Simulates posting data for ingestion (customize endpoint/payload as needed)
        self.client.post("/data-ingestion", json={"data": "sample_data"})  # Replace with your data ingestion endpoint and payload