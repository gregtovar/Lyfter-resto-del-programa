"""READ LINES - Reads a text file into a list of lines - Version 1.0

Developed by Greg Tovar

OCT 28 2026

"""


#
#
# # Returns every line of the file as a list. Each line keeps its "\n".
#
# Raises FileNotFoundError (from Python itself) when the file does not exist.



def read_lines(path):
    with open(path, 'r') as f:
        return f.readlines()



#
# End
#
