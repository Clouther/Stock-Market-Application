# Stock project
The objectives of the project is to have an end-to-end solution to predict stock price/evolution. 

Prerequisites:
- [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) installed
- [Docker](https://docs.docker.com/get-docker/) installed
 

## Setup steps
On your Google GCP account:
1. [Create your project](https://cloud.google.com/resource-manager/docs/creating-managing-projects)
2. [Get the credentials (json)](https://cloud.google.com/docs/authentication/getting-started) and S=set up the environment variable `GOOGLE_APPLICATION_CREDENTIALS`
3. Hook your github repo to google build. Allow the trigger for each push.


On your machine:
1. Fork this repository from your own github account
2. [Create your environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) using `scripts/environment.yml`.  
3. Activate the environment. `conda activate stock`
4. Run the app: `python app.py` 
5. Test the endpoint in a separated shell `curl http://localhost:8080/`


## Code organisation
- `application.conf`: This file contains the parametrisation of the app. It is used in the code to load constant like the version number of the app.
- `Dockerfile`: This file contains the definition of the steps to create the docker image. The image will be created by google build (CI/CD) and saved into the google storage. You can use this file to test the docker image on your local machine. See the section "Build and test the docker image".
- `get_data.py`: You can use this script to download the stock hosory for SNP500
- `app.py`: This file contains the main for the Flask server. It is also the entrypoint of the app. At this moment, there is only 2 end points defined. The purpose of this project is not to be a master developing an app, so your work in this file should remains minimal. 
- `src/algo`. This directory contains the code to fit and predict stock with a model. You can add your own here.
- `src/business_logic`. This code contains the logic to process the query, deal with model storage etc...
- `src/IO`. This code deal with fetching the data, accessing the google storage etc...






 
