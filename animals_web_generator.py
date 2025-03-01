import json
import os
from typing import Dict, List, Tuple, Set


def load_data(file_path: str) -> List[Dict]:
    """
    Loads data from a JSON file.

    Args:
        file_path (str): Path to JSON file

    Returns:
        List[Dict]: List of dictionaries containing animal data
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_path = os.path.join(current_dir, file_path)

    with open(absolute_path, "r", encoding='utf-8') as handle:
        return json.load(handle)


def serialize_animal(animal: Dict) -> str:
    """
    Serializes a single animal object to HTML format.

    Args:
        animal (Dict): Dictionary containing animal information

    Returns:
        str: HTML formatted string for a single animal
    """
    output = '<li class="cards__item">\n'

    if "name" in animal:
        output += f'    <div class="card__title">{animal["name"]}</div>\n'

    output += '    <div class="card__text">\n'
    output += '        <ul class="animal__details">\n'

    # Check if characteristics exists
    if "characteristics" in animal:
        chars = animal["characteristics"]

        # Diet information
        if "diet" in chars:
            output += f'            <li class="detail__item"><strong>Diet:</strong> {chars["diet"]}</li>\n'

        # Location information
        if "locations" in animal and animal["locations"]:
            output += f'            <li class="detail__item"><strong>Location:</strong> {animal["locations"][0]}</li>\n'

        # Type information
        if "type" in chars:
            output += f'            <li class="detail__item"><strong>Type:</strong> {chars["type"]}</li>\n'

        # Skin type information
        if "skin_type" in chars:
            output += f'            <li class="detail__item"><strong>Skin Type:</strong> {chars["skin_type"]}</li>\n'

        # Lifespan information
        if "lifespan" in chars:
            output += f'            <li class="detail__item"><strong>Lifespan:</strong> {chars["lifespan"]}</li>\n'

    output += '        </ul>\n'
    output += '    </div>\n'
    output += '</li>\n'
    return output


def serialize_animals_list(animals: List[Dict]) -> str:
    """
    Serializes a list of animals to HTML format.

    Args:
        animals (List[Dict]): List of animal dictionaries

    Returns:
        str: Complete HTML formatted string for all animals
    """
    return "".join(serialize_animal(animal) for animal in animals)


def read_template(template_path: str) -> str:
    """
    Reads HTML template file.

    Args:
        template_path (str): Path to template file

    Returns:
        str: Content of template file
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_path = os.path.join(current_dir, template_path)

    with open(absolute_path, "r", encoding='utf-8') as file:
        return file.read()


def write_html(html_content: str, output_path: str) -> None:
    """
    Writes HTML content to file.

    Args:
        html_content (str): HTML content to write
        output_path (str): Path to output file
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_path = os.path.join(current_dir, output_path)

    with open(absolute_path, "w", encoding='utf-8') as file:
        file.write(html_content)


def get_unique_values(animals: List[Dict], field: str) -> Set[str]:
    """
    Gets all unique values for a given field from the animals data.

    Args:
        animals (List[Dict]): List of animal dictionaries
        field (str): Field to get unique values for

    Returns:
        Set[str]: Set of unique values
    """
    values = set()
    for animal in animals:
        if "characteristics" in animal and field in animal["characteristics"]:
            values.add(animal["characteristics"][field])
        elif field == "location" and "locations" in animal and animal["locations"]:
            values.add(animal["locations"][0])
    return values


def filter_animals(animals: List[Dict], filters: Dict[str, str]) -> List[Dict]:
    """
    Filters animals list by multiple criteria.

    Args:
        animals (List[Dict]): List of animal dictionaries
        filters (Dict[str, str]): Dictionary of field:value pairs to filter by

    Returns:
        List[Dict]: Filtered list of animals
    """
    filtered_animals = animals
    for field, value in filters.items():
        if value == "all":
            continue

        if field == "location":
            filtered_animals = [
                animal for animal in filtered_animals
                if "locations" in animal
                   and animal["locations"]
                   and animal["locations"][0] == value
            ]
        else:
            filtered_animals = [
                animal for animal in filtered_animals
                if "characteristics" in animal
                   and field in animal["characteristics"]
                   and animal["characteristics"][field] == value
            ]

    return filtered_animals


def display_filter_menu(animals: List[Dict]) -> Dict[str, str]:
    """
    Displays filter options and gets user selections.

    Args:
        animals (List[Dict]): List of animal dictionaries

    Returns:
        Dict[str, str]: Dictionary of selected filters
    """
    filter_fields = {
        1: ("skin_type", "Skin Type"),
        2: ("diet", "Diet"),
        3: ("type", "Type"),
        4: ("location", "Location")
    }

    filters = {}
    print("\nFilter options:")
    for num, (field, display_name) in filter_fields.items():
        print(f"{num}. Filter by {display_name}")
    print("0. Done selecting filters")

    while True:
        try:
            choice = int(input("\nSelect a filter option (0 to finish): "))

            if choice == 0:
                break

            if choice not in filter_fields:
                print("Invalid choice. Please try again.")
                continue

            field, display_name = filter_fields[choice]

            # Get unique values for selected field
            values = get_unique_values(animals, field)
            print(f"\nAvailable {display_name} values:")
            sorted_values = sorted(values)
            for i, value in enumerate(sorted_values, 1):
                print(f"{i}. {value}")
            print("0. Show all")

            # Get user's value choice
            while True:
                try:
                    value_choice = int(input(f"\nSelect {display_name}: "))
                    if value_choice == 0:
                        filters[field] = "all"
                        break
                    if 1 <= value_choice <= len(sorted_values):
                        filters[field] = sorted_values[value_choice - 1]
                        break
                    print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")

        except ValueError:
            print("Please enter a valid number.")

    return filters


def process_animals_to_html() -> Tuple[bool, str]:
    """
    Processes animal data and generates HTML file.

    Returns:
        Tuple[bool, str]: Success status and error message if any
    """
    try:
        # Load animal data
        animals_data = load_data("animals_data.json")

        # Get filter selections from user
        filters = display_filter_menu(animals_data)

        # Apply filters
        if filters:
            animals_data = filter_animals(animals_data, filters)
            if not animals_data:
                return False, "No animals found matching the selected filters"

        # Generate animals info string
        animals_info = serialize_animals_list(animals_data)

        # Read template and replace placeholder
        template_content = read_template("animals_template.html")
        final_html = template_content.replace("__REPLACE_ANIMALS_INFO__", animals_info)

        # Write to output file
        write_html(final_html, "animals.html")

        # Prepare success message
        filter_msg = ", ".join(f"{k}: {v}" for k, v in filters.items() if v != "all")
        return True, f"Generated HTML for {len(animals_data)} animals" + \
                     (f" with filters: {filter_msg}" if filter_msg else "")

    except FileNotFoundError as e:
        return False, f"Error: File not found - {str(e)}"
    except json.JSONDecodeError:
        return False, "Error: Could not decode JSON file"
    except Exception as e:
        return False, f"An unexpected error occurred: {str(e)}"


def main() -> None:
    """
    Main function to generate HTML file from animal data.
    """
    success, message = process_animals_to_html()
    print(f"\n{message}")


if __name__ == "__main__":
    main()
