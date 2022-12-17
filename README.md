<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

**Table of Contents**

- [DeepLog api](#deeplog-api)
  - [Base philosophy from The Zen of Python](#base-philosophy-from-the-zen-of-python)
  - [Installation](#installation)
  - [Running the app with docker](#running-the-app-with-docker)
  - [Migration](#migration)
  - [Command](#command)
  - [Issue](#issue)
  - [Resolve](#resolve)
  - [References](#references)
- [DeepLogApi](#deeplogapi)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# DeepLog api

- python3
- django3.2.8
- postgresql

## Base philosophy from The Zen of Python

<hr>

- Beautiful is better than ugly.
- Explicit is better than implicit.
- Simple is better than complex.
- Complex is better than complicated.
- Flat is better than nested.
- Sparse is better than dense.
- Readability counts.
- Special cases aren't special enough to break the rules.
- Although practicality beats purity.
- Errors should never pass silently.
- Unless explicitly silenced.
- In the face of ambiguity, refuse the temptation to guess.
- There should be one-- and preferably only one --obvious way to do it.
- Although that way may not be obvious at first unless you're Dutch.
- Now is better than never.
- Although never is often better than _right_ now.
- If the implementation is hard to explain, it's a bad idea.
- If the implementation is easy to explain, it may be a good idea.
- Namespaces are one honking great idea -- let's do more of those!

## Installation

<hr>

```sh
$ pip3 install
```

## Running the app with docker

<hr>

development

```sH
$ docker-compose up --build
```

production

```
$ sudo ./init-letsencrypt.sh
$ docker-compose -f ./docker-compose.prod.yml up --build -d
```

## Migration

<hr>

```sh
$ docker exec -t -i <API CONTAINER ID> bash
$ python3 manage.py migrate
```

## Command

<hr>

- Making a model

```sh
$ python3 manage.py startapp <MODEL NAME>
```

## Issue

<hr>

-

## Resolve

<hr>

-
-

## References

- succeed ssl certification
  https://pentacent.medium.com/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71

- succeed jwt
  https://qiita.com/Syoitu/items/bc32b5e1c2fa891c2f96

- ManyToManyRelation
  https://djangobrothers.com/blogs/many_to_many_objects/

- Collaborative filtering
  https://qiita.com/ynakayama/items/59beb40b7c3829cc0bf2

- Math markdown
  https://qiita.com/PlanetMeron/items/63ac58898541cbe81ada

- https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml

# DeepLogApi
# DeepAiApi
