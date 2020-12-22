class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecturer(self, lecturer, grade):
        if isinstance(lecturer, Lecturer) and len(set(self.courses_in_progress).intersection(lecturer.courses_attached)) > 0:
            lecturer.grades.append(grade)
        else:
            # print('Нет общих курсов')
            return 'Ошибка'

    def get_avg_grade(self):
        grade_avg = 0
        avg_course = []

        if len(self.grades) > 0:
            for grade in self.grades.values():
                avg = sum(grade) / len(grade)
                avg_course.append(avg)
            grade_avg = round(sum(avg_course) / len(avg_course), 2)

        return grade_avg

    def __str__(self):
        return f'Имя: {self.name} \n' \
               f'Фамилия: {self.surname} \n' \
               f'Средняя оценка за домашне задания: {self.get_avg_grade()} \n' \
               f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)} \n' \
               f'Завершенные курсы: {", ".join(self.finished_courses)} \n'

    def __lt__(self, other):
        if not isinstance(other, Student):
            print('Не студент')
            return

        return self.get_avg_grade() < other.get_avg_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = []

    def get_avg_grade(self):
        grade_avg = 0

        if len(self.grades) > 0:
            grade_avg = round(sum(self.grades) / len(self.grades), 2)

        return grade_avg

    def __str__(self):
        return f'Имя: {self.name} \n' \
               f'Фамилия: {self.surname} \n' \
               f'Средняя оценка за лекции: {self.get_avg_grade()} \n' \

    def __lt__(self, other):
        if not isinstance(other, Mentor):
            print('Не ментор')
            return

        return self.get_avg_grade() < other.get_avg_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f'Имя: {self.name} \n' \
               f'Фамилия: {self.surname} \n' \


lecturer_1 = Lecturer('Some', 'Buddy')
lecturer_2 = Lecturer('Lect', 'Urer')
reviewer_1 = Reviewer('Another', 'Man')
reviewer_2 = Reviewer('Rev', 'Ewer')
student_1 = Student('Ruoy', 'Eman', 'your_gender')
student_2 = Student('Stu', 'Dent', 'your_gender')

student_1.courses_in_progress += ['Python', 'Go']
student_2.courses_in_progress += ['Python']
lecturer_1.courses_attached += ['Python', 'Git']
lecturer_2.courses_attached += ['Python']
reviewer_1.courses_attached += ['Python', 'Git']
reviewer_2.courses_attached += ['Python']

student_1.rate_lecturer(lecturer_1, 10)
student_1.rate_lecturer(lecturer_1, 9)
student_2.rate_lecturer(lecturer_1, 6)
student_2.rate_lecturer(lecturer_2, 5)

reviewer_1.rate_hw(student_1, 'Python', 10)
reviewer_1.rate_hw(student_1, 'Python', 9)
reviewer_2.rate_hw(student_1, 'Python', 7)
reviewer_2.rate_hw(student_2, 'Python', 7)

print(student_1)
print(lecturer_1)
print(reviewer_1)
print(reviewer_1)
print(student_1 > student_2)
print(lecturer_1 < lecturer_2)

# best_student = Student('Ruoy', 'Eman', 'your_gender')
# best_student.courses_in_progress += ['Python']
#
# cool_mentor = Mentor('Some', 'Buddy')
# cool_mentor.courses_attached += ['Python']
#
# cool_mentor.rate_hw(best_student, 'Python', 10)
# cool_mentor.rate_hw(best_student, 'Python', 10)
# cool_mentor.rate_hw(best_student, 'Python', 10)
#
# print(best_student.grades)