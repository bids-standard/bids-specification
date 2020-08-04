"""Use the pandoc library as a final step to build the pdf.

This is done once the duplicate src directory is processed.
"""
import os
import subprocess

"""Number of chars maximal in one line approximated from a line of the PDF"""
NB_CHARS_LINE_PDF = 100

def correct_table(table):
    """Compute the max number of characters and dashes for each column and create the corrected table

    Parameters
    ----------
    table : List of List of str
        Table content extracted from the markdown file.

    Returns
    -------
    new_table : List of str
        List of corrected lines of the input table with corrected number of dashes and aligned fences.
    """
    import numpy as np
    
    nb_of_rows = len(table)
    nb_of_cols = len(table[0])

    nb_of_chars = []
    for i, row in enumerate(table):
         # Ignore number of dashes in the count of characters
        if i != 1:
            nb_of_chars.append([len(elem) for elem in row])

    # Convert the list to a numpy array and computes the maximum number of chars for each column
    nb_of_chars_arr = np.array(nb_of_chars)
    max_chars_in_cols = nb_of_chars_arr.max(axis=0)

    # Computes number of dashes based on the maximal number of characters in each column
    nb_of_dashes = max_chars_in_cols
    prop_of_dashes = nb_of_dashes / nb_of_dashes.sum()
    nb_of_chars_in_pdf = prop_of_dashes * int(NB_CHARS_LINE_PDF)

    # print('    - Number of chars in table cells: {}'.format(max_chars_in_cols))
    # print('    - Number of dashes (per column): {}'.format(nb_of_dashes))
    # print('    - Proportion of dashes (per column): {}'.format(prop_of_dashes))
    # print('    - Number of chars max in column (PDF): {}'.format(nb_of_chars_in_pdf))

    # Offset that can be used to ajust the correction of number of dashes in the first and 
    # second columns by the number specified
    offset = [15, 0]
    
    # Computes the corrected number of dashes. An offset can be used to extend 
    for i, (value, prop) in enumerate(zip(max_chars_in_cols,prop_of_dashes)):
        # Correction for first column
        if i == 1:
            if int(value) < int(NB_CHARS_LINE_PDF) and prop < 0.5:
                first_column_width = int(nb_of_dashes.sum() * (value / int(NB_CHARS_LINE_PDF)) + offset[0])
            else:
                first_column_width = int(value)
            # print('    - Final number of chars in first column: {}'.format(first_column_width))
        # Correction for second column
        elif i == 2:
            if int(value) < int(NB_CHARS_LINE_PDF) and prop < 0.5:
                second_column_width = int(nb_of_dashes.sum() * (value / int(NB_CHARS_LINE_PDF)) + offset[1])
            else:
                second_column_width = int(value)
            # print('    - Final number of chars in second column: {}'.format(second_column_width))

    # Format the lines with correct number of dashes or whitespaces and correct alignment of fences and
    # populate the new table (A List of str)
    new_table = []
    for i, row in enumerate(table):
        row_content = []
        for j, elem in enumerate(row):
            if j == 0 or j == len(row) - 1:
                row_content.append(elem)
            else:
                if i == 1:
                    if j == 1:
                        row_content.append('{:-{align}{width}}'.format(elem, align='<', width=(first_column_width)))
                    elif j == 2:
                        row_content.append('{:-{align}{width}}'.format(elem, align='<', width=(second_column_width)))
                    else:
                        row_content.append('{:-{align}{width}}'.format(elem, align='<', width=(max_chars_in_cols[j])))
                else:
                    if j == 1:
                        row_content.append('{:{align}{width}}'.format(elem, align='<', width=(first_column_width)))
                    elif j == 2:
                        row_content.append('{:{align}{width}}'.format(elem, align='<', width=(second_column_width)))
                    else:
                        row_content.append('{:{align}{width}}'.format(elem, align='<', width=(max_chars_in_cols[j])))
           
        #print(row_content)

        # Handles return to line
        if i < nb_of_rows - 1:
            new_table.append('|'.join(row_content)+' \n')
        elif i == nb_of_rows - 1:
            new_table.append('|'.join(row_content)+' \n\n')

    return new_table

def correct_tables():
    """Make sure that:
    * proportion and number of dashes (---) are sufficiently enough for PDF generation, and 
    * fences (|) are corrected aligned
    """
    markdown_list = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(".md") and file != 'index.md' and file != '01-contributors.md' and file != '04-entity-table.md':
                print('Check tables in {}'.format(os.path.join(root, file)))
                markdown_list.append(os.path.join(root, file))
                with open(os.path.join(root, file),'r') as f:
                    content = f.readlines()
                tables = []
                table_mode = False
                start_line = 0
                new_content = []
                for line_nb, line in enumerate(content):
                    if line:
                        # Use dashes to detect where a table start and extract the header and the dashes lines
                        if '--' in line and not table_mode:
                            table_mode = True
                            start_line = line_nb-1
                            print('  * Detected table starting line {}'.format(start_line))
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
                                end_line = line_nb-1
                                table_mode = False
                                
                                # Correct the given table
                                table = correct_table(table)

                                # Update the corresponding lines in the markdown with the corrected table
                                count = 0
                                for i, new_line in enumerate(content):
                                    if i == start_line:
                                        new_content.pop()
                                    if i >= start_line and i <= end_line:
                                        new_content.append(table[count])
                                        count += 1   
                        else:
                            new_content.append(line)

                    line_nb += 1

                # Overwrite with the new markdown content
                with open(os.path.join(root, file),'w') as f:
                    f.writelines(new_content)

           
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