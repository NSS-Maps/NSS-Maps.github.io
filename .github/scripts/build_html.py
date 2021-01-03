#!/bin/env python3
import os

ROOT_DIR = './'
MAPS_DIR = ROOT_DIR + 'maps'
TMPL_PATH = ROOT_DIR + '.github/scripts/index.tmpl.html'
INDEX_PATH = ROOT_DIR + 'index.html'


def main():
    with open(TMPL_PATH, 'r') as tmpl:
        template = tmpl.read()
    
    map_data = scan_maps_dir(MAPS_DIR)
    html_content = map_data_to_html(map_data)

    with open(INDEX_PATH, 'w') as output:
        output.write(template.format(content = html_content))


def scan_maps_dir(path):
    results = {}
    for entry in os.scandir(path):
        if not (entry.is_dir() or entry.name.endswith('.html') or entry.name.endswith('.md')):
            continue

        results[entry.name] = {
            'name': entry.name,
            'path': entry.path,
            'children': {}
        }

        if entry.is_dir():
            results[entry.name]['children'] = scan_maps_dir(entry.path)

    return results


def map_data_to_html(map_data):
    html = ''
    for name in sorted(map_data):
        entry = map_data[name]

        if entry['children']:
            html += f'''
                <section class="collection">
                    <header class="collection__header">{entry['name']}</header>
                    {map_data_to_html(entry['children'])}
                </section>
            '''
        else:
            html += f'''
                <div class="card">
                    <a href="{entry['path']}" target="_new">{entry['name']}</a>
                </div>
            '''
    return html


main()