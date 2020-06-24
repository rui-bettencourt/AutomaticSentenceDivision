# import 

read_file  = open('gpsr.txt', 'r')
write_input_file = open('dataset_input.txt', 'w')
write_output_file = open('dataset_output.txt', 'w')

number_of_line = 0
for line in read_file:
    # print(line)
    #INPUT for neural network
    text_without_comas = line.replace(',', '')
    write_input_file.write(text_without_comas)
    # print(text_without_comas)
    
    #OUTPUT for neural network
    text_splitted = line.replace(' ,',',').replace(', and ',' and ').replace('and ', ', ').replace('\n','').split(', ')
    
    output_string = ''
    i = 0
    n_sentences = len(text_splitted)
    for unit in text_splitted:
        output_string += unit
        i += 1
        if i<n_sentences:
            output_string += " | "
        else:
            output_string += '\n'
            
    write_output_file.write(output_string)
    number_of_line += 1
    print("Iter: " + str(number_of_line))
    # print(text_splitted)
    # print("---------------\n")