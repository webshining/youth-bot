-include .env
LOCALES_PATH := ./data/locales
I18N_DOMAIN := $(or $(I18N_DOMAIN),bot)

run:
	python main.py
logs:
	docker compose logs -f app
rebuild:
	docker compose up -d --no-deps --force-recreate --build
pybabel_extract:
	pybabel extract --input-dirs=. -o $(LOCALES_PATH)/$(I18N_DOMAIN).pot
pybabel_init: 
	pybabel init -i $(LOCALES_PATH)/$(I18N_DOMAIN).pot -d $(LOCALES_PATH) -D $(I18N_DOMAIN) -l en && \
	pybabel init -i $(LOCALES_PATH)/$(I18N_DOMAIN).pot -d $(LOCALES_PATH) -D $(I18N_DOMAIN) -l ru && \
	pybabel init -i $(LOCALES_PATH)/$(I18N_DOMAIN).pot -d $(LOCALES_PATH) -D $(I18N_DOMAIN) -l uk
pybabel_update: 
	pybabel update -i $(LOCALES_PATH)/$(I18N_DOMAIN).pot -d ./data/locales -D $(I18N_DOMAIN)
pybabel_compile:
	pybabel compile -d $(LOCALES_PATH) -D $(I18N_DOMAIN)