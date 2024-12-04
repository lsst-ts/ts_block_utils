from typing import Any, Dict

__all__ = ["build_configuration_schema"]


def build_configuration_schema(
    block_number: int, properties: Dict[str, Dict[str, Any]]
) -> str:
    """
    Builds a configuration schema string for a given BLOCK and configurable
    properties.

    Parameters
    ----------
    block_number : int
        The BLOCK number to include in the title and description.
    properties : dict
        A dictionary where each key is a property name, and each value is a
        dictionary with keys 'description', 'type', and optionally 'default'.

    Returns
    -------
    str
        A formatted configuration schema string.
    """

    # Define the base schema with the BLOCK number
    configuration_schema = (
        "$schema: http://json-schema.org/draft-07/schema#\n"
        f"title: BLOCK-{block_number} configuration\n"
        f"description: Configuration for BLOCK-{block_number}.\n"
        "type: object\n"
        "properties:\n"
    )

    # Add each property to the schema
    for prop_name, prop_details in properties.items():
        configuration_schema += f"  {prop_name}:\n"
        configuration_schema += f'    description: {prop_details["description"]}\n'
        configuration_schema += f'    type: {prop_details["type"]}\n'
        if "default" in prop_details:
            # Add quotes around the default value if it's a string
            default_value = prop_details["default"]
            if prop_details["type"] == "string":
                default_value = f'"{default_value}"'
            configuration_schema += f"    default: {default_value}\n"

    return configuration_schema
