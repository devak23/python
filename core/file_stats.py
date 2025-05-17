import datetime
import os

from utils.logging_functions import logger


def main(file_path: str) -> None:
    try:
        file_stat = os.stat(file_path)
        creation_time = file_stat.st_ctime

        logger.info(f"creation_time of the file = {creation_time}")
        logger.info(f"delta: {datetime.timedelta(seconds=creation_time)}")
    except FileNotFoundError:
        logger.error("File not found")
    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    main('/home/abhay/Downloads/demo/src/main/java/com/example/demo/DemoApplication.java')