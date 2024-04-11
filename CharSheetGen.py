# Character Sheet Generator
# CSG is a program for generating character sheets from basic info
# by alpenstorm

# import necessary libraries
import os
import json
import urllib.request

# assign global variables 
global saveFolder
global tempFolder
global settings

print('''**********************************************
CHARACTER SHEET GENERATOR v.1.0.1
by alpenstorm
**********************************************''')

#---------------------------------------------------
# Pre-run checks
#---------------------------------------------------

# there are three pairs of try-excepts for the checks
# the first one (under this comment) checks if the "conf/" folder exists. if it doesn't, it will create one (conf is where we store the config file)
try:
    os.listdir("conf/")
except:
    print('NO CONFIG FOLDER FOUND AT conf/, CREATING...')
    os.mkdir("conf/")

# this one checks if the config file exists. if it doesn't, it will create one
try:
    with open('conf/config.json', 'r', encoding='utf8') as f:
        settings = json.load(f)
        saveFolder = settings["saveFolder"]
        tempFolder = settings["tempFolder"]
    f.close()
except:
    print('NO CONFIG FILE FOUND AT "conf/config.json, CREATING...')
    data = {"saveFolder": "sheets/", "tempFolder": "temp/", "cssAsked": "false"}
    with open('conf/config.json', "w", encoding='utf8') as w:
        w.write(json.dumps(data, indent=4))
    with open('conf/config.json', 'r', encoding='utf8') as r:
        settings = json.load(r)

    saveFolder = settings["saveFolder"]
    tempFolder = settings["tempFolder"]
    w.close()
    r.close()

# and this one checks if the root folders exist
try:
    os.listdir(saveFolder)
    os.listdir(tempFolder)
except:
    print(f"NO SAVE FOLDER FOUND AT {saveFolder}, CREATING...")
    os.mkdir(saveFolder)
    print(f"NO TEMP FOLDER FOUND AT {tempFolder}, CREATING...")
    os.mkdir(tempFolder)

#---------------------------------------------------
# Functions
#---------------------------------------------------

# Function Explanations:
# write(img, name, origin, basicinfo, otherinfo, combatinfo, quotes) - 
# main() - 

# clears the terminal when called
def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# creates a menu that downloads the default css file from my website and saves the response in the config json
def css(message):
    with open('conf/config.json', "r", encoding='utf8') as w:
        data = json.load(w)
        css_asked = data.get("cssAsked")
    w.close()
    wr = {"saveFolder": "sheets/", "tempFolder": "temp/", "cssAsked": "true"}
    if css_asked == "false":
        if message == "y" or message == "Y":
            urllib.request.urlretrieve("https://dfstudios.neocities.org/charsheetmaker/styles.css", f"{saveFolder}/styles.css")
            open('conf/config.json', "w").close()
            with open('conf/config.json', "w", encoding='utf8') as w:
                w.write(json.dumps(wr, indent=4))
            w.close()
        elif message == "n" or message == "N":
            open('conf/config.json', "w").close()
            with open('conf/config.json', "w", encoding='utf8') as w:
                w.write(json.dumps(wr, indent=4))
            w.close()
        else:
            css(input("[Y,N]: "))

# takes an input txt file and creates a new text file with html <br> tags instead of newline chracters
def insert_br(input_file_path, output_file_path):
    replacements = {'\n': '<br>'}
    try:
        with open(input_file_path, 'r', encoding='utf8') as infile, open(output_file_path, 'w', encoding='utf8') as outfile:
            for line in infile:
                for src, target in replacements.items():
                    line = line.replace(src, target)
                outfile.write(line)
        print(f"Line breaks replaced successfully. Output written to {output_file_path}")
        infile.close()
        outfile.close()
    except FileNotFoundError:
        print(f"Error: File '{input_file_path}' not found.")
        insert_br(input_file_path, output_file_path)

# takes an input file, reads it, and stores the text in a variable
def read_file_contents(file_path) -> str:
    try:
        with open(file_path, 'r', encoding='utf8') as file:
            file_contents = file.read()
            return file_contents
    except FileNotFoundError:
        return "File not found."

# writes the input variables to an html file
def write(img, maximgheight, name, origin, basicinfo, otherinfo, combatinfo, quotes):
    basicinfo = read_file_contents(f'{tempFolder}/basicInfoTemp.txt')
    otherinfo = read_file_contents(f'{tempFolder}/otherInfoTemp.txt')
    combatinfo = read_file_contents(f'{tempFolder}/combatInfoTemp.txt')
    quotes = read_file_contents(f'{tempFolder}/quotesTemp.txt')
    
    with open(f'{saveFolder}/CSG {name} ({origin}).html', "w", encoding='utf8') as w:
        w.write(f'''<!DOCTYPE html>
<link rel="stylesheet" href="styles.css">

<img src="{img}" alt="{name}" style="max-height: {maximgheight}px; float: right;">

<h1>Name: {name}</h1>
<h3>Origin: {origin}</h3>

<body>
    <h4>Basic Information</h4>
    <p>{basicinfo}</p>
    
    <h4>Other Information</h4>
    <p>{otherinfo}</p>

    <h4>Combat Information</h4>
    <p>{combatinfo}</p>

    <h4>Quotes</h4>
    <blockquote>{quotes}</blockquote>
</body>
''')

    w.close()
    print(f"Successfully wrote to {saveFolder}/CSG {name} ({origin}).html")
    os.remove(f"{tempFolder}/basicInfoTemp.txt")
    os.remove(f"{tempFolder}/otherInfoTemp.txt")
    os.remove(f"{tempFolder}/combatInfoTemp.txt")
    os.remove(f"{tempFolder}/quotesTemp.txt")
    print("Processed and removed temporary files!")

def ask_css():
    with open('conf/config.json', "r", encoding='utf8') as r:
        data = json.load(r)
        css_asked = data.get("cssAsked")
        if css_asked == "false":
            css(input("Do you want to download a CSS file for the style? [Y,N]: "))
    r.close()

# puts it all together
def main():
    write(input("Enter the location of the image file for the char sheet (can be a web link): "), 
          input("Enter the max image height (in pixels): "),
          input("Enter the character's name: "), 
          input("Enter the character's origin: "),
          insert_br(input("Enter text file containing basic info: "), f"{tempFolder}/basicInfoTemp.txt"),
          insert_br(input("Enter text file containing other info: "), f"{tempFolder}/otherInfoTemp.txt"),
          insert_br(input("Enter text file containing combat info: "), f"{tempFolder}/combatInfoTemp.txt"),
          insert_br(input("Enter text file containing quotes: "), f"{tempFolder}/quotesTemp.txt")
          )

    xt = input("Do you want to create another sheet? [Y,N]: ")
    
    if xt == "y" or xt == "Y":
        clear()
        main()
    elif xt == "n" or xt == "N":
        quit()
    else:
        xt = input("[Y,N]: ") 

#---------------------------------------------------
# Start the program and ask to download the CSS file
#---------------------------------------------------

ask_css()
main()