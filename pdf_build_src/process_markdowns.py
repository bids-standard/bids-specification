'''
List of functions required: 
1. running shell commands 
2. extracting header string from CHANGELOG 
3. adding header string to header.tex file 
4. copy images to root images directory 
5. making a copy of the src directory in the cd and using that for the pdf generation 
6. Finding cross .md internal links and replacing them with only the text 
7. Generating pdf with pandoc 
'''

import os, sys
import argparse
import subprocess
import re
import fileinput
import io

def run_shell_cmd(command): 
	# print(command.split())
	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	
	# subprocess.run(command.split())
	output = process.stdout.read()
	
	return output.decode('utf-8')

def copy_src():
	# source and target directories
	src_path = "../src/"
	target_path = "src_copy"

	# dir_name = "src_copy"
	mkdir_cmd = "mkdir "+target_path
	run_shell_cmd(mkdir_cmd)

	# make a copy of the source directory in the current directory
	copy_cmd = "cp -a "+src_path+" "+target_path

	# run_shell_cmd("pwd")
	run_shell_cmd(copy_cmd)

def remove_src_copy():
	"""
	if a copy of the src file has been created then delete it once pdf is generated
	"""
	run_shell_cmd("rm -rf src_copy")
	return

def copy_bids_logo():
	"""
	copies BIDS_logo.jpg from the BIDS_logo directory in the root 
	"""
	run_shell_cmd("cp ../BIDS_logo/BIDS_logo.jpg src_copy/images/") 

def copy_images(root_path): 
	"""
	copies images from images directory of 
	subdirectories to images directory in the 
	src directory
	"""

	""" TODO: taking complex directory structures into consideration while copy images

	# subdir_list = []

	# for root, dirs, files in os.walk('./src_copy'):
	# 	break

	# # finding subdirectories that are basically modules and follow the same
	# # naming convention as those of the .md files 
	# for each in dirs:
	# 	split_filename = each.split('-')
	# 	# print(split_filename)
	# 	x = re.search("(\d{2}|\d+)",split_filename[0])
	# 	if x:
	# 		subdir_list.append(each)
	# print(subdir_list)
	"""
	
	subdir_list = []
	for root, dirs, files in os.walk(root_path):
		if 'images' in dirs: 
			subdir_list.append(root)
	print(subdir_list)

	for each in subdir_list:
		if each != root_path: 
			run_shell_cmd("cp -a "+each+"/images/"+" "+root_path+"/images/")

	# 	break

def build_pdf(filename, root_path):
	subprocess.run(["mv",])
	markdown_list=[]
	for root, dirs, files in os.walk(root_path):
		for file in files:
			if file.endswith("." + "md") and file != 'index.md':
				markdown_list.append(os.path.join(root, file))
			elif file == 'index.md': 
				index_page = os.path.join(root, file)
	
	default_pandoc_cmd ="pandoc "
	files_string = index_page + " " +" ".join(sorted(markdown_list))
	# print(files_string)
	flags = " -f markdown_github --include-before-body cover.tex --toc -V documentclass=report --listings -H listings_setup.tex -H header.tex -V linkcolor:blue -V geometry:a4paper -V geometry:margin=2cm --pdf-engine=xelatex -o " 
	output_filename = filename
	cmd = default_pandoc_cmd + files_string + flags + output_filename
	# subprocess.run("pwd")
	# subprocess.run(cmd.split())

def extract_header_string(): 
	released_versions = []
	for i, line in enumerate(open('./src_copy/CHANGES.md')):
		
		match_list = re.findall(r'^##\s\[v.+\]',line)
		if len(match_list) > 0: 
			wordlist = line.split()
			# print(match_list[0].split())
			released_versions.append([match_list[0].split()[1], wordlist[2] ])
	version_number = released_versions[0][0].strip('[]')
	version_date = released_versions[0][1].strip('()')

	# for each in released_versions: 
	# 	version_number = each.split()[1]
	# 	version_date = each.split()[2]
	return version_number, version_date

def add_header(): 
	version_number = extract_header_string()[0]
	version_date = extract_header_string()[1]


	header_string = "\chead{Brain Imaging Data Structure "+ version_number +" "+ version_date+"}"
	i=0

	# for line in fileinput.input('header.tex', inplace=True):
	# 	print(line)
	# 	if line.startswith('\chead'):
	# 		line.replace(r'\\chead\{.+\}',header_string)

	# with is like your try .. finally block in this case
	with open('header.tex', 'r') as file:
		data = file.readlines()

	print(data)
	# print "Your name: " + data[0]

	# now change the 2nd line, note that you have to add a newline
	data[-2] = header_string+'\n'

	# # and write everything back
	with open('header.tex', 'w') as file:
		file.writelines( data )

# def remove_cross_internal_links(root_path):
	

# 	primary_pattern = re.compile(r'\[((?!http).[\w\s.\(\)`*/–]+)\]\(((?!http).+(\.md|\.yml|\.md#[\w\-\w]+))\)')
	

# 	for root, dirs, files in os.walk(root_path):
# 		for file in files:
# 			if file.endswith("." + "md"):
# 				print("here with "+file)
# 				with open(os.path.join(root,file),'r') as markdown: 
# 					data = markdown.readlines()

# 				for ind, line in enumerate(data):
# 					match = primary_pattern.search(line)

# 					if match: 
# 						line = re.sub(primary_pattern, match.group().split('](')[0][1:], line)

# 					data[ind] = line

# 				with open(os.path.join(root,file), 'w') as markdown: 
# 					markdown.writelines(data)


def remove_internal_links(root_path, link_type):

	if link_type == 'cross':
		primary_pattern = re.compile(r'\[((?!http).[\w\s.\(\)`*/–]+)\]\(((?!http).+(\.md|\.yml|\.md#[\w\-\w]+))\)')
	elif link_type == 'same':
		primary_pattern = re.compile(r'\[([\w\s.\(\)`*/–]+)\]\(([#\w\-._\w]+)\)') 

	for root, dirs, files in os.walk(root_path):
		for file in files:
			if file.endswith("."+"md"):
				with open(os.path.join(root,file),'r') as markdown: 
					data = markdown.readlines()

				for ind, line in enumerate(data):
					match = primary_pattern.search(line)

					if match: 
						line = re.sub(primary_pattern, match.group().split('](')[0][1:], line)

					data[ind] = line

				with open(os.path.join(root,file), 'w') as markdown: 
					markdown.writelines(data)
					

if __name__ == '__main__':

	root_path = './src_copy'

	# Step 1: make a copy of the src directory in the current directory 
	copy_src()

	# Step 2: copy BIDS_logo to images directory of the src_copy directory
	copy_bids_logo()
	
	# Step 3: copy images from subdirectories of src_copy directory 
	copy_images(root_path)

	extract_header_string()
	add_header()

	# remove_cross_internal_links(root_path)
	remove_internal_links(root_path, 'cross')
	remove_internal_links(root_path, 'same')

	# Last but 1 step: running pandoc
	# pdf_filename = "bids-specs.pdf"
	# build_pdf(pdf_filename, root_path)


	# # Last step: remove the 'src_copy' directory
	# remove_src_copy()





