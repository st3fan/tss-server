NAME = tss-server
TAG = tws/$(NAME):master

default: build

build:
	docker build -q -t $(TAG) .

