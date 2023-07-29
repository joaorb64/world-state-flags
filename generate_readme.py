from bs4 import BeautifulSoup
import json
import re
import unicodedata
import os
import requests
import textwrap

f = open('countries+states+cities.json')
data = json.load(f)

readme_base = open("README_BASE.md").read()

with open("README.md", 'w') as outfile:
    outfile.write(readme_base)

    outfile.write("\n\n")
    outfile.write("## Stats\n\n")

    outfile.write(
        "FLAGS: "+str(len(os.popen('find out/ -type f -name \"*.png\"').readlines()))+"\n\n")

    for country in data:
        if len(country.get("states")) == 0:
            continue

        flags_found = len(
            os.popen('find out/'+country["iso2"]+'/ -type f -name \"*.png\"').readlines())
        total_flags = len(country["states"])

        states_string = ""

        for state in country.get("states"):
            flag_exists = os.path.isfile(
                f'out/{country["iso2"]}/{state.get("state_code")}.png')

            if flag_exists:
                states_string += f"<img src='out/{country['iso2']}/{state.get('state_code')}.png' width='32'/> "

            states_string += f"""{state.get('state_code')} - {state.get('name')}{' ✔️' if flag_exists else ''}"""

            states_string += "\n\n"

        outfile.write(
            f'<details>\n'
            f'<summary>{country["name"]}{(" ✔️" if flags_found == total_flags else "")} ({flags_found}/{total_flags})</summary>\n'
            f'{states_string}'
            f'</details>\n'
        )

        outfile.write("\n\n")
