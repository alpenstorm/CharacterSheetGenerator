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
global textFolder

global settings

print('''**********************************************
Character Sheet Generator (CSG) v.1.1.3
by alpenstorm
**********************************************''')

#---------------------------------------------------
# Pre-run checks
#---------------------------------------------------

# there are four pairs of try-excepts for the checks
# the first one (under this comment) checks if the "conf/" folder exists. if it doesn't, it will create one (conf is where we store the config file)
try:
    os.listdir("conf/")
except:
    print("NO CONFIG FOLDER FOUND AT 'conf/', CREATING...")
    os.mkdir("conf/")

# this one checks if the config file exists. if it doesn't, it will create one
try:
    with open('conf/config.json', 'r', encoding='utf8') as f:
        settings = json.load(f)
        saveFolder = settings["saveFolder"]
        tempFolder = settings["tempFolder"]
        textFolder = settings["textFolder"]
    f.close()
except:
    print("NO CONFIG FILE FOUND AT 'conf/config.json', CREATING...")
    data = {"saveFolder": "sheets/", "tempFolder": "temp/", "textFolder": "txt/", "cssAsked": "false"}
    with open('conf/config.json', "w", encoding='utf8') as w:
        w.write(json.dumps(data, indent=4))
    with open('conf/config.json', 'r', encoding='utf8') as r:
        settings = json.load(r)

    saveFolder = settings["saveFolder"]
    tempFolder = settings["tempFolder"]
    textFolder = settings["textFolder"]

    w.close()
    r.close()


# and this one checks if the root folders exist
try:
    os.listdir(saveFolder)
    os.listdir(tempFolder)
    os.listdir(f"{textFolder}/")
except:
    print(f"NO SAVE FOLDER FOUND AT {saveFolder}, CREATING...")
    os.mkdir(saveFolder)
    print(f"NO TEMP FOLDER FOUND AT {tempFolder}, CREATING...")
    os.mkdir(tempFolder)
    print(f"NO TEXT FOLDER FOUND AT '{textFolder}/', CREATING...")
    os.mkdir(f"{textFolder}/")

# this one tries to find the default csg files to add into the html
try:
    with open(f'{textFolder}/basic.csg', 'r', encoding='utf8') as f:
        file_basic = f'{textFolder}/basic.csg'
        f.close()
    with open(f'{textFolder}/other.csg', 'r', encoding='utf8') as f:
        file_other = f'{textFolder}/other.csg'
        f.close()
    with open(f'{textFolder}/combat.csg', 'r', encoding='utf8') as f:
        file_combat = f'{textFolder}/combat.csg'
        f.close()
    with open(f'{textFolder}/quotes.csg', 'r', encoding='utf8') as f:
        file_quotes = f'{textFolder}/quotes.csg'
        f.close()
    with open(f'{textFolder}/trivia.csg', 'r', encoding='utf8') as f:
        file_trivia = f'{textFolder}/trivia.csg'
        f.close()
except:
    print(f"NO BASIC TEXT FILE FOUND AT '{textFolder}/basic.csg', CREATING...")
    open(f'{textFolder}/basic.csg', 'w', encoding='utf8').close()
    print(f"NO OTHER TEXT FILE FOUND AT '{textFolder}/other.csg', CREATING...")
    open(f'{textFolder}/other.csg', 'w', encoding='utf8').close()
    print(f"NO COMBAT TEXT FILE FOUND AT '{textFolder}/combat.csg', CREATING... ")
    open(f'{textFolder}/combat.csg', 'w', encoding='utf8').close()
    print(f"NO QUOTES TEXT FILE FOUND AT '{textFolder}/quotes.csg', CREATING... ")
    open(f'{textFolder}/quotes.csg', 'w', encoding='utf8').close()
    print(f"NO TRIVIA TEXT FILE FOUND AT '{textFolder}/trivia.csg', CREATING... ")
    open(f'{textFolder}/trivia.csg', 'w', encoding='utf8').close()

    print("Input the basic info, other info, combat info, quotes, and trivia in these default files if you want. \nIf you don't, you can specify the text files in the prompt.")
    input("Restarting CSG, press [Return].")
    quit()

#---------------------------------------------------
# Functions
#---------------------------------------------------

# clears the terminal when called
def clear() -> None:
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# creates a menu that downloads the default css file from my website and saves the response in the config json
def css(message: str) -> None:
    with open('conf/config.json', "r", encoding='utf8') as w:
        data = json.load(w)
        css_asked = data.get("cssAsked")
    w.close()
    wr = {"saveFolder": "sheets/", "tempFolder": "temp/", "textFolder": "txt/", "cssAsked": "true"}
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

# asks to download a css file if the cssAsked variable is false in config.json
def ask_css() -> None:
    with open('conf/config.json', "r", encoding='utf8') as r:
        data = json.load(r)
        css_asked = data.get("cssAsked")
        if css_asked == "false":
            css(input("Do you want to download a CSS file for the style? [Y,N]: "))
    r.close()

# helper function for insert_br()
def do_br(i: str, o: str) -> None:
    try:
        replacements = {'\n': '<br>'}
        with open(i, 'r', encoding='utf8') as infile, open(o, 'w', encoding='utf8') as outfile:
            for line in infile:
                for src, target in replacements.items():
                    line = line.replace(src, target)
                outfile.write(line)
        print(f"Output written to {o}")
        infile.close()
        outfile.close()
    except FileNotFoundError:
        print(f"Error: File '{i}' not found.")
        quit()    

# takes an input txt file and creates a new text file with html <br> tags instead of newline chracters
def insert_br(input_file_path: str = "", default_input_file_path: str = "", output_file_path: str = "") -> None:
    if default_input_file_path != "":
        do_br(default_input_file_path, output_file_path)
    else:
        do_br(input_file_path, output_file_path)

# helper function for insert_li()
def do_li(i: str ,o: str) -> None:
    try:
        with open(i, 'r') as input_file:
            lines = input_file.readlines()

        formatted_lines = [f"<li>{line.strip()}</li>" for line in lines]

        with open(o, 'w') as output_file:
            output_file.write("\n".join(formatted_lines))

        print(f"Output written to {o}")
    except FileNotFoundError:
        print(f"Error: File '{i}' not found.")
        quit()

# takes an input txt file and creates an HTML list out of it
def insert_li(input_file_path: str = "", default_input_file_path: str = "", output_file_path: str = "") -> None:
    if default_input_file_path != "":
        do_li(default_input_file_path, output_file_path)
    else:
        do_li(input_file_path, output_file_path)

# takes an input file, reads it, and stores the text in a variable
def read_file_contents(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf8') as file:
            file_contents = file.read()
            return file_contents
    except FileNotFoundError:
        return "File not found."

# writes the input variables to an html file
def write(img: str, maximgheight: int, name: str, origin: str, 
          race: str, basicinfo: str, otherinfo: str, 
          combatinfo: str, quotes: str, trivia: str) -> None:

    basicinfo = read_file_contents(f'{tempFolder}/basicInfoTemp.txt')
    otherinfo = read_file_contents(f'{tempFolder}/otherInfoTemp.txt')
    combatinfo = read_file_contents(f'{tempFolder}/combatInfoTemp.txt')
    quotes = read_file_contents(f'{tempFolder}/quotesTemp.txt')
    trivia = read_file_contents(f'{tempFolder}/triviaTemp.txt')
    
    with open(f'{saveFolder}/CSG {name} ({origin}).html', "w", encoding='utf8') as w:
        w.write(f'''<!DOCTYPE html>
<link rel="stylesheet" href="styles.css">

<img src="{img}" alt="{name}" style="max-height: {maximgheight}px; float: right;">

<h1>Name: {name}</h1>
<h2>Origin: {origin}</h2>
<h3>Race: {race}</h3>

<body>
    <h4>Basic Information</h4>
    <p>{basicinfo}</p>
    
    <h4>Other Information</h4>
    <p>{otherinfo}</p>

    <h4>Combat Information</h4>
    <p>{combatinfo}</p>

    <h4>Quotes</h4>
    <blockquote>{quotes}</blockquote>

    <h4>Trivia</h4>
    <ul>{trivia}</ul>
</body>
''')

    w.close()
    print(f"Successfully wrote to {saveFolder}/CSG {name} ({origin}).html")
    os.remove(f"{tempFolder}/basicInfoTemp.txt")
    os.remove(f"{tempFolder}/otherInfoTemp.txt")
    os.remove(f"{tempFolder}/combatInfoTemp.txt")
    os.remove(f"{tempFolder}/quotesTemp.txt")
    os.remove(f"{tempFolder}/triviaTemp.txt")
    print("Processed and removed temporary files!")

# creates a small menu to quit the program
def smallmenu(message: str) -> None:
    if message == "y" or message == "Y":
        clear()
        main()
    elif message == "n" or message == "N": quit()
    else: smallmenu(input("[Y,N]: ")) 

# puts it all together
def main() -> None:
    write(input("Enter the location of the image file for the char sheet (can be a web link): "), 
          int(input("Enter the max image height (in pixels): ")),
          input("Enter the character's name: "), 
          input("Enter the character's origin: "),
          input("Enter the character's race: "),
          insert_br(input(f"Enter text file containing basic info (default is {textFolder}/basic.csg): "), f"{textFolder}/basic.csg", f"{tempFolder}/basicInfoTemp.txt"),
          insert_br(input(f"Enter text file containing other info (default is {textFolder}/other.csg): "), f"{textFolder}/other.csg", f"{tempFolder}/otherInfoTemp.txt"),
          insert_br(input(f"Enter text file containing combat info (default is {textFolder}/combat.csg): "),f"{textFolder}/combat.csg", f"{tempFolder}/combatInfoTemp.txt"),
          insert_br(input(f"Enter text file containing quotes (default is {textFolder}/quotes.csg): "), f"{textFolder}/quotes.csg", f"{tempFolder}/quotesTemp.txt"),
          insert_li(input(f"Enter text file containing trivia (default is {textFolder}/trivia.csg): "), f"{textFolder}/trivia.csg", f"{tempFolder}/triviaTemp.txt")
          )
    smallmenu(input("Do you want to create another sheet? [Y,N]: "))

#---------------------------------------------------
# Start the program and ask to download the CSS file
#---------------------------------------------------

ask_css()
main()