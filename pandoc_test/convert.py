import markdown

filename = '05---Omelet_##.md'

with open(filename, 'r') as f:

    ingrident_bool = bool()
    opskrift_bool = bool()
    text = f.read()
    new_text = str()

    for line in text.splitlines():

        # get heading, remove ## and spaces
        if '##' in line:
            tmp_header = line[2:].strip()
            heading = 'title: ' + '"{}"'.format(tmp_header)
        
        # get number of servings for either 1 number or a range a,b
        elif '*Til' and 'personer' in line:

            tmp_servering = list(filter(str.isdigit, line))

            if len(tmp_servering) == 1:

                tmp_servering = 'noOfServings: ' + str(tmp_servering[0]) + '/n'

            elif len(tmp_servering) == 2:

                tmp_servering = 'noOfServings: ' + str(tmp_servering[0]) + '-' + str(tmp_servering[1]) + '/n'

            else:

                tmp_servering = 'noOfServings: ' + '/n'
        
        elif '**Ingredienser**' in line:

             ingrident_bool = True
             tmp_ingredienser = '\tingredients:\n'

        elif '**Opskrift**' in line:

            ingrident_bool = False # list of ingredients is finished, this is used for next elif
            opskrift_bool = True
            tmp_opskrift = '---\n'
 
        elif ingrident_bool is True and line != '':

            tmp_ingredienser = tmp_ingredienser + '- ' + line + '\n' 

        elif opskrift_bool is True:

            ignore = ['*', '*\\']

            if line not in ignore:

                tmp_opskrift = tmp_opskrift + line + '\n'


new_text = tmp_header + 'draft: false\n' + 'weight: 1\n' + tmp_servering + tmp_ingredienser + tmp_opskrift
filename = filename[5:-6] + '.md'

with open(filename, 'w') as f:    
    f.write(new_text)