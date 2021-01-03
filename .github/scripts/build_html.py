#!/bin/env python3
import os
import markdown2


ROOT_DIR = "./"
MAPS_DIR = ROOT_DIR + "maps"
TMPL_PATH = ROOT_DIR + ".github/scripts/index.tmpl.html"
INDEX_PATH = ROOT_DIR + "index.html"


def main():
    with open(TMPL_PATH, "r") as tmpl:
        template = tmpl.read()

    html_content = map_data_to_html(scan_maps_dir(MAPS_DIR))

    with open(INDEX_PATH, "w") as output:
        output.write(template.format(content=html_content))


def scan_maps_dir(path):
    results = {}
    markdown_entries = []

    for entry in os.scandir(path):
        if entry.name.endswith(".md"):
            markdown_entries.append(entry)
            continue

        if not (entry.is_dir() or entry.name.endswith(".html")):
            continue

        results[entry.name] = {
            "name": os.path.splitext(entry.name)[0],
            "path": entry.path,
            "description": "",
            "children": scan_maps_dir(entry.path) if entry.is_dir() else {},
        }

    attach_descriptions(markdown_entries, results)
    return results


def attach_descriptions(markdown_entries, map_entries):
    for md_entry in markdown_entries:
        base_name = os.path.splitext(md_entry.name)[0]
        html_name = base_name + ".html"

        if base_name in map_entries:
            entry_key = base_name
        elif html_name in map_entries:
            entry_key = html_name
        else:
            continue

        with open(ROOT_DIR + md_entry.path, "r") as md_input:
            map_entries[entry_key]["description"] = md_input.read()


def map_data_to_html(map_entries):
    html = ""

    for key in sorted(map_entries):
        entry = map_entries[key]

        if entry["children"]:
            html += f"""
                <section class="collection">
                    <header class="collection__header">{entry['name']}</header>
                    {description_html(entry)}
                    {map_data_to_html(entry['children'])}
                </section>"""
        else:
            html += f"""
                <div class="card">
                    <a href="{entry['path']}" target="_new">{entry['name']}</a>
                    {description_html(entry)}
                </div>"""

    return html


def description_html(entry):
    if not entry["description"]:
        return ""

    return f"""
        <div class="description"> 
            {markdown2.markdown(entry["description"])} 
        </div>"""


main()