# Car Scraper Application

> **⚠️ DISCLAIMER:** This project is archived and likely no longer functional. The target websites (avto.net and doberavto.si) have probably updated their anti-scraping measures, changed their HTML structure, or implemented new protections since this code was written. This repository is provided for educational and reference purposes only.

A Python application that scrapes car listings from Slovenian automotive websites (avto.net and doberavto.si) and stores the data in MongoDB.

## Features

- **Multi-site scraping**: Supports both avto.net and doberavto.si
- **VIN extraction**: Ensures all collected cars have valid VIN numbers
- **Anti-detection**: Uses curl-impersonate and browser user-agent rotation
- **Scheduled execution**: Daily automated runs at configurable times
- **MongoDB storage**: Structured data storage with statistics tracking
- **Comprehensive logging**: Detailed operation logs and error tracking

## Prerequisites

- Python 3.12+
- MongoDB instance (local or cloud)
- Required system dependencies (curl, build tools)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd avto-cena-scraper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual configuration values
   ```

4. **Configure MongoDB connection**
   Update the `.env` file with your MongoDB credentials:
   ```env
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
   DB_NAME=your-database-name
   ```

## Usage

### Run Once
```bash
python main.py
```

### Run with Scheduler
```bash
python main_scheduled.py
```

### Docker
```bash
# Build image
docker build -t avto-scraper .

# Run container
docker run --env-file .env avto-scraper
```

### Devbox (Development)
```bash
devbox shell
python main.py
```

## Configuration

All configuration is done through environment variables in `.env`:

- `MONGO_URI`: MongoDB connection string
- `DB_NAME`: Database name
- `THREAD_COUNT`: Number of concurrent threads (default: 30)
- `AVTO_NET_PROD_DB`: Collection for avto.net data
- `DOBER_AVTO_PROD_DB`: Collection for doberavto.si data
- `SCRAPER_STAT_DB`: Collection for scraping statistics

## Project Structure

```
Backend/
├── db/                     # Database connection and operations
├── logger/                 # Logging configuration
└── scraper/
    ├── avto_net_scraper/   # avto.net scraping pipeline
    ├── dober_avto_scraper/ # doberavto.si scraper
    └── utils/              # Common utilities and helpers
```

## Data Output

Each scraper collects:
- Vehicle make, model, and specifications
- Price and listing details
- VIN numbers (mandatory for final dataset)
- Listing URLs and metadata
- Timestamp of collection

Statistics are tracked including:
- Total listings found
- Successfully processed listings
- Items with valid VIN numbers
- Processing time and performance metrics

## Security

- Environment variables for sensitive data
- No hardcoded credentials in source code
- Comprehensive `.gitignore` for security files
- Anti-detection measures for responsible scraping

## License

This project is for educational and research purposes only. Please respect the terms of service of the target websites.