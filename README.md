# Airline Operations & Passenger Intelligence System
**Gruppe 7 - WP_HubaBubba_Projekt**

##  Project Overview
This project is an End-to-End Data Pipeline designed to analyze global airline datasets. It automates the process of fetching raw data from Kaggle, cleaning and transforming it into a structured SQLite database, and visualizing key business insights through an interactive Web Dashboard.

##  Software Architecture
The project follows a modular **Model-View-Controller (MVC)** inspired architecture to ensure clean separation of concerns:

- **Backend:** Centralized configuration for database paths and table schemas.
- **ETL (Extract, Transform, Load):** Automated data ingestion from Kaggle and pre-processing.
- **Frontend:** Interactive dashboard built with Dash and Plotly for business intelligence.



---

##  Getting Started

### 1. Prerequisites
Ensure you have Python 3.10+ installed. You will also need a Kaggle account for the automated download.

### 2. Installation
Clone the project and install the required dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt




