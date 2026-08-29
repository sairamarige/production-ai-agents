import logging

logging.basicConfig(
    level=logging.DEBUG,  # show everything, DEBUG and above
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log"),
    ],
)

logger = logging.getLogger(__name__)


def demonstrate_levels():
   
    logger.debug("This is a DEBUG message - detailed internal info for developers")
    logger.info("This is an INFO message - normal application event")
    logger.warning("This is a WARNING message - something unexpected, but not fatal")
    logger.error("This is an ERROR message - an operation failed")
    logger.critical("This is a CRITICAL message - the app may be unable to continue")


def demonstrate_exception_logging():
    try:
        result = 10 / 0
    except Exception:
        logger.exception("Calculation failed")


if __name__ == "__main__":
    demonstrate_levels()
    demonstrate_exception_logging()
    logger.info("logging_demo.py finished running - check the console and app.log")