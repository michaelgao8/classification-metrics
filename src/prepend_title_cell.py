import json
import nbformat as nbf
import argparse
import sys

def add_ipynb_title(title: str, input_file: str, output_file: str, replace_first=False):
    """Add or replaces the first cell of an ipython notebook with a markdown title

    title (str): Markdown text to reside in the first cell
    input_file (str): Path to the input file or template to be modified
    output_file (str): Path to the write destination
    replace_first (bool): If true, replaces the first cell of the input_file instead of prepending
        a new cell

    CLI use example:

    python prepend_title.py -t '# New Header' -i 'Metrics Template.ipynb' -o 'my_notebook.ipynb'

    """
    # Ensure master template file won't be overwritten
    if output_file.split('/')[-1]== 'Metrics Template.ipynb':
        raise('Master Template overwrite is not permitted. Choose another output filepath')
        sys.exit('1')
    elif output_file.split('\\')[-1]== 'Metrics Template.ipynb': # ...Windows
        raise('Master Template overwrite is not permitted. Choose another output filepath')
        sys.exit('1')

    # Create Title Cell
    cell = nbf.v3.new_text_cell('markdown', title)

    # Read in input_file ipynb
    with open(input_file) as f:
        data = json.load(f)
    
    met_nb = nbf.reads(json.dumps(data), as_version=4)

    # Insert new cell at the front of the ipynb
    if replace_first:
        met_nb.get('cells')[0] = cell
    else:
        met_nb.get('cells').insert(0, cell)

    # Write out the result
    nbf.write(met_nb, output_file)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = 'Add or replace the title cell of an ipython notebook')
    parser.add_argument('--title', '-t', help='Title cell text you wish to add')
    parser.add_argument('--input', '-i', help='Path to input ipynb file')
    parser.add_argument('--output', '-o', help='Path to output ipynb file')
    parser.add_argument('--replace', '-r', help='Replace an existing title cell', action='store_true')
    args = parser.parse_args()

    add_ipynb_title(args.title, args.input, args.output, args.replace)
