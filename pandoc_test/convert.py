import markdown
import os

def convert_format_index(path, root, filename, save):
    
    with open(path, 'r') as f:

        text = f.read()
        tmp_opskrift = '---\n'

        for line in text.splitlines():

            # get heading, remove ## and spaces
            if '#' in line:

                tmp_header = line[2:].strip()
                tmp_header = 'title: ' + '"{}"'.format(tmp_header)

            elif line != '' or (line == '' and tmp_opskrift[-1:] != '\n'): # avoid double new lines

                tmp_opskrift = tmp_opskrift + line + '\n'

        new_text = '---\n' + tmp_header + '\n' + 'draft: false\n' + 'weight: 1\n' + tmp_opskrift

        # new_filename = filename[5:-5] + '.md'
        new_filename = '_index.md'
        new_filename = os.path.join(root, new_filename)

    if save is True:

        with open(new_filename, 'w') as f:    
            f.write(new_text)

        os.remove(path)
        
    return


def convert_format_recipe(path, root, filename, save):

    with open(path, 'r') as f:

        ingrident_bool = bool()
        incl_servering = False
        visited_ingredients = False
        opskrift_bool = bool()
        text = f.read()

        for line in text.splitlines():

            # get heading, remove ## and spaces
            if '##' in line and '###' not in line:
                tmp_header = line[2:].strip()
                tmp_header = 'title: ' + '"{}"'.format(tmp_header) # check is this works 
            
            # get number of servings for either 1 number or a range a,b
            elif '*Til' in line:

                incl_servering = True

                tmp_servering = list(filter(str.isdigit, line))

                if len(tmp_servering) == 1:

                    tmp_servering = 'noOfServings: ' + str(tmp_servering[0]) + '\n'

                elif len(tmp_servering) == 2:

                    tmp_servering = 'noOfServings: ' + str(tmp_servering[0]) + '-' + str(tmp_servering[1]) + '\n'

                else:

                    tmp_servering = 'noOfServings: ' + '\n'
            
            elif '**Ingredienser**' in line:
                
                visited_ingredients = True
                ingrident_bool = True
                tmp_ingredienser = 'ingredients:\n'

            elif '**Opskrift**' in line:

                ingrident_bool = False # list of ingredients is finished, this is used for next elif
                opskrift_bool = True
                tmp_opskrift = '---\n'
    
            elif ingrident_bool is True and line != '':

                tmp_ingredienser = tmp_ingredienser + '\t'+ '- ' + line + '\n' 

            elif opskrift_bool is True:

                ignore = ['*', '*\\']

                if line not in ignore:

                    tmp_opskrift = tmp_opskrift + line + '\n'

    if incl_servering is False: #some recipes don't include explicit for serverings 

        tmp_servering = 'noOfServings: ' + '\n'
    
    if visited_ingredients is False: 

        tmp_ingredienser = '\tingredients:\n'

    new_text = '---\n' + tmp_header + '\n' + 'draft: false\n' + 'weight: 1\n' + tmp_servering + tmp_ingredienser + tmp_opskrift

    new_filename = filename[5:-6] + '.md'
    new_filename = os.path.join(root, new_filename)


    if save is True:

        with open(new_filename, 'w') as f:    
            f.write(new_text)

        os.remove(path)

    return 


def update_format(path, root, filename):

    save = True # toggle to save outputs 

    # check if the file is recipe
    try:

        with open(path, 'r') as f:

            try: 

                text = f.read()

            except UnicodeDecodeError as e:

                print('{} on {}'.format(e, filename))
                return

            # check if already updated

            if '-' not in filename:
                print('{} was ignored'.format(filename))
                return

            if '**Opskrift**' in text:

                convert_format_recipe(path, root, filename, save)

            elif '#' in text:

                convert_format_index(path, root, filename, save)

            else:

                return

    except FileNotFoundError as e:

        print('{} on {}'.format(e, filename))
        return 

    return

def rename_folders(dir):

    for root, subdirs, files in os.walk(dir):

        for subdir in subdirs:
            
            first_character_passed = False
            new_name = str()
            for char in subdir:

                if str(subdir[0]).isnumeric() is False:

                    continue # don't treat folders already renamed 

                if char != '-' and char.isnumeric() is False:

                    new_name = new_name + char.lower()
                    first_character_passed = True
                 
                elif char == '-' and first_character_passed is True:

                    new_name = new_name + '_' #replace - with space in line

                else:

                    pass
                      
            old_path = os.path.join(root, subdir)
            new_path = os.path.join(root, new_name)
            os.rename(old_path, new_path)
    
    return


if __name__ == "__main__":

    dir = r'/Users/lau/OneDrive/KogebogRepo/kogebog/pandoc_test/output_copy'

    rename_folders(dir)

    for root, subdirs, files in os.walk(dir):

        for file in files:

            path = os.path.join(root, file)
            update_format(path, root, file)


    
    

            


