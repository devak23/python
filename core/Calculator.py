import importlib
import sys
import yaml

class Calculator:
    def __init__(self, command, init_values):
        self._command = command
        self._init_values = init_values

    def run(self):
        config_file = './config/calculator.yaml'
        with open(config_file, 'r') as f:
            self._yaml_data = yaml.safe_load(f)

        if not self._yaml_data:
            raise ValueError(f"could not load file: {config_file}")

        matching_operation = next(
            (block for block in self._yaml_data['operations'] if block.get('command') == self._command), None
        )

        if not matching_operation:
            raise ValueError(f"Invalid command: {self._command} requested")

        module = importlib.import_module(matching_operation['module'])
        clazz = getattr(module, matching_operation['class'])
        instance = clazz(** {'number1': int(self._init_values[0]), 'number2': int(self._init_values[1])} )
        result = instance.execute()

        print(result)


if __name__ == '__main__':
    calculator = Calculator(sys.argv[1], sys.argv[2:])
    calculator.run()

