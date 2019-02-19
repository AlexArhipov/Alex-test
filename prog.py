import sys
import os
import urllib.parse
import urllib.request
from html.parser import *
import textwrap


class myHtmlParser(HTMLParser): #класс для обработки исходного кода html страницы

    def __init__(self, **kwargs):
         super().__init__()
         self.maxlen=80 # максимальная длинна строки
         self.textc=[] #список параграфов
         self.recording = False #флаг записи информации
         self.href = 0    #атирбут флага ссылки
         self.fl = 0      #флаг ссылки
         self.links = ""  #ссылка

    def translete(self): # преобразование HTML страницы в текстовый блок
        textin=[] #обнуление переменных
        wrtext=''
        textout=''
        for parag in self.textc:
            textin.append(''.join(parag)) # получение списка параграфов
        for parag in textin:
            if parag[-1]!='f': #контроль фалга параграфа с ссылкой
                wrtext+=parag # добавляем к текущему параграфу параграф с ссылкой
                textout += "\n".join(textwrap.wrap(wrtext, self.maxlen)) + "\n\n" # формируем конечный файл
                wrtext=''
            else:
                wrtext=parag[:-1] # убираем флаг параграфа с сыылкой и запоминаем во временную переменную
        return textout # возвращаем сформированый файл

    def handle_starttag(self, tag, attrs): # проверка и определение открытого тегоа
         if tag == 'title': # проверка на заголовок
             self.recording = True
         if tag == 'p': # проверка на текст
             self.recording = True
         if tag == 'a': # проверка на ссылку
             if self.recording == True :
                 self.href=1
                 # находим аттрибут адреса ссылки
                 for attr in attrs:
                     if attr[0] == 'href': # проверка что атрибут содержит ссылку
                         self.links = attr[1] #получание адреса ссылки
         if (tag != 'p'and tag != 'title' and self.recording == True):
             self.fl = 1 # флаг ссылки

    def handle_endtag(self, tag): # проверка и определение зактрытого тега
        if tag == 'title':# проверка на заголовок
            self.recording = False
        if tag == 'p': # проверка на текст
            self.recording = False
        if tag == 'a': # проверка на ссылку
            if self.recording == True :
        #     if self.recording == False :
                self.href=0
        if (tag != 'p' and tag != 'title' and self.recording == True):
            self.fl = 0 # флаг ссылки

    def handle_data(self, data):# обработка инофрмации между тегами
        if self.recording: # проверка что можно заносить параграф в список
            if self.href==1:  # является ли элемент ссылкой
                self.textc.append("["+self.links+"] "+data+'f')# внесение ссылки в словарь параграфов
            else :
                if self.fl!= 1: # если не является ссылкой
                    self.textc.append(data) #внесение текста в словарь параграфов

class CreateFiles(): # класс для создания и сохранения файла с полезной информацией

    def __init__(self, **kwargs):
         self.__url1=''  # ссылка на страницу сайта

    def extractHTML(self, url1): # получение данных с HTML страницы
        resource = urllib.request.urlopen(url1)#получение исходного кода страницы
        content =  resource.read().decode(resource.headers.get_content_charset()) #кодировка странцы для понимания её питоном

        SaveText=myHtmlParser() # создание экземплюяра класса
        SaveText.feed(content) # передача исходного кода
        SaveText.close()
        textout_f=SaveText.translete() # вызов метода обработки информации

        result_parse = urllib.parse.urlparse(url1) # получаем адрес ссылки и домен сайта
        hostname = result_parse.hostname #получаем домен сайта
        path = result_parse.path#получаем url который идет после домена
        if path[-1] == "/":  # убираем слеши первый и последний
            path = path[1:-1]
        path_items = path.split('/') # делаем разбивку на список
        source_name = path_items[-1] # получаем имя статьи
        file_name = source_name+'.txt'# дабавляем расширение файла
        # Формирование пути сохранения файла.
        relative_path = hostname + "/" + "/".join(path_items[0:-1]) #  формируем из списка директорию для сохранения
        if not os.path.exists(relative_path): #  проверка существует ли задаваемая директория
            os.makedirs(relative_path) #  создаем директорию
        # Запись в файл.
        f = open(relative_path + "/" + file_name, 'w', encoding='utf-8') # создаем файл в с уканием директории
        f.write(textout_f) #  вносим преобразованный текст
        f.close() # закрываем файл

if len(sys.argv)>1: # проверка на ввод ссылки на страницу
     url1=sys.argv[1] # передаем в переменную адрес сайта
else:
     url1="Ссылка не введена"
html1=CreateFiles()
html1.extractHTML(url1)
