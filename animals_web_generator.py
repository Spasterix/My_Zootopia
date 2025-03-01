import json
import os
from typing import Dict, List, Tuple


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


def process_animals_to_html() -> Tuple[bool, str]:
    """
    Processes animal data and generates HTML file.

    Returns:
        Tuple[bool, str]: Success status and error message if any
    """
    try:
        # Load animal data
        animals_data = load_data("animals_data.json")

        # Generate animals info string
        animals_info = serialize_animals_list(animals_data)

        # Read template and replace placeholder
        template_content = read_template("animals_template.html")
        final_html = template_content.replace("__REPLACE_ANIMALS_INFO__", animals_info)

        # Write to output file
        write_html(final_html, "animals.html")
        return True, ""

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
    success, error_message = process_animals_to_html()
    if not success:
        print(error_message)
    else:
        print("HTML file successfully generated as 'animals.html'")


if __name__ == "__main__":
    main()
