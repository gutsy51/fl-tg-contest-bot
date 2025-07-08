from os import path

import yaml


def get_config_texts(file_path: str, required_keys: set = None) -> dict:
    """Returns config`s values."""

    if not path.exists(file_path):
        raise FileNotFoundError(f'No config file found in {file_path}')

    with open(file_path, encoding='utf-8', mode='r') as f:
        config_data = yaml.safe_load(f)
        if not config_data:
            raise ValueError(f'Empty config file in {file_path}')

    texts = config_data.get('texts', {})
    if required_keys:
        missing_keys = required_keys - texts.keys()
        if missing_keys:
            raise ValueError(f'Missing keys in config.yaml: {missing_keys}')

    return texts

if __name__ == '__main__':
    print(get_config_texts('../config/config.yaml'))
