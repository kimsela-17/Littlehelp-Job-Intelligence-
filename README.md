# LittleHelp Job Intelligence

**A machine learning-based job recommendation system and interactive dashboard for the Cambodian labor market.**

LittleHelp Job Intelligence helps job seekers — including fresh graduates and returnees — find relevant employment opportunities by combining text-based recommendation models (Bag-of-Words, TF-IDF, and Sentence-BERT) with an interactive dashboard that visualizes labor market trends collected from major Cambodian job portals.
---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Frontend Setup](#frontend-setup)
  - [Backend Setup](#backend-setup)
  - [GPU Acceleration (Optional)](#gpu-acceleration-optional)
- [Data Pipeline](#data-pipeline)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Team](#team)
- [License](#license)

---

## Overview

Job seekers in Cambodia, particularly fresh graduates and workers returning from abroad, often struggle to find employment opportunities that match their skills, education, and experience across scattered job portals. This project addresses that gap by:

1. **Collecting** job postings from major Cambodian job portals (CamHR, BongThom, Khmer24, KhmerOnline) via web scraping.
2. **Cleaning and engineering features** from the raw data (education level, province grouping, returnee eligibility, skill counts, etc.).
3. **Analyzing** labor market trends through exploratory data analysis (salary distribution, education requirements, regional job availability).
4. **Recommending** jobs to users using three text-matching approaches — BoW, TF-IDF, and SBERT — ranked by relevance.
5. **Visualizing** all of the above through an interactive web dashboard with a dedicated, simplified view for returnees.

## Features

- **Job Recommendation Engine** — match user profiles to job postings using BoW, TF-IDF, or SBERT similarity scoring
- **Interactive Dashboard** — explore job market trends by province, industry, salary, and education level
- **Returnee-Friendly Interface** — simplified job search experience for users with limited formal education or prior work experience


## Project Structure

```
.
├── EDA/                    # Exploratory data analysis notebooks and generated charts
├── backend/                 # FastAPI application
│   ├── data/                 # Processed datasets used by the API
│   ├── App.py                 # FastAPI entry point
│   ├── filter_data.py          # Filtering logic (e.g., province, education, salary)
│   ├── recommend.py            # Recommendation logic (BoW / TF-IDF / SBERT)
│   ├── train_model.py          # Model training script
│   └── requirements.txt
├── data-pipeline/            # Web scraping and data preparation
│   ├── crawler.py              # Scrapes job postings from job portals
│   ├── cleaner.py               # Cleans and validates raw data
│   ├── database.py              # Database read/write utilities
│   └── pipeline_runner.py        # Orchestrates the full pipeline end-to-end
├── frontend/                  # React + Vite application
│   ├── public/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── .gitignore
└── README.md
```

## Tech Stack

| Layer                  | Technology                                         |
|-------------------------|-----------------------------------------------------|
| Backend                  | Python, FastAPI                                      |
| Frontend                 | React, Vite, Tailwind CSS                             |
| Data Collection          | Selenium, BeautifulSoup4, Scrapy                       |
| Data Analysis            | Pandas, Matplotlib, Seaborn                            |
| Recommendation Models    | Bag-of-Words, TF-IDF, Sentence-BERT (SBERT)             |
| ML Acceleration (optional)| PyTorch with CUDA                                       |

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- pip / virtualenv (or conda)
- Git
- (Optional) An NVIDIA GPU with CUDA support, for faster model training

### Clone the Repository

```bash
git clone https://github.com/Radayou07/Job_Recommendation_system.git
cd Job_Recommendation_system
```

### Frontend Setup

```bash
cd frontend
npm install        # make sure Node.js is installed on your system
npm run dev         # run the development server
```

The dashboard will be available at `http://localhost:5173` by default (Vite's default port).

### Backend Setup

Open a new terminal from the project root:

```bash
cd backend
pip install -r requirements.txt
python App.py       # run the API server
```

By default, the API will be available at `http://localhost:8000`.

> **Note:** Make sure the backend server is running before using the dashboard, since the frontend fetches recommendation and job market data from the API.

### GPU Acceleration (Optional)

If you have an NVIDIA GPU with CUDA support, install the CUDA-enabled build of PyTorch instead of the default CPU-only version for significantly faster model training:

```bash
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu124
```

Training (e.g., the SBERT-based recommendation model via `train_model.py`) will run noticeably faster on a CUDA-enabled GPU compared to CPU-only execution.

## Data Pipeline

The `data-pipeline/` directory contains the scripts used to collect and prepare job posting data:

| Script                 | Purpose                                                            |
|--------------------------|--------------------------------------------------------------------|
| `crawler.py`              | Scrapes job postings from CamHR, BongThom, Khmer24, and KhmerOnline |
| `cleaner.py`               | Cleans and validates the scraped data (missing values, duplicates) |
| `database.py`              | Handles reading/writing the processed dataset                       |
| `pipeline_runner.py`        | Runs the full pipeline end-to-end (crawl → clean → store)             |

### Usage

```bash
cd data-pipeline
pip install -r requirements.txt
python pipeline_runner.py
```

This produces the cleaned, feature-enriched dataset used by `backend/` and `EDA/`.

## Exploratory Data Analysis

The `EDA/` directory contains the notebooks and exported charts used to analyze trends in the Cambodian labor market, including:

- Salary distribution by province and education level
- Job type and category breakdowns
- Skill demand analysis
- Job accessibility for returnees with limited education or experience


## License

This project is for academic purposes as part of a mini-project submission.
