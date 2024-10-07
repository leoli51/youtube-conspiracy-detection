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

## Papers Summaries

### "It is just a flu": Assessing the Effect of watch history on YouTube's Pseudoscientific Video Recommendations.

*Papadamou, K., Zannettou, S., Blackburn, J., Cristofaro, E. D., Stringhini, G., & Sirivianos, M. (2022). “It Is Just a Flu”: Assessing the Effect of Watch History on YouTube’s Pseudoscientific Video Recommendations. Proceedings of the International AAAI Conference on Web and Social Media, 16(1), 723-734. https://doi.org/10.1609/icwsm.v16i1.19329*

Notes: requested access to dataset used in the study at https://zenodo.org/records/4769731

**Research questions**:
- RQ1: Can we effectively detect and characterize pseudoscientific content on YouTube?
- RQ2: What is the proportion of pseudoscientific content on the homepage of a YouTube user, in search results, and the video recommendations section of YouTube? How are these proportions affected by the user’s watch history?

**Summary**:

- **Groundtruth dataset**: crowdsourced (Appen) groundtruth dataset. 1,197 science, 1,325 pseudoscience, and 3,212 irrelevant videos. Due to limited agreement scores, 600 videos have been manually annotated by the authors to test the groundtruth dataset quality.
- **Classifier**: Input: snippet, video tags, transcript, 200 top comments. Inputs are embedded using fine-tuned FastText models for each input feature (?). Each input feature is transformed into a 300-dimensional embeddings vector. Model is a four-layer fully connected network with ReLu activations. The layers sizes are: 256, 128, 64, and 32. Thi results in `(1200 (input) + 1 (bias)) * 256 + (256 + 1 (bias)) * 128 + (128 + 1 (bias)) * 64 + (64 + 1 (bias)) * 32 + (32 + 1 (bias)) * 2 (output) = 350754 parameters`. The model is trained with dropout technique. Threshold for pseudoscientific label 0.7 (🤔 in the dataset the pseudoscience videos are 0.3 of the total). Accuracy 0.79, better than BERT based model (same but BERT instead of FastText), SVM, and Random Forest.
- **Analysis of Homepage, Search, and Recommendations**: they study the amount of misinformation videos in these three environments. They use three user profiles with a controlled watch history: a user interested in scientific content, a user interested in pseudoscientific content, and a user with interests in both. Furthermore they also perform the experiments with a non-logged in user and the Data API.

**Findings**:
- YouTube targets specific misinformation topics in its policies: there were less/no misinformation videos related to Covid.
- Watch history affects suggested videos.
- Statistically insignificant difference between results of non-logged in user (browser) and Data API.