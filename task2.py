"""
Задача №2.

В нашей школе мы не можем разглашать персональные данные пользователей, но чтобы преподаватель и ученик смогли объяснить
 нашей поддержке, кого они имеют в виду (у преподавателей, например, часто учится несколько Саш), мы генерируем
  пользователям уникальные и легко произносимые имена. Имя у нас состоит из прилагательного, имени животного и
   двузначной цифры. В итоге получается, например, "Перламутровый лосось 77". Для генерации таких имен мы и решали
    следующую задачу:
Получить с русской википедии список всех животных (https://inlnk.ru/jElywR) и вывести количество животных на каждую
 букву алфавита. Результат должен получиться в следующем виде:
А: 642
Б: 412
В:....
"""
from requests import get
from bs4 import BeautifulSoup
import pymorphy2


res = get('https://inlnk.ru/jElywR').text
soup = BeautifulSoup(res, 'html.parser')
morph = pymorphy2.MorphAnalyzer()
result = {}
f = soup.find('a', text='Следующая страница')
flag = True
while f and flag:
    t = soup.find('div', attrs={'id': 'mw-pages'})
    for num, tag in enumerate(t.find_all('li')):
        animal = tag.a.text
        if ord(animal[0].lower()) < 1072:
            flag = False
            break
        upp = []
        for word in animal.split():
            wall = morph.parse(word)[:2]
            w = morph.parse(word)[0]
            w_norm = w.normalized
            if not (w.tag.POS == 'ADJF' or w.word.endswith(('ая', "ый", 'ья', 'ий')) or w.word.startswith('(')):
                if w.tag.POS == 'NOUN' and w.tag.animacy in ['anim', 'inan'] and w.word.endswith(('ы', 'и')):
                    add1 = w_norm.word
                else:
                    add1 = w.word

                if add1[0] not in result.keys():
                    result[add1[0]] = set([add1])
                else:
                    result[add1[0]].add(add1)
                break
    res = get('https://ru.wikipedia.org' + f['href']).text
    soup = BeautifulSoup(res, 'html.parser')
    f = soup.find('a', text='Следующая страница')

for char in sorted(result.keys()):
    print(f'{char.upper()}: {len(result[char])}')

