import nltk
from textblob import TextBlob

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

file  = open('/home/rui/gpsr.txt', 'r')
write_file = open('/home/rui/gpsr_stats.txt', 'w')

verbs_string = ''
blob_verbs_string = ''

manual_verbs = ["move", "get", "offer", "meet"]

for line in file:

    text = nltk.word_tokenize(line)
    blob = TextBlob(line)   

    pos_tagged = nltk.pos_tag(text)
    # print(pos_tagged)
    
    blob_tags = blob.tags
    print(blob_tags)
    print(blob.noun_phrases)
    for sentence in blob.sentences:
        print(sentence.sentiment.polarity)
    print(blob.translate(to="pt"))

    pos_tagged2 = []

    for pos in pos_tagged:
        if pos[0].lower() in manual_verbs:
            pos_tagged2.append([pos[0],'VB'])
        else:
            pos_tagged2.append(pos)
    # print(pos_tagged2)

    verbs = filter(lambda x:x[1]=='VB' or x[1]=='VBP' or x[1]=='VBD',pos_tagged2)
    
    verbs_blob = filter(lambda x:x[1][0]=='V',blob_tags)

    print(len(verbs))
    for verb in verbs:
        verbs_string += verb[0] + ' | '
    for verb in verbs_blob:
        blob_verbs_string += verb[0] + ' | '
    
    write_file.write(str(len(verbs)) + ' | ' + verbs_string + "- " + str(len(verbs_blob)) + ' | ' + blob_verbs_string + '- ' + line)
    # print(verbs)
    verbs_string = ''
    blob_verbs_string = ''
    
file.close()
write_file.close()