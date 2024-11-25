# Парсинг PEP

## Описание проекта
**bs4_parser_pep** - это проект парсера, который собирает информацию о всех документах PEP, указывает и сравнивает их статусы, а также выводит результаты в терминал, сохраняет в файл или архив.

## Основные особенности проекта
- сбор и формирование ссылок на новинки в Python;
- сбор информации о версиях Python;
- формирование архива с документацией;
- сбор и подсчет статусов документов PEP;
- вывод информации в терминал, сохранение результатов работы в формате csv;
- логирование и обработка ошибок;

## Запуск проекта

```bash
git clone https://github.com/YroslavBochkov/bs4_parser_pep.git
cd backend
```
### Создайте и активируйте виртуальное окружение:
#### Для Linux/macOS:
```bash
python3 -m venv env
source env/bin/activate
```
#### Для Windows:
```bash
python3 -m venv env
source env/scripts/activate
```
#### 3. Обновите pip и установите зависимости:
```bash
python3 -m pip install --upgrade pip
pip install -

# Работа с парсером

### Режимы работы
Сброр ссылок на статьи о нововведениях в Python:
```bash
python main.py whats-new
```
Сброр информации о версиях Python:
```bash
python main.py latest-versions
```
Скачивание архива с актуальной документацией:
```bash
python main.py download
```
Сброр статусов документов PEP и подсчёт статусов:
```bash
python main.py pep
```

## Технологии
[![Python](https://img.shields.io/badge/Python-3.7-blue?style=flat-square&logo=Python&logoColor=3776AB&labelColor=d0d0d0)](https://www.python.org/)
[![Beautiful Soup 4](https://img.shields.io/badge/BeautifulSoup-4.9.3-blue?style=flat-square&labelColor=d0d0d0)](https://beautiful-soup-4.readthedocs.io)

### Автор

Ярослав Бочков
