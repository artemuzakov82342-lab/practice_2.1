lines = [
    "Python крутая темка",
    "Нормалдаки или плаки плаки",
    "Программирование убивает мышление",
    "В лесу родилась елочка",
    "Hello world! This is a test"
]

with open('../resource/text.txt', 'w', encoding='utf-8') as f:
    for line in lines:
        f.write(line + '\n')

with open('../resource/text.txt', 'r', encoding='utf-8') as f:
    content = [line.rstrip('\n') for line in f.readlines()]

print(f"Строк: {len(content)}")

words = sum(len(line.split()) for line in content)
print(f"Слов: {words}")

longest = max(content, key=len)
print(f"Самая длинная строка ({len(longest)} симв.): {longest}")

vowels = set('аеёиоуыэюяaeiou')
consonants = set('бвгджзйклмнпрстфхцчшщъьbcdfghjklmnpqrstvwxyz')

text = ' '.join(content).lower()
v_count = sum(1 for c in text if c in vowels)
c_count = sum(1 for c in text if c in consonants)

print(f"Гласных: {v_count}, Согласных: {c_count}")