import logging

# Configure the logger
logger = logging.getLogger("asynchronous")
logger.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)

# Prevent propagation to the root logger (avoid duplicate logs)
logger.propoagate = False

# Package-level logger exposed globally
# Import modules can directly access it as `asyncronous.log`
__all__ = ["logger"]
