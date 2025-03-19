# Welcome to My Movie Recommendation System

## Project Overview
This project is a custom-built movie recommendation engine that provides tailored film suggestions based on your input. I developed a modern, user-friendly web interface using Flask, while leveraging natural language processing techniques for backend analysis. The system is deployed on Google Cloud with an automated CI/CD pipeline to ensure seamless updates.


![Movie-Recommendation-Home-Screen](https://github.com/rajvijay1504/Movie_Recommendation/blob/main/images/image1.png)



### Running the web application locally: 
Step 1: Cloning github repository:
```python
git clone https://github.com/rajvijay1504/Movie_Recommendation.git 
```

Step 2: 
```python
cd Movie_Recommendation/
```

Step 3: Installing all the package dependencies.
```python
make install
```

Step 4: Running Flask app locally: (Copy link displayed on console on your preffered browser)
```python
python3 main.py
```

### Website Navigation Instructions:
Step 1: Enter a movie title (or the keyword of that movie) that you would like in the search bar and hit submit.

Step 2: This brings you to a new webpage of all the search results. If the search is not found, please click “Try again” to retry. If the search is successful, find the movie that you want and copy and paste it's IMDB's ID (on the right side of the movie title) to the search bar and hit submit to begin search. You could also check the movie summary by clicking the movie title. This will bring you to the IMDB website of that movie.

Step 3: After the computation is finished. You will be redirected to the recommendation result web page. The five movies shown on the page are the movies we recommended based on the movie you gave us. For more info, you could click on the movie title. This will bring you to the IMDB website of that movie.

Step 4: To recommend different movies, hit the “Try a different movie” button.

### Set up Google Cloud Project:
Step 1: Create new gcp project:

Step 2: Check to see if your console is pointing to the correct project:
```python
gcloud projects describe $GOOGLE_CLOUD_PROJECT
```

Step 3: Set working project if it is not correct:
```python
gcloud config set project $GOOGLE_CLOUD_PROJECT
```

Step 4: Follow steps 1-4 under "Running the Web Application locally" to set up github repo and test Flask application:

Step 5: In the root project of the folder, replace PROJECT-ID below with your GCP project-id, and build the google cloud containerized flask application:
```python
gcloud builds submit --tag gcr.io/<PROJECT-ID>/app
```

Step 6: In the root folder of the project, replace PROJECT-ID below with your GCP project-id, and run the flask application:
```python
gcloud run deploy --image gcr.io/<PROJECT-ID>/app --platform managed
```

Step 7: Paste the URL link provided on the console, in your preferred browser to run the application!


### Seting up Continuous Integration/Continuous Deployment:

Step 1: Navigate to Github Actions and create a new workflow. Add a main.yaml file with the below specifications:
```python
name: Movie Recommendation Engine

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.8
      uses: actions/setup-python@v1
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        make install
    - name: Lint with pylint
      run: |
        make lint
```

Step 2: Open Cloud Run on GCP console:

Update Memory specification to 512 MiB.

Update Timeout specification to 500 seconds.

Save and Re-Deploy Cloud Run application.

![Cloud-Run-Configuration-Specs](https://github.com/rajvijay1504/Movie_Recommendation/blob/main/images/image2.png)

Step 3: Open Cloud Build on GCP console:

Create a new trigger.

Specify github repository.

Triggered on Master branch.

Deployment specifications already available in: cloudbuild.yaml file.

Step 4: Test CI/CD:
Update github repo by merging feature branch into master branch. This will automatically trigger Github actions to lint and test the code, along with triggering Cloud Build to deploy the code updates into the production flask container. 


### Cloud Architecture
![Cloud Architecture](https://github.com/rajvijay1504/Movie_Recommendation/blob/main/images/image3.png)

The above diagram is the cloud architecture of our movie recommendation engine. Inside the cloud diagram we have our google cloud services listed: Storage Bucket, Compute Instance, Cloud Run, and Cloud Build. The storage bucket stores the movie dataset and the docker image of our website. The compute instances are where code files lie within the cloud platform. Cloud run sets up continuous deployment which allows us to deploy our website smoothly every time we make changes. Outside of cloud, our github repository set up github actions to allow us to continuously integrate our pushes into the repository.

### Tools and Technologies Used:
##### Backend: 
1. GCP Storage Bucket

2. GCP Compute Instance

3. GCP Cloud Run

4. GCP Cloud Build

5. NLP methods

##### Frontend:
1. Flask

2. HTML

3. CSS

4. JavaScript




