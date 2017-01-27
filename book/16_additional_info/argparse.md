## Модуль argparse

argparse - это модуль для обработки аргументов командной строки.

Примеры того, что позволяет делать модуль:
* создавать аргументы и опции, с которыми может вызываться скрипт
* указывать типы аргументов, значения по умолчанию
* указывать какие действия соответствуют аргументам
* выполнять вызов функции, при указании аргумента
* отображать сообщения с подсказами по использованию скрипта

argparse не единственный модуль для обработки аргументов командной строки.
И даже, не единственный такой модуль в стандартной библиотеке.

Мы будем рассматривать только argparse.
Но, если вы столкнетесь с необходимостью использовать подобные модули,
обязательно посмотрите и на те модули, которые не входят в стандартную библиотеку Python.
Например, на [click](http://click.pocoo.org/5/).

> [Очень хорошая статья](https://realpython.com/blog/python/comparing-python-command-line-parsing-libraries-argparse-docopt-click/), которая сравнивает разные модули обработки аргументов командной строки (рассматриваются argparse, click и docopt).


Посмотрим на пример скрипта, на основе примера в разделе subprocess (файл ping_function.py):
```python
import subprocess
from tempfile import TemporaryFile
import argparse

def ping_ip(ip_address, count=3):
    """
    Ping IP address and return tuple:
    On success: (return code = 0, command output)
    On failure: (return code, error output (stderr))
    """
    with TemporaryFile() as temp:
        try:
            output = subprocess.check_output(['ping', '-c', str(count), '-n', ip_address],
                                             stderr=temp)
            return 0, output
        except subprocess.CalledProcessError as e:
            temp.seek(0)
            return e.returncode, temp.read()


parser = argparse.ArgumentParser(description='Ping script')

parser.add_argument('-a', action="store", dest="ip")
parser.add_argument('-c', action="store", dest="count", default=2, type=int)

args = parser.parse_args()
print args

rc, message = ping_ip( args.ip, args.count )
print message
```

Разберемся с argparse:
* Сначала необходимо создать парсер:
 * ```parser = argparse.ArgumentParser(description='Ping script')```
* затем, мы начинаем добавлять аргументы:
 * ```parser.add_argument('-a', action="store", dest="ip")```
  * аргумент, который мы передадим после опции ```-a```, сохранится в переменную ```ip```
 * ```parser.add_argument('-c', action="store", dest="count", default=2, type=int)```
  * аргумент, который передается после опции ```-c```, будет сохранен в переменную ```count```, но, прежде, будет конвертирован в число. Если аргумент не было указан, по умолчанию, будет значение 2

Строку ```args = parser.parse_args()``` мы указываем, после того как определили все аргументы.

После её выполнения, в переменной ```args``` содержатся все аргументы, которые мы передали скрипту.
И к ним можно обращаться, использую синтаксис ```args.ip```.


Попробуем вызвать скрипт с разными аргументами.

Такой вывод мы получим, если передать оба аргумента:
```
$ python ping_function.py -a 8.8.8.8 -c 5
Namespace(count=5, ip='8.8.8.8')
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=48.673 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=49.902 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=48 time=48.696 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=48 time=50.040 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=48 time=48.831 ms

--- 8.8.8.8 ping statistics ---
5 packets transmitted, 5 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 48.673/49.228/50.040/0.610 ms
```

> Namespace это объект, который возвращает метод parse_args()

Передаем только IP-адрес:
```
$ python ping_function.py -a 8.8.8.8
Namespace(count=2, ip='8.8.8.8')
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=48.563 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=49.616 ms

--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 48.563/49.090/49.616/0.526 ms
```

Теперь попробуем вызывать скрипт без аргументов:
```
$ python ping_function.py
Namespace(count=2, ip=None)
Traceback (most recent call last):
  File "ping_function.py", line 31, in <module>
    rc, message = ping_ip( args.ip, args.count )
  File "ping_function.py", line 16, in ping_ip
    stderr=temp)
  File "/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 566, in check_output
    process = Popen(stdout=PIPE, *popenargs, **kwargs)
  File "/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 710, in __init__
    errread, errwrite)
  File "/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 1335, in _execute_child
    raise child_exception
TypeError: execv() arg 2 must contain only strings

```

Мы получили ошибку.
Ошибка, возможно, не совсем понятная, так как, если бы не было argparse, и мы вызвали функцию, не указав IP-адрес, мы бы получили ошибку, что не все аргументы указаны.
Но, из-за argparse, фактически аргумент передается, только он равен ```None```.
Это видно в строке ```Namespace(count=2, ip=None)```.

В таком скрипте, очевидно, IP-адрес необходимо указывать всегда.
В argparse мы можем указать, что аргумент является обязательным.

Добавьте, в строке опции ```-a```, в конце ```required=True```:
```python
parser.add_argument('-a', action="store", dest="ip", required=True)
```

Теперь, если мы вызовем скрипт без аргументов, мы получим такой вывод:
```
$ python ping_function.py
usage: ping_function.py [-h] -a IP [-c COUNT]
ping_function.py: error: argument -a is required
```

Теперь мы видим понятное сообщение, что надо указать обязательным аргумент.
И подсказку usage.

Также, благодаря argparse, нам доступен help:
```
$ python ping_function.py -h
usage: ping_function.py [-h] -a IP [-c COUNT]

Ping script

optional arguments:
  -h, --help  show this help message and exit
  -a IP
  -c COUNT
```

Обратите внимание, что в сообщении, все опции, которые мы указывали, находятся в секции `optional arguments`.
argparse сам определяет, что мы указали опцию, так как она начинается с ```-``` и в имени только одна буква.


Попробуем задать IP-адрес, как позиционный аргумент.
И добавим сообщения, которые описывают аргументы.


Файл ping_function_ver2.py:
```python
import subprocess
from tempfile import TemporaryFile

import argparse


def ping_ip(ip_address, count=3):
    """
    Ping IP address and return tuple:
    On success: (return code = 0, command output)
    On failure: (return code, error output (stderr))
    """
    with TemporaryFile() as temp:
        try:
            output = subprocess.check_output(['ping', '-c', str(count), '-n', ip_address],
                                             stderr=temp)
            return 0, output
        except subprocess.CalledProcessError as e:
            temp.seek(0)
            return e.returncode, temp.read()


parser = argparse.ArgumentParser(description='Ping script')

parser.add_argument('host', action="store", help="IP or name to ping")
parser.add_argument('-c', action="store", dest="count", default=2, type=int,
                    help="Number of packets")

args = parser.parse_args()
print args

rc, message = ping_ip( args.host, args.count )
print message
```

Изменился способ передачи IP-адреса.
Теперь, вместо указания опции ```-a```, можно просто передать IP-адрес.
Он будет автоматически сохранен в переменной ```host```.
И автоматически считается обязательным.

То есть, нам не нужно указывать ```required=True``` и ```dest="ip"```.


Кроме того, мы указали сообщения, которые будут выводиться, при вызове help.

Теперь вызов скрипта будет выглядеть так:
```
$ python ping_function_ver2.py 8.8.8.8 -c 2
Namespace(host='8.8.8.8', count=2)
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=48 time=49.203 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=48 time=51.764 ms

--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 49.203/50.484/51.764/1.280 ms
```

А сообщение help так:
```
$ python ping_function_ver2.py -h
usage: ping_function_ver2.py [-h] [-c COUNT] host

Ping script

positional arguments:
  host        IP or name to ping

optional arguments:
  -h, --help  show this help message and exit
  -c COUNT    Number of packets
```

### Вложенные парсеры

argparse поддерживает большое количество возможностей и параметров.
До сих пор, мы рассмотрели лишь самые базовые.

Теперь мы рассмотрим один из способов организации более сложной иерархии аргументов.

> Этот пример покажет больше возможностей argparse, но они этим не ограничиваются, поэтому, если вы будете использовать argparse, обязательно посмотрите [документацию модуля](https://docs.python.org/2.7/library/argparse.html) или [статью на PyMOTW](https://pymotw.com/2/argparse/index.html).


argparse позволяет создавать иерархию парсеров.

Файл parse_dhcp_snooping.py:
```python
# -*- coding: utf-8 -*-
import argparse

# Default values:
DFLT_DB_NAME = 'dhcp_snooping.db'
DFLT_DB_SCHEMA = 'dhcp_snooping_schema.sql'


def create(args):
    print "Creating DB %s with DB schema %s" % (args.name, args.schema)


def add(args):
    if args.sw_true:
        print "Adding switch data to database"
    else:
        print "Reading info from file(s) \n%s" % ', '.join( args.filename )
        print "\nAdding data to db %s" % args.db_file


def get(args):
    if args.key and args.value:
        print "Geting data from DB: %s" % args.db_file
        print "Request data for host(s) with %s %s" % (args.key, args.value)
    elif args.key or args.value:
        print "Please give two or zero args\n"
    else:
        print "Showing %s content..." % args.db_file


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='description')


create_parser = subparsers.add_parser('create_db', help='create new db')
create_parser.add_argument('-n', metavar='db-filename', dest='name',
                           default=DFLT_DB_NAME, help='db filename')
create_parser.add_argument('-s', dest='schema', default=DFLT_DB_SCHEMA,
                           help='db schema filename')
create_parser.set_defaults( func=create )


add_parser = subparsers.add_parser('add', help='add data to db')
add_parser.add_argument('filename', nargs='+', help='file(s) to add to db')
add_parser.add_argument('--db', dest='db_file', default=DFLT_DB_NAME, help='db name')
add_parser.add_argument('-s', dest='sw_true', action='store_true',
                        help='add switch data if set, else add normal data')
add_parser.set_defaults( func=add )


get_parser = subparsers.add_parser('get', help='get data from db')
get_parser.add_argument('--db', dest='db_file', default=DFLT_DB_NAME, help='db name')
get_parser.add_argument('-k', dest="key",
                        choices=['mac', 'ip', 'vlan', 'interface', 'switch'],
                        help='host key (parameter) to search')
get_parser.add_argument('-v', dest="value", help='value of key')
get_parser.add_argument('-a', action='store_true', help='show db content')
get_parser.set_defaults( func=get )



if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
```

Теперь создается не только парсер, как в прошлом примере, но и вложенные парсеры.
Вложенные парсеры будут отображаться как команды.
Но, фактически, они будут использоваться как обязательные аргументы.

С помощью вложенных парсеров, создается иерархия аргументов и опций.
Аргументы, которые добавлены во вложенный парсер, будут доступны как аргументы этого парсера.


Например, в этой части, создан вложенный парсер create_db и к нему добавлена опция ```-n```:
```python
create_parser = subparsers.add_parser('create_db', help='create new db')
create_parser.add_argument('-n', dest='name', default=DFLT_DB_NAME,
                           help='db filename')
```

Синтаксис создания вложенных парсеров и добавления к ним аргументов, одинаков:
```python
create_parser = subparsers.add_parser('create_db', help='create new db')
create_parser.add_argument('-n', metavar='db-filename', dest='name',
                           default=DFLT_DB_NAME, help='db filename')
create_parser.add_argument('-s', dest='schema', default=DFLT_DB_SCHEMA,
                           help='db schema filename')
create_parser.set_defaults( func=create )
```

Метод ```add_argument``` добавляет аргумент.
Тут синтаксис точно такой же, как и без использования вложенных парсеров.

В строке ``create_parser.set_defaults( func=create )``` указывается, что, при вызове парсера ```create_parser```, будет вызвана функция create.

Функция create получает как аргумент, все аргументы, которые были переданы.
И, внутри функции, можно обращаться к нужным:
```python
def create(args):
    print "Creating DB %s with DB schema %s" % (args.name, args.schema)
```

Если вызвать help для этого скрипта, вывод будет таким:
```
$ python parse_dhcp_snooping.py -h
usage: parse_dhcp_snooping.py [-h] {create_db,add,get} ...

optional arguments:
  -h, --help           show this help message and exit

subcommands:
  valid subcommands

  {create_db,add,get}  description
    create_db          create new db
    add                add data to db
    get                get data from db
```

Обратите внимание, что каждый вложенный парсер, который создан в скрипте, отображается как команда в подсказке usage:
```
usage: parse_dhcp_snooping.py [-h] {create_db,add,get} ...
```

У каждого вложенного парсера теперь есть свой help:
```
$ python parse_dhcp_snooping.py create_db -h
usage: parse_dhcp_snooping.py create_db [-h] [-n db-filename] [-s SCHEMA]

optional arguments:
  -h, --help      show this help message and exit
  -n db-filename  db filename
  -s SCHEMA       db schema filename
```

Кроме вложенных парсеров, в этом примере также есть несколько новых возможностей argparse.


#### ```metavar```

В парсере create_parser используется новый аргумент - ```metavar```:
```python
create_parser.add_argument('-n', metavar='db-filename', dest='name',
                           default=DFLT_DB_NAME, help='db filename')
create_parser.add_argument('-s', dest='schema', default=DFLT_DB_SCHEMA,
                           help='db schema filename')
```

Аргумент ```metavar``` позволяет указывать имя аргумента для вывода в сообщении usage и help:
```
$ python parse_dhcp_snooping.py create_db -h
usage: parse_dhcp_snooping.py create_db [-h] [-n db-filename] [-s SCHEMA]

optional arguments:
  -h, --help      show this help message and exit
  -n db-filename  db filename
  -s SCHEMA       db schema filename
```

Посмотрите на разницу между опциями ```-n``` и ```-s```:
* после опции ```-n```, и в usage, и в help, указывается имя, которое указано в параметре metavar
* после опции ```-s``` указывается имя переменной, в которую сохраняется значение

#### ```nargs```

В парсере add_parser используется ```nargs```:
```python
add_parser.add_argument('filename', nargs='+', help='file(s) to add to db')
```

```nargs``` позволяет указать, что в этот аргумент должно попасть определенное количество элементов.
В нашем случае, все аргументы, которые были переданы скрипту, после имени аргумента ```filename```,
попадут в список nargs.
Но должен быть передан хотя бы один аргумент.

Сообщение help, в таком случае, выглядит так:
```
$ python parse_dhcp_snooping.py add -h
usage: parse_dhcp_snooping.py add [-h] [--db DB_FILE] [-s]
                                  filename [filename ...]

positional arguments:
  filename      file(s) to add to db

optional arguments:
  -h, --help    show this help message and exit
  --db DB_FILE  db name
  -s            add switch data if set, else add normal data
```

Если мы передадим несколько файлов, они попадут в список.
А, так как функция add, просто выводит имена файлов, вывод получится таким:
```
$ python parse_dhcp_snooping.py add filename test1.txt test2.txt
Reading info from file(s)
filename, test1.txt, test2.txt

Adding data to db dhcp_snooping.db
```

```nargs``` поддерживает такие значения:
* ```N``` - должно быть указанное количество аргументов. Аргументы будут в списке (даже, если указан 1)
* ```?``` - 0 или 1 аргумент
* ```*``` - все аргументы попадут в список 
* ```+``` - все аргумнеты попадут в список, но должен быть передан, хотя бы, один аргумент


#### ```choices```

В парсере get_parser используется ```choices```:
```python
get_parser.add_argument('-k', dest="key",
                        choices=['mac', 'ip', 'vlan', 'interface', 'switch'],
                        help='host key (parameter) to search')
```

Для некоторых аргументов, важно, чтобы значение было выбрано только из орпределенных вариантов.
Для таких случаев, можно указывать ```choices```.

Для этого парсера, help выглядит так:
```
$ python parse_dhcp_snooping.py get -h
usage: parse_dhcp_snooping.py get [-h] [--db DB_FILE]
                                  [-k {mac,ip,vlan,interface,switch}]
                                  [-v VALUE] [-a]

optional arguments:
  -h, --help            show this help message and exit
  --db DB_FILE          db name
  -k {mac,ip,vlan,interface,switch}
                        host key (parameter) to search
  -v VALUE              value of key
  -a                    show db content
```

А, если выбрать неправильный вариант:
```
$ python parse_dhcp_snooping.py get -k test
usage: parse_dhcp_snooping.py get [-h] [--db DB_FILE]
                                  [-k {mac,ip,vlan,interface,switch}]
                                  [-v VALUE] [-a]
parse_dhcp_snooping.py get: error: argument -k: invalid choice: 'test' (choose from 'mac', 'ip', 'vlan', 'interface', 'switch')
```

> В данном примере важно указать варианты на выбор, так как затем, на основании выбранного варианта, генерируется SQL-запрос. И, благодаря ```choices```, нет возможно указать какой-то параметр, кроме разрешенных.


#### Импорт парсера

В файле parse_dhcp_snooping.py, последние две строки будут выполняться только в том случае, если скрипт был вызван как основной.
```python
if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
```

А значит, если импортировать файл, эти строки не будут вызваны.

Попробуем импортировать парсер в другой файл (файл call_pds.py):
```python
from parse_dhcp_snooping import parser

args = parser.parse_args()
args.func(args)
```

А теперь попробуем вызвать сообщение help:
```
$ python call_pds.py -h
usage: call_pds.py [-h] {create_db,add,get} ...

optional arguments:
  -h, --help           show this help message and exit

subcommands:
  valid subcommands

  {create_db,add,get}  description
    create_db          create new db
    add                add data to db
    get                get data from db
```

И вызвать какой-то аргумент:
```
$ python call_pds.py add test.txt test2.txt
Reading info from file(s)
test.txt, test2.txt

Adding data to db dhcp_snooping.db
```

Как видите, всё работает без проблем.

#### Передача аргументов вручную

И, последняя особенность argparse, которую мы рассмотрим - возможность передавать аргументы вручную.

Мы можем передать аргументы как список, при вызове метода ```parse_args()``` (файл call_pds2.py):
```python
from parse_dhcp_snooping import parser, get

args = parser.parse_args('add test.txt test2.txt'.split())
args.func(args)
```

> Необходимо использвоать метод split(), так как метод ```parse_args```, ожидает список аргументов.

Результат будет таким, как если бы мы вызвали скрипт с аргументами:
```
$ python call_pds2.py
Reading info from file(s)
test.txt, test2.txt

Adding data to db dhcp_snooping.db
```
