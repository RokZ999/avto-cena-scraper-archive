import time

from schedule import every, repeat, run_pending

from Backend.logger.log_config import log
from main import main

def main_with_logging() -> None:
    """Execute main function with comprehensive logging."""
    try:
        log.info("Starting main function.")
        main()
        log.info("Main function completed successfully.")
    except Exception as e:
        log.error(f"Error occurred in main function: {e}")

@repeat(every().day.at("21:24"))
def scheduled_task() -> None:
    """Daily scheduled task that runs the scraper at 21:24."""
    main_with_logging()

if __name__ == "__main__":
    log.info("Scheduler started.")
    try:
        while True:
            run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        log.info("Scheduler stopped.")
    except Exception as e:
        log.error(f"Scheduler encountered an error: {e}")
