#!/usr/bin/env python3
#
# Pelican to Hugo v20180603
#
# Convert Markdown files using the pseudo YAML frontmatter syntax
# from Pelican to files using the strict YAML frontmatter syntax
# that Hugo and other static engines expect.
#
# Anthony Nelzin-Santos
# https://anthony.nelzin.fr
# anthony@nelzin.fr
#
# European Union Public Licence v1.2
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-11-12

import os, os.path, re
import subprocess
from shutil import rmtree, copytree

    #  Add the path to your files below
outpath = '/home/alex/websites/sci-blog.com/content/folder'
inpath = '/home/alex/websites/www.sci-blog.com/content'

def pre_process():

    # Clear files in outpath
    for files in os.listdir(outpath):
        path = os.path.join(outpath, files)
        try:
            rmtree(path)
        except OSError:
            os.remove(path)

    # copy all Markdown files over
    cp_cmd = f'cp {inpath}/*.md {outpath}/'
    os.system(cp_cmd) # need 'shell=True' if passing the whole command as a string

def pelicantohugo():
    files = os.listdir(outpath)

    for file in files:
        first_img = True
        file_name, file_extension = os.path.splitext(file)
        # Input files will be left in place,
        # output files will be suffixed with "_hugo".
        regexed_file = file_name + '_hugo' + file_extension

        # Only convert visible Markdown files.
        # This precaution is useless… until it is useful,
        # mainly on .DS_Store-ridden macOS folders.
        if not file_name.startswith('.') and file_extension in ('.md'):
            input_file = os.path.join(outpath, file)
            output_file = os.path.join(outpath, regexed_file)

            # The files will be edited line by line using regex.
            # The conversion of a thousand files only takes a few seconds.
            with open(input_file, 'r',newline='') as fi, open(output_file, 'w') as fo:
                for line in fi:
                    # Frontmost handling
                    line = re.sub(r'(Title:)', r'title:', line)
                    line = re.sub(r'(Tags:)', r'tags:', line)
                    line = re.sub(r'(Date:)', r'date:', line)
                    line = re.sub(r'(Category:)', r'categories:', line)
                    line = re.sub(r'(Slug:)', r'slug:', line)
                    line = re.sub(r'(Summary:.*$)', r'', line)
                    line = re.sub(r'(author:.*$)', r'', line)
                    line = re.sub(r'(Subtitle:)', r'description:', line)
                    # Add closing frontmatter delimiter after the tags.
                    line = re.sub(r'(\[TOC\].*$)', r'---', line)

                    # Add opening frontmatter delimiter before the title.
                    line = re.sub(r'(title:)', r'---\n\1', line)
                    # Enclose the title in quotes.
                    line = re.sub(r'title: (.*)', r'title: "\1"', line)
                    line = re.sub(r'description: (.*)', r'description: "\1"', line)
                    # Change date formatting.
                    line = re.sub(r'(date: \d{4}-\d{2}-\d{2}) (\d{2}:\d{2})', r'\1T\2:00Z', line)
                    # Slow but insightful way to edit the tags.
                    if re.match(r'tags: (.*)', line):
                        # Split the comma separated list of tags.
                        tag_split = re.sub(r'(.*)', r'\1', line).split(', ')
                        # Output the new list of tags.
                        tag_plist = '\n- '.join(tag_split)
                        # Insert a newline before the list.
                        tag_list = re.sub(r'tags: (.*)', r'tags: \n- \1', tag_plist)
                        # And enclose the tags in quotes.
                        line = re.sub(r'- (.*)', r'- "\1"', tag_list)
                    # get proper slug
                    if re.match(r'slug: (.*)', line):
                        slug_match = re.search(r'slug: (.*)', line)
                        slug = slug_match.group(1)
                        os.system(f'mkdir {outpath}/{slug}')  # create subfolder using slug for feature image
                    if re.search(r'\(https://cdn.*?\)', line):
                        img = re.search(r'!\[(.*?)\]\((https://cdn.*?)\)', line)
                        img_url = img.group(2)
                        img_caption = img.group(1)
                        if first_img:   # for first image which is the feature image, need special handling
                            first_img = False
                            if re.search(r'\.((?:jpg|png|jpeg|gif|svg))', img_url):
                                img_e = re.search(r'\.((?:jpg|png|jpeg|gif|svg))', img_url)
                                img_ext = img_e.group(1)
                            else:
                                img_ext = 'jpeg'
                            # download image from Medium and put into the created subfolder
                            os.system(f'wget -O {outpath}/{slug}/{slug}.{img_ext} {img_url}')
                            line = ''
                        else:
                            # all other images just extract the image url and put into 'figure' shortcode
                            line = f'{{{{< figure caption="{img_caption}" src="{img_url}" >}}}}'

                    # YouTube shortcode
                    if re.search(r'src="https://www.youtube.com/embed/(.*?)"', line):
                        video = re.search(r'src="https://www.youtube.com/embed/(.*?)"', line)
                        video_code = video.group(1)
                        line = f'{{{{< youtube video_code >}}}}'
                    fo.write(line)
                # Print a little something about the conversion.
                #print(file_name + ' converted.')
            os.remove(input_file)

            # when all is ready, set the 'image:' front matter correctly so feature image could work
            with open(output_file, 'r') as fi:
                data = fi.readlines ()
            with open(output_file, 'w') as fo:
                image_meta_added = False
                for line in data:
                    # Add opening frontmatter delimiter before the title.
                    if not image_meta_added and not first_img:
                        line = re.sub(r'(---)', f'---\nimage: {slug}.{img_ext}', line)
                        image_meta_added = True
                    fo.write(line)
        if not first_img: os.system(f'mv {output_file} {outpath}/{slug}/index.md')

pre_process()
pelicantohugo()
