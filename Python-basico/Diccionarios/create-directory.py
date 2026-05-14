#
# Create folder in MAC OS computer, then file, 
# then read the file
#
#
# Declare library for OS
#
import os
#
# Variables
#
desktop_path = '';
projects_folder = '';
exist_ok = False;
ideas_file = '';
contents = '';
number_lines = [2,3,4,5,6,7];
index_for = 1;
#
#  Create a folder on the desktop called "Projects"
#
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop");
projects_folder = os.path.join(desktop_path, "Projects2");
os.makedirs(projects_folder, exist_ok=True);
print();
print("------------------------------------------");
print("-----------Program OUTPUT ---------");
print("------------------------------------------");
print(f'Folder was created: {projects_folder}');
print();
#
# Create a text file called "ideas.txt" inside the "Projects2" folder
#
ideas_file = os.path.join(projects_folder, "ideas.txt");
with open(ideas_file, "w") as file:
    file.write('-----Beginning of txt file-------\n');
    file.write("This is my first file using a Python program in a mas OS - Line 1\n");
    for index_for in number_lines:
        file.write(f'Line: ' + str(index_for) + '\n');
        index_for = index_for + 1;
with open(ideas_file, "a") as file:
    file.write('-----End of txt file-------\n');
print();
print(f'File created and written in mac OS: {ideas_file}');
print();
# 
# Display the contents of "ideas.txt" on screen
#
print("\n ----- Contents of ideas.txt:------\n");
print();
with open(ideas_file, "r") as file:
    contents = file.read();
    print(contents);
print();
print("------------------------------------------");
print("-----------End of Program OUTPUT ---------");
print("------------------------------------------");
#
# End of Program
# 