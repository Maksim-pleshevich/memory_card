#создай приложение для запоминания информации
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QRadioButton, QGroupBox, QButtonGroup, QMessageBox)
from random import shuffle, randint
#создание приложения и главного окна
class Question():
    def __init__(self, question, r_answer, w1, w2, w3):
        self.question =question
        self.r_answer = r_answer
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3

question_list = []
question_list.append(Question('Государственный язык Бразилии', 'Португальский', "Бразильский", "Испанский", "Итальянский"))
question_list.append(Question('Формула спирта', 'C2H5OH', 'C2H6OH', 'H2O', 'KOH'))
question_list.append(Question('Какое государство находится в столице Италии?', 'Ватикан', 'Кипр', 'Андорра', 'Мальта'))


app = QApplication([])

# главное окно
window = QWidget()
window.setWindowTitle("Memory Card")
window.resize(500, 300) #setFixedSize(500, 300)  
 
btn_OK = QPushButton("Ответить")
lb_Question = QLabel("В каком году была основана Москва?")
 
# Группа вариантов ответов
RadioGroupBox = QGroupBox("Варианты ответов")
r_1 = QRadioButton("1147")
r_2 = QRadioButton("1242")
r_3 = QRadioButton("1861")
r_4 = QRadioButton("1943")

RadioGroup = QButtonGroup() 
RadioGroup.addButton(r_1)
RadioGroup.addButton(r_2)
RadioGroup.addButton(r_3)
RadioGroup.addButton(r_4)

 
# Расположение ответов в группе
layout_ans1 = QHBoxLayout()
layout_ans2 = QVBoxLayout()
layout_ans3 = QVBoxLayout()
 
layout_ans2.addWidget(r_1)
layout_ans2.addWidget(r_2)
layout_ans3.addWidget(r_3)
layout_ans3.addWidget(r_4)
 
layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3)
 
RadioGroupBox.setLayout(layout_ans1)
 
# Группа результатов
AnsGroupBox = QGroupBox("Результаты теста")
lb_Result = QLabel("Правильно/Неправильно")
lb_Correct = QLabel("Правильный ответ")
 
layout_res = QVBoxLayout()
layout_res.addWidget(lb_Result, alignment=(Qt.AlignLeft | Qt.AlignTop))
layout_res.addWidget(lb_Correct, alignment=Qt.AlignHCenter, stretch=2)
AnsGroupBox.setLayout(layout_res)
 
layout_line1 = QHBoxLayout()
layout_line2 = QHBoxLayout()
layout_line3 = QHBoxLayout()
 
layout_line1.addWidget(lb_Question, alignment=(Qt.AlignHCenter | Qt.AlignVCenter))
 
layout_line2.addWidget(RadioGroupBox)
layout_line2.addWidget(AnsGroupBox)
#RadioGroupBox.hide() 
AnsGroupBox.hide()
 
layout_line3.addStretch(1)
layout_line3.addWidget(btn_OK, stretch=2)
layout_line3.addStretch(1)
 
# Главный слой
layout_card = QVBoxLayout()
layout_card.addLayout(layout_line1, stretch=2)
layout_card.addLayout(layout_line2, stretch=8)
layout_card.addStretch(1)
layout_card.addLayout(layout_line3, stretch=1)
layout_card.addStretch(1)
layout_card.setSpacing(5)
window.setLayout(layout_card)

def show_result():
    RadioGroupBox.hide()
    AnsGroupBox.show()
    btn_OK.setText('Следующий вопрос')

def show_question():
    RadioGroupBox.show()
    AnsGroupBox.hide()
    btn_OK.setText('Ответить')
    RadioGroup.setExclusive(False)
    r_1.setChecked(False)
    r_2.setChecked(False)
    r_3.setChecked(False)
    r_4.setChecked(False)
    RadioGroup.setExclusive(True)

def start_test():
    if 'Ответить' == btn_Ok.text():
        show_result()
    else:
        show_question()

answers = [r_1, r_2, r_3, r_4]

def ask(q: Question):
    shuffle(answers)
    answers[0].setText(q.r_answer)
    answers[1].setText(q.w1)
    answers[2].setText(q.w2)
    answers[3].setText(q.w3)
    lb_Question.setText(q.question)
    lb_Correct.setText(q.r_answer)
    show_question()

def show_correct(res):
    lb_Result.setText(res)
    show_result()

def check_answer():
    if answers[0].isChecked():
        show_correct('Правильно!')
        window.score += 1
        print(f"Статистика:\n-Всего вопросов: {window.total}\n-Правильных ответов: {window.score}\n")
        print(f"Рейтинг: {round(window.score / window.total * 100, 2)}%")
    else:
        if answers[1].isChecked() or answers[2].isChecked() or answers[3].isChecked():
            show_correct('Неверно!')
            print(f"Рейтинг: {round(window.score / window.total * 100, 2)}%")

def next_question():
    if len(question_list) > 0:
        window.total += 1
        print(f"Статистика: \nВсего вопросов: {window.total}\nПравильный ответов: {window.score}")
        cur_question = randint(0, len(question_list) - 1)
        q = question_list[cur_question]
        question_list.remove(q)
        ask(q)
    else:
        show_statistics()

def show_statistics():
    msg = QMessageBox()
    msg.setWindowTitle("Статистика и рейтинг")
    msg.setText(f'Статистика:\n-Всего вопросов: {window.total}\n-Правильных ответов: {window.score}\n'
                f'Рейтинг: {round(window.score / window.total * 100, 2)}%')
    msg.exec()
    app.quit()
        
def click_OK():
    if btn_OK.text() == 'Ответить':
        check_answer()
    else:
        next_question()

btn_OK.clicked.connect(click_OK)

window.score = 0
window.total = 0

next_question()
window.show()
app.exec()