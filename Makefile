VENV_NAME = .venv

ifeq ($(OS),Windows_NT)
    #Windows
    PYTHON = python
    VENV_ACTIVATE = $(VENV_NAME)\Scripts\activate
    PYTHON_RUN = $(VENV_NAME)\Scripts\python
    PIP = $(VENV_NAME)\Scripts\python -m pip
    RM = rd /s /q
    RUN_CMD = $(PYTHON_RUN) main.py
else
    #macOS/Linux
    PYTHON = python3
    VENV_ACTIVATE = source $(VENV_NAME)/bin/activate
    PYTHON_RUN = $(VENV_NAME)/bin/python
    PIP = $(VENV_NAME)/bin/python -m pip
    RM = rm -rf
    RUN_CMD = $(PYTHON_RUN) main.py
endif

install:
	   @echo "Создание виртуального окружения"
	   @$(PYTHON) -m venv $(VENV_NAME)
	   @echo "Установка зависимостей"
	   @$(PIP) install --upgrade pip
	   @$(PIP) install -r requirements.txt

run:
	   @echo "Запуск сервиса"
ifeq ($(OS),Windows_NT)
	   @cmd /c "$(VENV_ACTIVATE) && $(PYTHON_RUN) main.py"
else
	   @bash -c "$(VENV_ACTIVATE) && $(PYTHON_RUN) main.py"
endif

test:
	   @echo "Запуск тестов"
ifeq ($(OS),Windows_NT)
	   @cmd /c "$(VENV_ACTIVATE) && $(PYTHON_RUN) -m pytest -v tests/"
else
	   @bash -c "$(VENV_ACTIVATE) && $(PYTHON_RUN) -m pytest -v tests/"
endif