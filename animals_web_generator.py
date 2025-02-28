import json
import os
from typing import Dict, List


def load_data(file_path: str) -> List[Dict]:
    """
    Loads data from a JSON file.

    Args:
        file_path (str): Path to JSON file

    Returns:
        List[Dict]: List of dictionaries containing animal data
    """
    # Create absolute path to JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_path = os.path.join(current_dir, file_path)

    with open(absolute_path, "r", encoding='utf-8') as handle:
        return json.load(handle)


def print_animal_info(animal: Dict) -> None:
    """
    Prints available information about an animal.

    Args:
        animal (Dict): Dictionary containing animal information
    """
    if "name" in animal:
        print(f"Name: {animal['name']}")
    if "characteristics" in animal and "diet" in animal["characteristics"]:
        print(f"Diet: {animal['characteristics']['diet']}")
    if "locations" in animal and animal["locations"]:
        print(f"Location: {animal['locations'][0]}")
    if "characteristics" in animal and "type" in animal["characteristics"]:
        print(f"Type: {animal['characteristics']['type']}")
    print()


def main() -> None:
    """
    Main function to load and display animal data.
    """
    try:
        animals_data = load_data("My_Zootopia/animals_data.json")
        for animal in animals_data:
            print_animal_info(animal)
    except FileNotFoundError:
        print("Error: File 'animals_data.json' not found.")
        print("Please make sure the file is in the same directory as the script.")
    except json.JSONDecodeError:
        print("Error: Could not decode JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
