import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

verbs_string = ''

manual_verbs = ["move", "get", "offer", "meet"]

line = 'Meet Mary at the bookcase, then find her in the dining room please'
    
text = nltk.word_tokenize(line)   

pos_tagged = nltk.pos_tag(text)

# print(pos_tagged)

pos_tagged2 = []

for pos in pos_tagged:
    if pos[0].lower() in manual_verbs:
        pos_tagged2.append([pos[0],'VB'])
    else:
        pos_tagged2.append(pos)

print(pos_tagged2)

print('')

verbs = filter(lambda x:x[1]=='VB' or x[1]=='VBP' or x[1]=='VBD',pos_tagged2)

for verb in verbs:
    verbs_string += verb[0] + ' | '
print(str(len(verbs)) + ' | ' + verbs_string + "- " + line)
# print(verbs)
