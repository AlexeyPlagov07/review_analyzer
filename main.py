import sqlite3
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
#cursor.execute("CREATE TABLE data (review TEXT, p_n TEXT)")
#conn.commit()

insert_query = "INSERT INTO data VALUES (?,?)"



def clean_text(text):
    text = list(text)
    for i in range(len(text)):
        try:
            if text[i] == "." or text[i] == "," or text[i] == "?" or text[i] == "!" or text[i] == "\'" or text[i] == "(" or text[i] == ")" or type(text[i]) == int or text[i] == "%" or text[i] == ":" or text[i] == "&":
                text.pop(i)
        except IndexError:
            pass
    return (''.join(text)).lower()
word_dict = {}
positive_word_count = {}
negative_word_count = {}


def machine_learn(text):
    if text[1] == "positive":   
        for i in (clean_text(text[0])).split():
            if i not in word_dict:
                word_dict[i] = (len(word_dict) + 1)
            if word_dict[i] in positive_word_count.keys():
                positive_word_count[word_dict[i]] = positive_word_count[word_dict[i]] + 1
            else:
                positive_word_count[word_dict[i]] = 1
    elif text[1] == "negative":
        for i in (clean_text(text[0])).split():
            
            if i not in word_dict:
                word_dict[i] = (len(word_dict) + 1)
            if word_dict[i] in negative_word_count.keys():
                negative_word_count[word_dict[i]] = negative_word_count[word_dict[i]] + 1
            else:
                negative_word_count[word_dict[i]] = 1


cursor.execute("SELECT * FROM data")
result1 = list(cursor.fetchall())

for i in result1:
    machine_learn(list(i))

def clean_lists(p_l, n_l):
    temp_list = (set(p_l) & set(n_l))
    for i in list(temp_list):
        p_l.pop(i)
        n_l.pop(i)
    
clean_lists(positive_word_count, negative_word_count)


test_text = "It's dunks so.... It was wicked awesome"
test_machine = (clean_text(test_text))


def convert_text(tt):
    temp_list = []
    tt = tt.split()
    for i in tt:
        if i in word_dict.keys():
            temp_list.append(word_dict[i])
    return temp_list
def machine_test(p_l, n_l, tt):
  
    pos_set = set(list(p_l.keys())) & set(convert_text(tt))
    neg_set = set(list(n_l.keys())) & set(convert_text(tt))
    
    if len(pos_set) > len(neg_set):
        return "positive"
    elif len(neg_set) > len(pos_set):
        return "negative"
    else:
        return "neutral"


cursor.execute("SELECT * FROM data")
result1 = list(cursor.fetchall())
print(result1)

output = (machine_test(positive_word_count, negative_word_count, test_machine))
print(output)
correct = input("Correct?(y/n): ")

if correct == 'y':
    cursor.execute(insert_query, (test_text, output))
    conn.commit()
elif correct == "n":
    if output == "positive":
        output = "negative"
    elif output == "negative":
        output = "positive"
    cursor.execute(insert_query, (test_text, output))
    conn.commit()
elif correct == " positive":
    output = "positive"
    cursor.execute(insert_query, (test_text, output))
    conn.commit()
elif output == "negative":
    output = "negative"
    cursor.execute(insert_query, (test_text, output))
    conn.commit()

