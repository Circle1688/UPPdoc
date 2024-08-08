import yaml

def load_config():
    with open('config.yaml', 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data

def update_config(key, value):
    data = load_config()

    # 更新数据
    keys = key.split('.')
    current_data = data
    for k in keys[:-1]:
        current_data = current_data.setdefault(k, {})
    current_data[keys[-1]] = value

    # 写入更新后的数据
    with open('config.yaml', 'w', encoding='utf-8') as file:
        yaml.safe_dump(data, file)
