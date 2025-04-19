import time
from utils.logging_functions import logger
from yaml_reader import YamlPipelineExecutor


def main():
    scrapper_start_time = time.time()
    yaml_pipeline_executor = YamlPipelineExecutor(pipeline_location='./pipelines/wiki-yahoo-scrapper-pipeline.yaml')
    yaml_pipeline_executor.process_pipeline()


    logger.info(f"Finished. Extracting price took {time.time() - scrapper_start_time} seconds")

if __name__ == "__main__":
    main()

