import argparse
import html
import json
import os
import random
from pathlib import Path

import cowsay
import requests


class Fml:
    def __init__(self, data_file_path=None):
        if data_file_path is None:
            home_path = Path.home()
            data_file_path = home_path / ".fml_data"
        self.data_file_path = data_file_path
        self.data = dict()
        if self.data_file_exists():
            with open(data_file_path, "r") as data_file_handle:
                try:
                    self.data = json.load(data_file_handle)
                except json.decoder.JSONDecodeError:
                    pass

    def data_file_exists(self):
        return os.path.exists(self.data_file_path)

    def set_name(self, first_name, last_name) -> str:
        if first_name is None or last_name is None:
            return "First name or last name is invalid"

        if not first_name.isalpha() or not last_name.isalpha():
            return "First name and last name can just contain alphabets"

        self.update_data_file({"first_name": first_name, "last_name": last_name})
        return f"Name updated to {first_name} {last_name}!"

    def update_data_file(self, update_dict):
        self.data.update(update_dict)
        with open(self.data_file_path, "w") as data_file_handle:
            data_file_handle.write(json.dumps(self.data))

    def get_joke(self):
        if not self.data_file_exists():
            first_name = "Chuck"
            last_name = "Norris"
        else:
            data = json.load(open(self.data_file_path))
            first_name = data["first_name"]
            last_name = data["last_name"]

        url = f"http://api.icndb.com/jokes/random?firstName={first_name}&lastName={last_name}"
        try:
            icndb_response = requests.get(url)
        except requests.exceptions.ConnectionError:
            return "Oops! Looks like you are not connected yet. Unfortunately, I can't tell you a joke without " \
                   "asking my friend incdb :("
        if not 200 <= icndb_response.status_code <= 299:
            return "Oops! Something is wrong. I wasn't able to tell you a joke :/"

        return icndb_response.json().get("value").get("joke")

    def joke_with_character(self):
        characters = {
            "beavis": cowsay.beavis,
            "cheese": cowsay.cheese,
            "daemon": cowsay.daemon,
            "cow": cowsay.cow,
            "dragon": cowsay.dragon,
            "ghostbusters": cowsay.ghostbusters,
            "kitty": cowsay.kitty,
            "meow": cowsay.meow,
            "milk": cowsay.milk,
            "stegosaurus": cowsay.stegosaurus,
            "stimpy": cowsay.stimpy,
            "turkey": cowsay.turkey,
            "turtle": cowsay.turtle,
            "tux": cowsay.tux,
        }
        joke = html.unescape(self.get_joke())
        characters[random.choice(cowsay.char_names)](joke)


def main():
    parser = argparse.ArgumentParser(
        description="To see a joke on your terminal. Type fml\nTo set a custom name instead of Chuck Norris"
                    " use, fml --name <first-name> <last-name>\nExample: fml --name John Doe will use John Doe as the"
                    " character instead of Chuck Norris\nFacing an issue? or want to drop a feedback? write to me at "
                    "slash-arun@outlook.com or create an issue on github at https://github.com/slash-arun/fml/issues")
    parser.add_argument('--name', nargs=2, type=str, help="FIRST LAST")
    try:
        args = parser.parse_args()
    except argparse.ArgumentError:
        print(
            "Oops! the command could not be understood. Please type fml --help to see the usage."
        )
        return

    fml = Fml()

    if args.name:
        first_name, last_name = args.name
        print(fml.set_name(first_name, last_name))
    else:
        fml.joke_with_character()


if __name__ == '__main__':
    main()
