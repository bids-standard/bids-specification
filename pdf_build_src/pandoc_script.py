"""Use the pandoc library as a final step to build the pdf.

This is done once the duplicate src directory is processed.
"""
import os
import subprocess

def correct_table(table):
    """Compute the max number of characters and dashes for each column and create the corrected table"""
    import numpy as np
    new_table = []
    nb_of_rows = len(table)
    nb_of_cols = len(table[0])
    nb_of_chars = []
    for row in table:
        nb_of_chars.append([len(elem) for elem in row])
    nb_of_chars = np.array(nb_of_chars)
    max_chars_in_cols = nb_of_chars.max(axis=0)
    print('    - Number of chars in table cells: {}'.format(max_chars_in_cols))

    for row in table:
        for i, elem in enumerate(row):
            if i == 0:
                row_content = '|'
            elif i > 0:
                row_content += ' {:{align}{width}} |'.format(elem, align='<', width=(max_chars_in_cols[i]))

        print(row_content)


def correct_tables():
    """Make sure that:
    * proportion and number of dashes (---) are sufficiently enough for PDF generation, and 
    * fences (|) are corrected aligned
    """
    markdown_list = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(".md") and file != 'index.md' and file != '01-contributors.md':
                print('Check tables in {}'.format(os.path.join(root, file)))
                markdown_list.append(os.path.join(root, file))
                with open(os.path.join(root, file),'r') as f:
                    content = f.readlines()
                line_nb = 0
                tables = []
                table_mode = False
                for line in content:
                    if line:
                        # Use dashes to detect where a table start 
                        if '--' in line and not table_mode:
                            table_mode = True
                            print('  * Detected table starting line {}'.format(line_nb-1))
                            table = []
                            header_row = [c.strip() for c in content[line_nb-1].split('|')]
                            row = [c.strip() for c in line.split('|')]
                            table.append(header_row)
                            table.append(row)
                        elif table_mode:
                            row = [c.strip() for c in line.split('|')]
                            # Add row to table if this is not the end of the table
                            if row != ['']:
                                table.append(row)
                            else:
                                table_mode = False
                                table = correct_table(table)
                                tables.append(table)


                    line_nb += 1
                #print(tables)

           
def build_pdf(filename):
    """Construct command with required pandoc flags and run using subprocess.

    Parameters
    ----------
    filename : str
        Name of the output file.

    """
    markdown_list = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(".md") and file != 'index.md':
                markdown_list.append(os.path.join(root, file))
            elif file == 'index.md':
                index_page = os.path.join(root, file)

    default_pandoc_cmd = "pandoc "

    # creates string of file paths in the order we'd like them to be appear
    # ordering is taken care of by the inherent file naming
    files_string = index_page + " " + " ".join(sorted(markdown_list))

    flags = (" -f markdown_github --include-before-body cover.tex --toc "
             "-V documentclass=report --listings -H listings_setup.tex "
             "-H header.tex -V linkcolor:blue -V geometry:a4paper "
             "-V geometry:margin=2cm --pdf-engine=xelatex -o ")
    output_filename = filename

    cmd = default_pandoc_cmd + files_string + flags + output_filename
    subprocess.run(cmd.split())


if __name__ == "__main__":
    correct_tables()
    build_pdf('bids-spec.pdf')