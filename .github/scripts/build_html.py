#!/bin/env python3
import os
import markdown2

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
    markdown_entries = []

    for entry in os.scandir(path):
        if not (entry.is_dir() or entry.name.endswith('.html') or entry.name.endswith('.md')):
            continue

        if entry.name.endswith('.md'):
            markdown_entries.append(entry)
            continue

        results[entry.name] = {
            'name': entry.name,
            'path': entry.path,
            'description': '',
            'children': {}
        }

        if entry.is_dir():
            results[entry.name]['children'] = scan_maps_dir(entry.path)

    for md_entry in markdown_entries:
        base_name = md_entry.name[:-3]
        html_name = base_name + '.html'

        if base_name in results or html_name in results:
            with open(ROOT_DIR + md_entry.path, 'r') as md_input:
                description = md_input.read()
            
            if base_name in results:
                results[base_name]['description'] = description
            else:
                results[html_name]['description'] = description

    return results


def map_data_to_html(map_data):
    html = ''
    for name in sorted(map_data):
        entry = map_data[name]

        if entry['children']:
            html += f'''
                <section class="collection">
                    <header class="collection__header">{entry['name']}</header>
                    {entry['description'] and f"""
                        <div class="description">
                            {markdown2.markdown(entry['description'])}
                        </div>"""}
                    {map_data_to_html(entry['children'])}
                </section>
            '''
        else:
            html += f'''
                <div class="card">
                    <a href="{entry['path']}" target="_new">{entry['name']}</a>
                    {entry['description'] and f"""
                        <div class="description">
                            {markdown2.markdown(entry['description'])}
                        </div>"""}
                </div>
            '''
    return html


main()