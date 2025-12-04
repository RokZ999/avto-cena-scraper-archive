# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a car data scraping application that collects vehicle listings from two Slovenian automotive websites: avto.net and doberavto.si. The scraped data is stored in MongoDB with VIN numbers and other vehicle details.

## Architecture

The application follows a modular pipeline architecture with distinct operations:

### Main Entry Points
- `main.py` - Runs both scrapers sequentially
- `main_scheduled.py` - Scheduler that runs the main function daily at 21:24

### Scraper Architecture
Both scrapers follow a similar multi-stage pipeline:

**avto.net scraper** (Backend/scraper/avto_net_scraper/):
1. `operation01_car_pages_url_collector_v2.py` - Collects car listing page URLs
2. `operation02_car_direct_urls_collector_v2.py` - Extracts individual car URLs
3. `operation03_car_direct_urls_processor_v2.py` - Processes car URLs 
4. `operation04_car_data_extractor.py` - Extracts car data from pages
5. `operation05_save_data_db.py` - Saves data to MongoDB
6. `operation06_stat.py` - Generates statistics

**doberavto.si scraper** (Backend/scraper/dober_avto_scraper/):
- Single-file implementation that fetches data via API calls
- Uses threaded processing for VIN extraction from both API and HTML scraping
- Includes comprehensive data cleaning and filtering

### Core Components

**Database Layer** (Backend/db/):
- `MongoConnectionBuilder.py` - Builder pattern for MongoDB connections
- `MongoConnectionHandler.py` - Connection management with environment variables
- `MongoOperationHandler.py` - Database operations

**Utilities** (Backend/scraper/utils/):
- `api_request_processor.py` - HTTP request handling
- `curl_imp_proccessor.py` - curl-impersonate for advanced scraping
- `selenium_driverless_helpers.py` - Browser automation
- `lxml_processor.py` - HTML parsing with XPath
- `async_processor.py` - Asynchronous operations
- `decorators.py` - Timing and logging decorators

**Browser Impersonation**:
- Uses curl-impersonate binaries in `utils/curlimp/` for both Windows and Linux
- Chrome and Safari user-agent configurations for anti-detection

## Environment Configuration

Required environment variables:
- `MONGO_URI` - MongoDB connection string
- `DB_NAME` - Database name
- `DOBER_AVTO_PROD_DB` - Collection name for doberavto.si data
- `SCRAPER_STAT_DB` - Collection name for statistics

## Running the Application

### Local Development
```bash
# Install dependencies
pip install schedule==1.2.0 lxml==5.1.0 pymongo==4.6.3 python-dotenv==1.0.1 requests==2.31.0 aiohttp==3.9.5

# Run once
python main.py

# Run with scheduler
python main_scheduled.py
```

### Docker
```bash
# Build image
docker build -t avto-scraper .

# Run container
docker run avto-scraper
```

### Devbox
```bash
# Initialize environment
devbox shell

# Run application
python main.py
```

## Data Flow

1. **avto.net**: Multi-stage scraping with URL collection → individual page processing → data extraction → MongoDB storage
2. **doberavto.si**: API-first approach with VIN enrichment through secondary API calls and HTML scraping fallback
3. Both scrapers generate statistics stored in a separate MongoDB collection
4. Data includes comprehensive vehicle information with mandatory VIN numbers for final dataset

## Key Features

- **Anti-detection**: curl-impersonate, user-agent rotation, request throttling
- **Resilient scraping**: Threaded processing, error handling, retry mechanisms
- **Data validation**: VIN number verification, field filtering, datetime stamping
- **Monitoring**: Comprehensive logging, execution statistics, performance tracking