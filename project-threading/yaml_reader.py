import importlib
import yaml
from multiprocessing import Queue

class YamlPipelineExecutor():
    def __init__(self, pipeline_location):
        self._pipeline_location = pipeline_location
        self._queues = {}
        self._workers = {}


    def _load_pipeline(self):
        """Load pipeline configuration from a YAML file."""
        with open(self._pipeline_location, 'r') as f:
            self._yaml_data = yaml.safe_load(f)


    def _initialize_queues(self):
        """Initialize queues based on the YAML configuration."""
        for queue in self._yaml_data['queues']:
            self._queues[queue['name']] = Queue()


    def _initialize_workers(self):
        """
        Dynamically import worker modules/classes/functions specified in the configuration and initialize them with
        their parameters.
        """
        for worker in self._yaml_data['workers']:
            try:
                module_name = worker['module']
                class_name = worker['class']
                input_queue = worker.get('input_queue')
                output_queues = worker.get('output_queues')
                worker_name = worker['name']
                instances = worker.get('instances', 1) # 1 is a fallback parameter
                input_values = worker.get('input_values')

                # Create the initial arguments dictionary
                init_args = {}

                # Add input queue if applicable
                if input_queue:
                    init_args['input_queue'] = self._queues[input_queue]

                # Add output queues if applicable
                if output_queues:
                    init_args['output_queues'] = [self._queues[output_queue] for output_queue in output_queues]

                if input_values:
                    init_args['input_values'] = input_values

                # dynamically import the module & then load the class
                module = importlib.import_module(module_name)
                worker_class = getattr(module, class_name)

                # initialize the worker
                self._workers[worker_name] = []
                for i in range(instances):
                    self._workers[worker_name].append(worker_class(**init_args))

                print(f"Initialized worker '{worker['name']}' from {module_name}.{class_name}")
            except (ModuleNotFoundError, AttributeError) as e:
                print(f"Failed to initialize worker '{worker['name']}' from '{worker['name']}': {e}")

    def _join_workers(self):
        for worker_name in self._workers:
            for worker_thread in self._workers[worker_name]:
                worker_thread.join()

    def process_pipeline(self):
        self._load_pipeline()
        self._initialize_queues()
        self._initialize_workers()
        self._join_workers()
