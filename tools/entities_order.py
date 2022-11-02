"""
Script that checks the order of the entities of the suffix group of each datatype
and lists those that are out of order.
"""

import warnings
from pathlib import Path

import yaml


def main():

    status_ok = True

    entities_order = return_entities_order()

    datatypes_schema_path = Path(__file__).parent.joinpath(
        "..", "src", "schema", "rules", "datatypes"
    )
    files_to_check = datatypes_schema_path.rglob("*.yaml")

    for file_ in files_to_check:

        print(f"Checking: {file_}")

        with open(file_, "r") as f:

            schema = yaml.safe_load(f)

            for suffix_group in schema:

                entities = list(schema[suffix_group]["entities"].keys())

                if "$ref" in entities:
                    entities.remove("$ref")

                correct_order = sorted(entities, key=lambda x: entities_order.index(x))

                if entities != correct_order:

                    status_ok = False

                    warnings.warn(
                        f"""
                    \nsuffix group {suffix_group} in {file_} is out of order:
                    - got: {entities}
                    - should be: {correct_order}
                    """
                    )

    if not status_ok:
        raise RuntimeError(
            """
        Some suffix groups have their entities out of order.
        See warnings above.
        """
        )


def return_entities_order():
    entities_order_file = Path(__file__).parent.joinpath(
        "..", "src", "schema", "rules", "entities.yaml"
    )
    with open(entities_order_file, "r") as file:
        return yaml.safe_load(file)


if __name__ == "__main__":
    main()
