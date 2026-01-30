from html.entities import html5
from sys import argv
import re
import yaml

with open('settings.yaml', 'r') as f:
    settings = yaml.safe_load(f)
    
RESULT_FILE = settings['RESULT_FILE']
DELIMITER = settings['DELIMITER']



# merge the two lines lists

def generate_new_lines(lines1: list, lines2: list, html_mode = False) -> list:
    if html_mode:
        lines3 = [f"{lines1[i].replace('\n', '')}\n{lines2[i].replace('\n', '')}\n{DELIMITER}\n" for i in range(len(lines1))]
    else:
        lines3 = [f"<p>{lines1[i].replace('\n', '')}</p>\n<p>{lines2[i].replace('\n', '')}</p>\n{DELIMITER}\n" for i in range(len(lines1))]

    return lines3[:-1] + [lines3[-1].replace(f"\n{DELIMITER}\n", "")]

# replace the HTML characters, erase the spaces before "."

def correct_line(line: str) -> str:
    # replace all HTML chars, e.g. "&#x142;" => "ł"

    for entity in html_entities:
        line = line.replace(entity, html_entities[entity])
    
    # replace " ."  (EOL) with "."
    # replace " . "       with ". "
    
    if ' .' in line:
        r1 = r'[ ]*\.[ ]'
        r2 = r'[ ]*\.$'
        
        line = re.sub(r1, '. ', line)
        line = re.sub(r2, '.', line)
        
    return line

# delete all tags except <p>, <h1>, <h2>, <h3>

def delete_useless_tags(text:str) -> str:
    text = re.sub("<[^p|h|\/].*?>", "", text)
    text = re.sub("<\/[^p|h|\/].*?>", "", text)
    return text

# delete all tag attributes

def delete_tag_attributes(text: str) -> str:
    text = re.sub("<p.*?>", "<p>", text)
    text = re.sub("<h1.*?>", "<h1>", text)
    text = re.sub("<h2.*?>", "<h2>", text)
    text = re.sub("<h3.*?>", "<h3>", text)
    return text

def extract_hx_and_paragraphs(text: str) -> list:
    return re.findall("<[p|h].*?>.*?<\/[p|h].*?>", text)
    
    
if __name__ == "__main__":

    # test if arguments were added
    try:
        filename1 = argv[1]
        filename2 = argv[2]
    except:
        print("Enter two filenames as arguments.")
        exit()
        
    # test if the mentioned files exist
    try:
        with open(filename1, "r") as f:
            lines1 = f.readlines() 
    except:
        print(f"{filename1} does not exist.")
        exit()
    try:
        with open(filename2, "r") as f:
            lines2 = f.readlines() 
    except:
        print(f"{filename2} does not exist.")
        exit()
    
    # check if the files are empty
    
    if len(lines1) == 0:
        print(f"{filename1} is empty.")
        exit()
    elif len(lines2) == 0:
        print(f"{filename2} is empty.")
        exit()
    
    html_mode = "html" in argv[3:]
    
    # not in HTML mode
    
    if not html_mode:
        if len(lines1) != len(lines2):
            print("The two files don't have the same number of lines.")
            exit()
    
    # in HTML mode

    else:
        with open(filename1, "r") as f:
            text1 = f.read() 
        with open(filename2, "r") as f:
            text2 = f.read()
        
        text1 = delete_useless_tags(text1)
        text2 = delete_useless_tags(text2)

        text1 = delete_tag_attributes(text1)
        text2 = delete_tag_attributes(text2)
        
        lines1 = extract_hx_and_paragraphs(text1)
        lines2 = extract_hx_and_paragraphs(text2)

    lines3 = generate_new_lines(lines1, lines2, html_mode = html_mode)

    with open(RESULT_FILE, "w") as f:
        f.writelines(lines3)