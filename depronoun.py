#
from nltk.tokenize import word_tokenize
from xml.dom import minidom
import progressbar
from time import sleep

input_file = 'data/dataset_output.txt'
num_lines = sum(1 for line in open(input_file))

read_file  = open(input_file, 'r')
write_output_file = open('data/dataset_output_no_pronouns.txt', 'w')

pronouns = ['him','her']
pronouns_objects = ['it']
names = []
objects = []
special_objects = []
pronoun_error_counter_p = 0
pronoun_error_counter_o = 0
pronoun_misplacements = 0

# parse an xml file by name
mydoc_names = minidom.parse('Names.xml')
mydoc_objects = minidom.parse('Objects.xml')

names_raw = mydoc_names.getElementsByTagName('name')
for elem in names_raw:
    names.append(elem.firstChild.data)

objects_raw = mydoc_objects.getElementsByTagName('object')
category_raw =  mydoc_objects.getElementsByTagName('category')
for elem in objects_raw:
    if ' ' not in elem.attributes['name'].value:
        objects.append(elem.attributes['name'].value)
    else:
        complex_word = []
        for word in elem.attributes['name'].value.split(' '):
            complex_word.append(word)
        special_objects.append(complex_word)
for elem in category_raw:
    if ' ' not in elem.attributes['name'].value:
        objects.append(elem.attributes['name'].value)
    else:
        complex_word = []
        for word in elem.attributes['name'].value.split(' '):
            complex_word.append(word)
        special_objects.append(complex_word)

names.sort()
objects.sort()

print("The availabe names are: ")
print(names)
print("\n\n")

print("The availabe objects are: ")
print(objects)
print("\n\n")

print("The availabe special objects are: ")
print(special_objects)
print("\n\n")


bar = progressbar.ProgressBar(maxval=num_lines, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()

##### Actual code
i = 0
for line in read_file:
    i += 1
    used_name = None
    used_object = None
    words = word_tokenize(line)
    
    if any(pronoun in words for pronoun in pronouns):
        #Loop the tokenized line for the pronoun and name
        for word in words:
            if word in names:
                used_name = word

            if word in pronouns and used_name is not None:
                #if a pronoun was found and previously also a name, replace that pronoun by the name
                words[words.index(word)] = used_name
            elif word in pronouns and used_name is None:
                print("PRONOUN WITH NO NAME!")
                pronoun_error_counter_p += 1
    
    if any(pronoun in words for pronoun in pronouns_objects):
        #Loop the tokenized line for the pronoun and object
        for word in words:
            if word in objects:
                used_object = word
            if word in names:
                used_name = word
            
            if word in pronouns_objects and used_object is not None:
                words[words.index(word)] = "the " + used_object

            elif word in pronouns_objects and used_object is None:
                # print("PRONOUN WITH NO NAME!")
                success = False
                for special in special_objects:
                    correct_special = True
                    for item in special:
                        if item not in words:
                            correct_special = False
                            break
                    if correct_special:
                        to_add = ' '.join(special)
                        words[words.index(word)] = "the " + to_add  
                        success = True
                if not success and used_name is not None:
                    words[words.index(word)] = used_name
                    pronoun_misplacements += 1
                elif not success:
                    pronoun_error_counter_o += 1

    #Write the output into a file
    write_output_file.write(' '.join(words).replace(' .','.') + '\n')
    # print("Iter: " + str(i))
    bar.update(i)

bar.finish()
print("Success! With " + str(pronoun_error_counter_p) + " sentences that had a pronoun but no name and " + str(pronoun_error_counter_o) + " with no object.")
print("A total of " + str(pronoun_misplacements) + " were considered as pronoun misplacements and the it was replace by a name")
