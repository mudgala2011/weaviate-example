import pandas as pd

df = pd.read_csv("path/to/your/file/Resume.csv")

# Remove the html column
df.drop(columns=["Resume_html"], inplace=True)
df.head()
# export the new file to csv
df.to_csv("path/to/your/file/Resume_cleaned.csv", index=False)


# Note: Resumes dataset is sourced from kaggle- path = kagglehub.dataset_download("snehaanbhawal/resume-dataset")
# dataset will be loaded to your workspace in zip format, you can run a unzip and extract the contents
