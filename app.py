# Import necessary modules from Flask
from flask import Flask, request
# Import SQLAlchemy and Migrate for database interaction and migrations
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests

# Initialize the Flask application
app = Flask(__name__)

KOBO_API_URL = "https://kf.kobotoolbox.org/api/v2/assets/aDHXtBZLF4fHa3tXD4RQMT/data.json"

# Define a new route for handling requests to '/fetch-data' endpoint
@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    try:
        # Make a GET request to KoboToolbox API to fetch data
        response = requests.get(KOBO_API_URL)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON data from the response
            data = response.json()
            # Process the data as needed (here, assuming data is a list of records)
            # For example, you can insert the fetched data into your database
            for record in data:
                new_health = HealthModel(
                    disease=record['disease'],
                    age=record['age'],
                    gender=record['gender'],
                    income=record['income']
                )
                db.session.add(new_health)
                db.session.commit()
            # Return a success message indicating the successful fetch and insertion
            return {"message": "Data fetched and inserted successfully."}
        else:
            # Return an error message if the request to KoboToolbox API fails
            return {"error": "Failed to fetch data from KoboToolbox API."}
    except Exception as e:
        # Handle any exceptions that might occur during the process
        return {"error": str(e)}




# Set the URI for the PostgfreSQL database to be used in the application
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/health_api"
# Initialize SQLAlchemy with the Flask application instance
db = SQLAlchemy(app)
# Initialize Flask-Migrate with the Flask application instance and SQLAlchemy database instance
migrate = Migrate(app, db)

# Create a model representing the 'cars' table in the database
class HealthModel(db.Model):
    __tablename__ = 'Health'

    # Define columns in the 'cars' table
    id = db.Column(db.Integer, primary_key=True)
    disease = db.Column(db.String())
    age = db.Column(db.String())
    gender = db.Column(db.String())
    income = db.Column(db.String())
    

    # Constructor to initialize the model with values for name, model, and doors
    def __init__(self, disease, gender, age,income):
        self.disease = disease
        self.gender = gender
        self.age = age
        self.income = income
    

    # Representation method to provide a readable representation of the model object
    def __repr__(self):
        return f"<Health {self.disease}>"

# Define a route for handling requests to '/health' endpoint
@app.route('/health', methods=['POST', 'GET'])
def handle_health():
    # Handle POST requests to create a new health entry in the database
    if request.method == 'POST':
        # Check if the request payload is in JSON format
        if request.is_json:
            # Parse JSON data from the request
            data = request.get_json()
            print(data,">>>>>>>>>>>>>>>>>>>")#know where data has been created in the logs
            # Create a new car object with data from the JSON payload
            new_health = HealthModel(disease=data['disease'], 
                                age=data['age'], gender=data['gender'],
                                    income=data['income'])
            # Add the new health object to the database session
            db.session.add(new_health)
            # Commit the changes to the database
            db.session.commit()
            # Return a success message indicating the creation of the new health entry
            return {"message": f"health {new_health.disease} has been created successfully."}
        # Return an error message if the request payload is not in JSON format
        else:
            return {"error": "The request payload is not in JSON format"}

    # Handle GET requests to retrieve all health entries from the database
    elif request.method == 'GET':
        # Query all car objects from the database
        health = HealthModel.query.all()
        # Format the results as a list of dictionaries containing car information
        results = [
            {
                "disease": healthy.disease,
                "age": healthy.age,
                "gender": healthy.gender,
                "income": healthy.income
            } for healthy in health]
        # Return the count of car entries and the list of car information dictionaries
        return {"count": len(results), "health": results}

# Define a route for handling requests to '/cars/<car_id>' endpoint
@app.route('/health/<health_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_car(health_id):
    # Query the car object from the database with the specified car ID
    health = HealthModel.query.get_or_404(health_id)

    # Handle GET requests to retrieve the car information
    if request.method == 'GET':
        # Create a dictionary containing car information
        response = {
            "disease": health.disease,
            "age": health.age,
            "gender": health.gender,
            "income": health.income
    
        }
        # Return a success message and the car information dictionary
        return {"message": "success", "health": response}

    # Handle PUT requests to update the car information
    elif request.method == 'PUT':
        # Parse JSON data from the request
        data = request.get_json()
        # Update the car object with new data from the JSON payload
        health.disease = data['disease']
        health.age = data['age']
        health.gender = data['gender']
        health.income = data['income']
        # Add the updated car object to the database session
        db.session.add(health)
        # Commit the changes to the database
        db.session.commit()
        # Return a success message indicating the successful update of the car information
        return {"message": f"health {health.disease} successfully updated"}

    # Handle DELETE requests to delete the car entry from the database
    elif request.method == 'DELETE':
        # Delete the car object from the database session
        db.session.delete(health)
        # Commit the changes to the database
        db.session.commit()
        # Return a success message indicating the successful deletion of the car entry
        return {"message": f"health {health.name} successfully deleted."}

# Define a route for handling requests to '/favicon.ico' endpoint
@app.route('/favicon.ico')
def favicon():
    # Return an empty response with a 200 status code for favicon.ico requests
    return '', 200

#run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
