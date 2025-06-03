text = '1:23.45'

if ':' in text:

    text = text.replace(':','.')

    text = text.split('.')



print(text)
