# Population Health Leaders Data Collection

## Project Overview

This project aims to systematically collect and compile information on population health leaders across the United States healthcare landscape. The focus is on identifying key individuals in hospitals, health systems, health plans, and provider groups such as Accountable Care Organizations (ACOs) and Clinically Integrated Networks (CINs) who are driving population health initiatives.

### Purpose:
The primary goal is to create a comprehensive database of population health leaders, which can be valuable for:
- Networking and collaboration in the healthcare industry
- Identifying trends in population health leadership
- Supporting research on population health management strategies
- Facilitating outreach for conferences, workshops, or collaborative projects

### Methodology:
1. **Data Sources**: The project utilizes a curated list of acute care hospitals as a starting point (stored in `AcuteHospitalList.csv`).
2. **Web Scraping**: For each hospital, the system performs targeted web searches to identify relevant information about population health leaders.
3. **AI-Powered Analysis**: Leveraging Google's Gemini 1.5 AI model, the project processes search results to extract and validate information about population health leaders.
4. **Data Cleaning**: The collected data undergoes cleaning and standardization to ensure consistency and accuracy.
5. **Continuous Updates**: The process is designed to run incrementally, allowing for regular updates and expansion of the database.

### Key Information Collected:
For each identified population health leader, the project aims to collect:
- Full Name
- Job Title
- Organization
- Email Address (when publicly available)
- LinkedIn Profile Link

### Challenges and Considerations:
- Ensuring data accuracy and currency, given the dynamic nature of job positions
- Respecting privacy and data protection regulations
- Managing API rate limits and optimizing data collection efficiency
- Handling variations in how population health roles are titled across different organizations

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Collection Process](#data-collection-process)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

To set up this project, follow these steps:

```bash
# Clone the repository
git clone https://github.com/yourusername/population-health-leaders-data.git
cd population-health-leaders-data

# Install required Python packages
pip install pandas google-generativeai requests ratelimit
```

## Usage

To run the data collection script:

```bash
python main.py
```

This will start the process of collecting data on population health leaders based on the list of hospitals in `AcuteHospitalList.csv`.

## Project Structure

- `main.py`: The main script that orchestrates the data collection process.
- `utils/`:
  - `accessing_web.py`: Handles web searches using Google Custom Search API.
  - `gemini15.py`: Interacts with Google's Gemini 1.5 AI model for data processing.
  - `prompts.py`: Contains prompts and utilities for AI interactions and web scraping.
- `AcuteHospitalList.csv`: Input file containing the list of hospitals to search.
- `HealthPopLeadersLinkedIn.Rmd`: R Markdown file for data analysis and logging.

## Data Collection Process

1. Read the list of hospitals from `AcuteHospitalList.csv`.
2. For each hospital, perform a web search for population health leaders.
3. Process the top 3 search results using Google's Gemini 1.5 AI model.
4. Clean and extract relevant information about population health leaders.
5. Compile the results into a CSV file (`streaming.csv`) and Excel file (`output.xlsx`).
6. 
## Features

- **Automated Web Searching**: Utilizes Google Custom Search API to find relevant information on population health leaders for each hospital.

- **AI-Powered Content Processing**: Leverages Google's Gemini 1.5 AI model to extract and analyze information about population health leaders from web content.

- **Efficient Data Collection**: Implements concurrent processing and rate limiting to optimize data gathering while respecting API usage restrictions.

- **Robust Data Handling**: 
  - Incremental saving to prevent data loss
  - Generates both CSV and Excel output files
  - Implements data validation to ensure quality and relevance

- **Flexible and Scalable**: 
  - Customizable search parameters
  - Designed to handle large datasets of healthcare organizations
  - Easily extendable to include additional data sources or criteria

- **Intelligent Content Cleaning**: Uses Jina AI API for initial web content cleaning, with fallback mechanisms for reliability.

- **Comprehensive Error Handling and Logging**: Manages API failures and network issues, with detailed logging for easy monitoring and debugging.
