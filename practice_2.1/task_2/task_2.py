students_data = [
    "Иванов Иван:5,4,3,5",
    "Петров Петр:4,3,4,4",
    "Сидорова Мария:5,5,5,5"
]

with open('../resource/students.txt', 'w', encoding='utf-8') as f:
    for student in students_data:
        f.write(student + '\n')

students = []
with open('../resource/students.txt', 'r', encoding='utf-8') as f:
    for line in f:
        name, grades_str = line.strip().split(':')
        grades = list(map(int, grades_str.split(',')))
        avg = sum(grades) / len(grades)
        students.append((name, avg, grades))

with open('../resource/result.txt', 'w', encoding='utf-8') as f:
    for name, avg, _ in students:
        if avg > 4.0:
            f.write(f"{name}:{avg:.2f}\n")

best = max(students, key=lambda x: x[1])
worst = min(students, key=lambda x: x[1])

print(f"Студент с наивысшим баллом: {best[0]} ({best[1]:.2f})")
print(f"Студент с низким баллом: {worst[0]} ({worst[1]:.2f})")
print("\nСтуденты со средним баллом > 4.0 сохранены в result.txt")