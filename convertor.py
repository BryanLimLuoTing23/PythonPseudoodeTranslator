import re

StringConcatenatorPattern = r'(?<=[a-zA-Z0-9_"\'\)])\s*\+\s*(?=[a-zA-Z0-9_"\'\()])'
#Detects the '+'. It checks it is not inside quotes, and is surrounded by variables, string literals, NOT numbers'

indentOpeners = {"if": ["IF", "ENDIF"], "while": ["WHILE", "ENDWHILE"], "else":["ELSE", ""]} #Openers start a new indentation. Then they must be closed



def python_line_to_pseudocode(line, lineIndex):
    global indentstack
    global python_lines_indentation
    global indentsOpened
    line = line.strip()  # Remove leading and trailing whitespaces
    #print(f"Current python line: {line}")
    indent = "    " * indentsOpened  # Indentation for pseudocode
    newline = ""




    if line.startswith("print(") and line.endswith(")"): #Print statements
        content = line[6:-1]
        newline = f"{indent}OUTPUT {content}"

    if "input(" in line and "=" in line:   #Input statements
        variable, right = line.split(" = ", 1)
        variable = variable.strip()
        right = right.strip()[6:-1] if right.strip().endswith(")") else right.strip()[6:]

        if not right: #If there is no string in the input method, then just return one line.
            newline = f"{indent}INPUT {variable}"
        else: #If there is a string message in the input method, then you have to output 2 lines.
            newline = f"{indent}OUTPUT {right}\n{indent}INPUT {variable}"

    if "int(input(" in line and "=" in line:   #Int input statements
        left, right = line.split("=", 1)
        left = left.strip()
        right = right.strip()[9:-2]
        newline = f"{indent}OUTPUT {right}\n{indent}INPUT {left}\n{indent}{left} <- STRING_TO_NUM({left})"

    if "=" in line and all(word not in line for word in indentOpeners): #Detect variable assignment in python, then change to <-
        left, right = line.split("=", 1)
        left = left.strip()
        right = right.strip()
        newline = f"{indent}{left} <- {right}"

    if line.startswith("if "): #Open an if statement
        condition = line[3:].replace("==", "=").replace(":", "")
        newline = f"{indent}IF {condition}\n{indent}    THEN "
        indentstack.append("if")

    if line == "else:":
        newline = f"{indent}ELSE"
        indentstack.append("else")




    #Detect string concatenator '+', then change to a comma
    line = re.sub(StringConcatenatorPattern, ', ', line)

    if lineIndex == len(python_lines_indentation)-1 and lineIndex>=1 and python_lines_indentation[lineIndex] >= 0 and not(any((line.strip()).startswith(word) for word in indentOpeners)): #Compare the current line's indent to the previous non-empty line to check if any indent has been closed
        linebackcounter = lineIndex-1
        while python_lines_indentation[linebackcounter] == -1:
            linebackcounter -= 1

        #Adding an ENDINDENT
        endIndents = []
        while python_lines_indentation[lineIndex] < python_lines_indentation[linebackcounter] and python_lines_indentation[lineIndex] < indentsOpened:
        #Find the last known line and compare the 2 indentations. The difference in indentations is the number of ENDINDENTS you add.
        #I.e. if the difference is 2 indents, you add 2 ENDINDENTS.

            indentsOpened -= 1
            print(f"indentsOpened decremented to {indentsOpened} at line {lineIndex+1}")
            newline = newline[4:]
            indent = indent[4:]

            print(f"LineIndex = {lineIndex}, indentsOpened = {indentsOpened}")
            currentIndentOpener = indentstack.pop()

            endIndent = indentOpeners[currentIndentOpener][1]
            endIndents.append(f"{indent}{endIndent}")

        endIndentsStr = "\n".join(endIndents)

            #Remove an indent from the line that has closed the indent
        if line != "" and endIndentsStr:

            newline = f"{endIndentsStr}\n{newline}"



    return newline


# Update the function to handle indentation and if-elif-else blocks
def python_to_pseudocode(python_code):
    global indentsOpened
    indentsOpened = 0
    global python_lines_indentation
    global indentstack
    indentstack = []

    python_lines_indentation = []
    python_lines = python_code.split("\n")
    pseudocode_lines = []




    for i in range(0,len(python_lines)):
        line = python_lines[i]

        #Count indentation if lines is not empty
        if line != "":
            spaces = 0
            while (line != "") and (line[spaces] == " "):
                spaces+= 1
            currentLineIndentation = spaces/4
            python_lines_indentation.append(currentLineIndentation)
        else:
            python_lines_indentation.append(-1)


        pseudocode_line = python_line_to_pseudocode(line, i)
        pseudocode_lines.append(pseudocode_line)

        if any((line.strip()).startswith(word) for word in indentOpeners): #If the line starts with an indent opener
            print(f"Indent opener Detected on line {i+1}")
            indentsOpened += 1
            print(f"indentsOpened = {indentsOpened}")
    #print(f"python_lines_indentation: {python_lines_indentation}")
    return "\n".join(pseudocode_lines)

with open ("test1.py", "r") as file:

    wholefile = file.read()
    #print(f"Python file: \n{wholefile} \n")

    print(f"\nPseudocode: \n{python_to_pseudocode(wholefile)}")



#Second pass to fix then indentations?
