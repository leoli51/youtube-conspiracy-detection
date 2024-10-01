# master-thesis

Master thesis in Computer Science and Engineering at Pollimi. Topic: Conspiracy Theories, Fake News, Computational Sociology, AI/ML, Fact Checking,  

## Installation

1. Install [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) 
2. Clone this repository
3. Run `poetry install`
4. 🎉


## Running code with Google APIs

To use the google API's you need to authenticate with credentials. There are multiple way of doing it. Personally I used the gcloud CLI that provides credentials to applications when running locally. The advantage of this is that you don't need to setup, download, and manage API keys.
To setup authentication through the Gcloud CLI follow these steps:

1. Install Gcloud CLI, instructions [here](https://cloud.google.com/sdk/docs/install).
2. Setup a project in the google cloud platform.
3. Activate Youtube's API for the project.
4. Set the project as your current project in the Gcloud CLI with `gcloud config set project <project-id>`
5. Authenticate with `gcloud auth application-default login --scopes=openid,https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/youtube`.

Note: if you will need other authentication scopes you will have to add them in the `--scopes` list and reauthenticate.

Note: This took a while to figure out, [thank you](https://stackoverflow.com/questions/72526314/google-sheet-api-access-with-application-default-credentials-using-scopes-giving)! 

## Running notebooks

To run the notebooks you need to start the jupyter server in the environment. You can do this by running `poetry run jupyter notebook`.

