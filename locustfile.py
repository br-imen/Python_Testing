from locust import HttpUser, task, between, SequentialTaskSet

class UserBehavior(SequentialTaskSet):

    def on_start(self):
        # Perform a login operation as part of the starting sequence
        response = self.client.post("/showSummary", data={"email": "john@simplylift.co"})
        # Save the session cookie
        if 'session' in response.cookies:
            self.client.cookies.set('session', response.cookies['session'])

    @task(1)
    def index(self):
        self.client.get("/")
    
    @task(2)
    def show_summary(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task(3)
    def book_competition(self):
        self.client.get("/book/Spring%20Festival/Simply%20Lift")
    
    @task(4)
    def purchase_places(self):
        self.client.post("/purchasePlaces", data={
            "places": 1,
            "competition": "Spring Festival",
            "club": "Simply Lift"
        })
    
    @task(5)
    def display_points(self):
        self.client.get("/display-points")

class WebsiteUser(HttpUser):
    host = "http://localhost:8000" 
    tasks = [UserBehavior]
    wait_time = between(1, 5)