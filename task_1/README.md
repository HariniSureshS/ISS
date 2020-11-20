# Omdena-ISS Task 1 - Data Tabularization

**Task Manager**: Jianna Park

**General Goal**: Convert raw text data into machine-readable tabular format.

## Sub-Goal 1

**Description**: Convert given ISS case notes and welfare assessment reports into an excel sheet, using parameters given in “ISS-AI data points.xlsx” and “ISS Manual” templates (pages 22-24 and 28). All participants can add columns in places they see fit.

**Purpose**: Consolidate multiple files into a single consistent source. Gain insight on data distribution/sparsity.

**Timeline**: Weeks 1 and 2

**Note**: I wanted to see what we can do with the data given in the resources folder while we wait for more information. Acknowledging we haven’t yet decided on what to prioritize in our project, this task may or may not prove to be useful in the end. If you have strong recommendations, please feel free to give feedback or advice on how best to proceed with this task--I’d appreciate your input on naming convention, formatting, etc.

**Conclusion**: We ended up not using this data.

**Links**

- [Data Table](https://docs.google.com/spreadsheets/d/1JL6_FEGT_2-SIMQczyBCSBPNxSJjbfgOcRSYGsRuHh0/edit?usp=sharing)
- [Task 1 Notes](https://docs.google.com/document/d/1bKHEpK7X469wHbzy5VKq25iWe2zO7xPVbMWvjDi5aSQ/edit?usp=sharing)


## Sub-Goal 2

**Description**: Using the Data Table, manually create risk score feature table.

**Purpose**: Understand what kinds of features or information we want to extract for a risk score predictor model.

**Timeline**: Week 3

**Conclusion**: We ended up not using this data.

**Links**

- [Risk Score Feature Table](https://docs.google.com/spreadsheets/d/1uGgen4JpekoohF4WcU77l3dC_PXkV6UTpHdAPTcWrr8/edit#gid=0)


## Sub-Goal 3

**Description**: Manually give risk scores to all compiled cases.

**Purpose**: Train a risk score predictor model.

**Note**: Concluding that highly specific feature extraction of Sub-Goal 2 would not be easily automated, we decided to take a different approach. Three people will each give a risk score to each case based on their personal interpretation of the case, as well as keeping in mind general factors that affect the child's or client's welfare (physical, psychological, emotional, social/environmental, financial and interpersonal factors). We then average the scores into a final risk score, which will be used in model training.

**Timeline**: Week 4 - present

**Conclusion**: We're currently using this data in training different risk score models.

**Links**

- [Manual Risk Score Table](https://docs.google.com/spreadsheets/d/1_7YiZz0LdQn_ns-74dlZScZ25YcfkthLU11oIJTDW_k/edit?usp=drive_web&ouid=103236836343707553067)
