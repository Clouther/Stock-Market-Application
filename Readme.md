# Stock project
The objectives of the project is to have an end-to-end solution to predict tomorrow movement of stocks in the S&P500 stock. 

![Alt text](./static/img/Website.jpg?raw=true "Title")

<u> Next day predictions </u>

![Alt text](./static/img/Stock_Prediction.jpg?raw=true "Title")

<u> Model performance over the past 10 business days </u>

![Alt text](./static/img/Stock_Performance.jpg?raw=true "Title")

## Prerequisites
locally:
- [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) installed
- [Docker Desktop](https://docs.docker.com/get-docker/) installed


## Setup
Running on GCP:
1. [Create your project](https://cloud.google.com/resource-manager/docs/creating-managing-projects)
2. [Get the credentials (json)](https://cloud.google.com/docs/authentication/getting-started) and S=set up the environment variable `GOOGLE_APPLICATION_CREDENTIALS`
3. Hook GitHub repo to google build and allow the trigger for each push.


Running locally:
1. Fork this repository from your own github account
2. [Create your environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) using `scripts/environment.yml`.  
3. Activate the environment. `conda activate stock`
4. Run the app: `python app.py` 
5. Test the endpoint in a separated shell `curl http://localhost:8080/`


## Code
- `application.conf`: This file contains the parametrisation of the app. 
- `Dockerfile`: Anaconda base, the docker image is currently deployed on GCP
- `get_data.py`: You can use this script to download the stock history for S&P500
- `app.py`: This file contains the main for the Flask server.
- `src/algo`. This directory contains the code to fit and predict stock with our model.
- `src/business_logic`. Processes the query, deals with model storage
- `src/IO`. Fetches data, accessing the google storage, etc.






 
