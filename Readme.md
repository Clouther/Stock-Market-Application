# Stock project
This repository is for students from YCNG 228 course.
The objectives of the project is to develop an end to end solution to predict stock price/evolution. 

* Set up the git repo on [github](https://docs.github.com/en/github/getting-started-with-github/create-a-repo).  
* Set up the CI/CD on [GCP](https://cloud.google.com/cloud-build/docs/automating-builds/run-builds-on-github)

Prerequisites:
- [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) installed
- [Docker](https://docs.docker.com/get-docker/) installed
 

## Setup steps
On your Google GCP account:
1. [Create your project](https://cloud.google.com/resource-manager/docs/creating-managing-projects)
2. [Get the credentials (json)](https://cloud.google.com/docs/authentication/getting-started) and S=set up the environment variable `GOOGLE_APPLICATION_CREDENTIALS`
3. Hook your github repo to google build. Allow the trigger for each push.


On your machine:
1. Fork this repository in your github account
2. [Create your environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) using `scripts/environment.yml`.  
3. Activate the environment. `conda activate stock`
4. Run the app: `python app.py` 
5. Test the endpoint in a separated shell `curl http://localhost:8080/`

If ou get this message: 
```
Hello you should use an other route:!
EX: get_stock_val/<ticker>
```
You succeeded!! 

Now you have the ability to try to change the code and to put your own model into the app. 

## Code organisation
- `application.conf`: This file contains the parametrisation of the app. It is used in the code to load constant like the version number of the app.
- `Dockerfile`: This file contains the definition of the steps to create the docker image. The image will be created by google build (CI/CD) and saved into the google storage. You can use this file to test the docker image on your local machine. See the section "Build and test the docker image".
- `get_data.py`: You can use this script to download the stock hosory for SNP500
- `app.py`: This file contains the main for the Flask server. It is also the entrypoint of the app. At this moment, there is only 2 end points defined. The purpose of this project is not to be a master developing an app, so your work in this file should remains minimal. 
- `build_and_deploy_docker_image.sh`. This file contains some (basic) instruction on how to build a docker image and running it.
- `src/algo`. This directory contains the code to fit and predict stock with a model. You can add your own here.
- `src/business_logic`. This code contains the logic to process the query, deal with model storage etc...
- `src/IO`. This code deal with fetching the data, accessing the google storage etc...

Remember that this organisation and implementation is here to help you to start with something working. Feel free to break it and change anything. The more you try, the more you will learn.

# APP workflow
The app is using a flask server to process the queries. When the server receive a query on `/get_stock_val/<ticker>` where `<ticker>` is a stock name, it will:
1. Check if a model exists for this specific ticker
    - If the model exists on google storage, fetch the model.
    - If the model does not exists, download the data and train the model. Save the model on google storage.
2. Download the last days of data for this ticker (X of the model).
3. Do the inference and return it.

This is one of the most simple workflow. Feel free to change it and add complexity. However, increasing complexity comes at a cost, so, you need good reasons.

# Development workflow

You should see this process as circles. You might spend a lot of time iterating on models/strategies. However, you should always stay close to a production state where the code can run on GCP. To do so, I recommend baby steps and make sure your changes will not break the app functionality.  

# Develop and test your code
If you want to change the code and create your own version:
1. Make your changes in the code the way you want. Ideally, you should create a test for it.
2. Run `python app.py` and use `curl http://localhost:8080/[name_of_your_end_point]` to test the endpoint. You can run the server from your favorite IDE. This will help to debug.

## Build and test the docker image

- Build a docker image on your local machine:  
```bash
docker build . -f Dockerfile -t my_image
```
- Run the docker image:
```bash
docker run -p 8080:8080 -v $GOOGLE_APPLICATION_CREDENTIALS:/creds.json -e GOOGLE_APPLICATION_CREDENTIALS=/creds.json my_image
```
- You can now test if the app is working using `curl`:
```bash
curl http://0.0.0.0/[name_of_your_end_point]
```
- (Optional) If for some reasons, you want to see what is going on inside the docker, you can start it in an interacting mode:
```bash
docker run -it -p 8080:8080 -v $GOOGLE_APPLICATION_CREDENTIALS:/creds.json -e GOOGLE_APPLICATION_CREDENTIALS=/creds.json my_image /bin/bash

```

## Deploy your app

1. Push your code. If you are set up correctly, you should push the changes in your code and it will trigger a new build. You can check the status of your build on the Google build console.
2. The build should have created a new image. You can look at it in the 'Artifacts' tab.
3. If you click on the link at the right of the image (view), you will open a new tab (container registry)  
4. You can click on 'Deploy' and follow the instructions.

If every thing goes well, you should be redirected to a page where you can retrieve the URL of the instance.
5. On your machine, you can use curl to test your app:
```bash
curl https://[your_URL].run.app/[name_of_your_end_point]... 
```

ET VOILA!





 
