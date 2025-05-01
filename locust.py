from locust import HttpUser, task, between # 5: Import Locust classes for user simulation and timing

class PatientPortalUser(HttpUser): # 4: Define a simulated user for the patient portal
    wait_time = between(1, 5) # 3: Each user waits 1-5 seconds between actions (realistic load)

    @task
    def access_portal(self): # 2: This method simulates a user action (HTTP GET)
        self.client.get("/#YOUR_PATIENT_PORTAL_PATH") # 1: Replace with your app’s endpoint to test