# LMI-Capstone-2021

# Automated Onotology Generation Capstone Readme

Capstone Github

## Description

This repo contains all team code written to parse and build automated ontologies from the public DoD documents here: https://mikeanders.org/data/Ontologies/

## Getting Started

### Dependencies

Use the 'environment.yml' file to create a conda virtual environment that has all the necessary packages.

### Installing

Run 'conda env create --file environment.yml' in an anaconda prompt to create the 'capstone' virtual environment. Switch to this virtual environment by running 'conda activate capstone'.

### Running Files

The DocExtract.py file reads and parses all of the documents and outputs the file 'full_dataframe.csv'. This csv contains a spreadsheet with the following fields:

| Field       | Description |
| ----------- | ----------- |
| doc_type    | Type of document (five types: Admin Instructions, Directives, Instructions, Manuals, Memos)       |
| file_name   | Name of the document on the website        |
| raw_text      | The text read straight from the .txt file       |
| cleaned_text   | The text cleaned by eliminating line breaks and eliminating footer/headers        |
| cleaned_text_list      | A list of cleaned text separated by lines (useful for Section Segmentation       |
| url   | The url where the .txt document can be found        |
| acronyms      | A dictionary of the acronyms in the document (key - acronym, value - phrase)       |
| glossary   | A dictionary of the glossary definitions in the document (key - term, value - definition)        |

## Authors

Isaac Stevens (is3sb)
<br>
Srinivasa Chivaluri (spc6ph)
<br>
Katelyn Barbre (kb3kk)
<br>
Abby Bernhardt (aeb4rv)
