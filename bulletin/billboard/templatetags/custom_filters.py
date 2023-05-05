from django import template

register = template.Library()


@register.filter(name='Censor')
def Censor(value):
    banned_list = ['idiot', 'stupid', 'Idiot', 'Stupid']
    sentence = value.split()
    for i in banned_list:
        for words in sentence:
            if i in words:
                pos = sentence.index(words)
                sentence.remove(words)
                sentence.insert(pos, '*' * len(i))
    return " ".join(sentence)