ENVIRONMENT ?= dev
APPLICATION_NAME=restaurants-backend

PYTHON_VERSION=3.6.5
VIRTUALENV=~/.pyenv/versions/$(PYTHON_VERSION)/bin/virtualenv
PIP=~/.pyenv/versions/$(PYTHON_VERSION)/bin/pip
VENV_NAME=venv

init:
	# pyenv, virtualenv and requirements init
	test -d ~/.pyenv/versions/$(PYTHON_VERSION) || pyenv install $(PYTHON_VERSION)
	test -d $(PIP) || $(PIP) install virtualenv
	test -d $(VIRTUALENV) || $(PIP) install virtualenv
	test -d $(VENV_NAME) || $(VIRTUALENV) $(VENV_NAME)
	mkdir -p vendors && $(PIP) install -t vendors -Ur requirements.txt
ifeq ($(ENVIRONMENT),dev)
	$(VENV_NAME)/bin/pip install -Ur requirements-dev.txt
    # create settings_dev.py if it doesn't exist
	test -s instance/settings_dev.py || echo "from instance.settings import *" > instance/settings_dev.py
endif

run:
ifeq ($(ENVIRONMENT),dev)
	PYTHONPATH=vendors SETTINGS=settings_$(ENVIRONMENT).py APPLICATION_NAME=restaurants $(VENV_NAME)/bin/python run.py
endif
ifeq ($(ENVIRONMENT),prod)
	PYTHONPATH=vendors SETTINGS=settings_$(ENVIRONMENT).py APPLICATION_NAME=restaurants $(VENV_NAME)/bin/gunicorn app:app
endif

doc:
	rm swagger.json && \
	PYTHONPATH=vendors SETTINGS=settings_$(ENVIRONMENT).py APPLICATION_NAME=restaurants $(VENV_NAME)/bin/python doc.py
