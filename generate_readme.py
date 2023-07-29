from bs4 import BeautifulSoup
import json
import re
import unicodedata
import os
import requests

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

        outfile.write("### "+country["name"]+"\n\n")

        flags_found = len(
            os.popen('find out/'+country["iso2"]+'/ -type f -name \"*.png\"').readlines())
        total_flags = len(country["states"])

        # states_string = ""

        # for state in [f"{'a'}{'✔️' if os.path.isfile('out/')}" for state in country.get("states")]

        outfile.write(
            f'''
                <details>
                <summary>{flags_found}/{total_flags}</summary>

                ```
                ```
                </details>
            '''
        )

        outfile.write("\n")
