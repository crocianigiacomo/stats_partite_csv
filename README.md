# stats_partite_csv

Football Data Processor

Imagine you have many football match files, and you want to:

-Put them all in order

-Count goals

-See which teams score the most

-Discover exciting matches with lots of goals

This project does exactly that — automatically!

It reads football match data in JSON format, turns it into CSV files, cleans everything, and creates useful statistics.

What Does It Do?

Think of it like a smart football robot:

-It reads match files (JSON files).

-It creates folders for each league.

-It creates a CSV file for every matchday.

-It cleans and merges all matchdays into one big file.

-It calculates important statistics like:

    -Total goals scored

    -Total goals conceded

    -Matches with 3 or more total goals

-And it saves everything neatly in organized folders.

Technologies Used

This project uses powerful tools:

Python 3 – The main programming language.

Pandas – For data analysis and statistics.

JSON – To read structured football match data.

CSV – To store clean and organized tables.

OS & Glob modules – To manage files and folders automatically.

Datetime module – To convert timestamps into readable dates.

These technologies allow the program to:

-Process large amounts of match data.

-Automatically clean invalid or missing values.

-Perform real statistical calculations.

-Organize files in a scalable and structured way.

🔍 Main Features

1-JSON to CSV Conversion

The program:

-Reads match data from files like round_1.json

Extracts:

-Home team

-Away team

-Goals

-Match date

-Match status

-Skips postponed matches

-Creates one CSV file per round

2-Automatic League Organization

For each league:

-A folder is created automatically.

-Files are named clearly and consistently.

-Old files are deleted to avoid duplication.

3-Data Cleaning & Merging

The program:

-Merges all matchdays into one main league file.

-Keeps only useful columns:

-Home Team

-Away Team

-Home Goals

-Away Goals

-Calculates total goals per match.

4-Advanced Statistics Generation

It calculates:

- Matches with 3 or more total goals

- Goals scored at home

- Goals scored away

- Total goals scored

- Total goals conceded

Then it creates a ranked table sorted by most high-scoring matches.

📁 Project Structure (Example)
project_folder/
│
├── round_1.json
├── round_2.json
│
└── csv/
└── League_Name/
├── League_Name_giornata_1.csv
├── League_Name.csv
└── Statistiche_Somma_Gol.csv

How to Run

Just run:

python scrapfootball.py

Why This Project Is Powerful

Even though it looks simple, this project demonstrates:

Automated data pipelines

Data cleaning techniques

File system automation

Statistical aggregation

Structured data processing

Scalable architecture

It transforms raw football data into meaningful insights — completely automatically.

Final Summary

This project is like a smart football assistant that:

Reads match data

Organizes everything

Calculates statistics

Creates clean reports

All in one automatic system.

Simple to understand.
Powerful in execution.
Built with real data engineering concepts.
