import json

FILE_NAME = 'data/history.json'

def load_history_list():
    try:
        with open(FILE_NAME, 'r') as json_file:
            history_list = json.load(json_file)
        return history_list
    except FileNotFoundError:
        print(f"Error: File '{FILE_NAME}' not found. Returning an empty list.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in '{FILE_NAME}': {e}. Returning an empty list.")
        return []
    except Exception as e:
        print(f"Unexpected error loading history list from '{FILE_NAME}': {e}. Returning an empty list.")
        return []


def save_history_list(history_list):
    try:
        with open(FILE_NAME, 'w') as json_file:
            json.dump(history_list, json_file, indent=4)
        print(f"History list saved to '{FILE_NAME}'.")
    except Exception as e:
        print(f"Error saving history list to '{FILE_NAME}': {e}")


def __example():
    new_history = {
        'algorithms_name': 'A*',
        'visited_nodes': '254',
        'execute_time': '74.5',
        'steps': '64',
        'player_win': 2,
    }

    new_history1 = {
        'algorithms_name': 'BFS',
        'visited_nodes': '254',
        'execute_time': '74.5',
        'steps': '64',
        'player_win': 1,
    }

    history_list = [
        new_history,
        new_history1
    ]

    save_history_list(history_list)

    loaded_history_list = load_history_list()

    print(loaded_history_list)
    print(type(loaded_history_list))
    print(type(loaded_history_list.pop()))
