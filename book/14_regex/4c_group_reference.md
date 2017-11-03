## Повторение захваченного результата

При работе с группами можно использовать результат, который попал в группу, дальше в этом же выражении.

Например, в выводе sh ip bgp последний столбец описывает атрибут AS Path (через какие автономные системы прошел маршрут):
```python
In [1]: bgp = '''
   ...: R9# sh ip bgp | be Network
   ...:    Network          Next Hop       Metric LocPrf Weight Path
   ...: *  192.168.66.0/24  192.168.79.7                       0 500 500 500 i
   ...: *>                  192.168.89.8                       0 800 700 i
   ...: *  192.168.67.0/24  192.168.79.7         0             0 700 700 700 i
   ...: *>                  192.168.89.8                       0 800 700 i
   ...: *  192.168.88.0/24  192.168.79.7                       0 700 700 700 i
   ...: *>                  192.168.89.8         0             0 800 800 i
   ...: '''
```

Допустим, надо получить те префиксы, у которых в пути несколько раз повторяется один и тот же номер AS.

Это можно сделать с помощью ссылки на результат, который был захвачен группой.
Например, такое выражение отображает все строки, в которых один и тот же номер повторяется хотя бы два раза:
```python
In [2]: for line in bgp.split('\n'):
   ...:     match = re.search(r'(\d+) \1', line)
   ...:     if match:
   ...:         print(line)
   ...:
*  192.168.66.0/24  192.168.79.7                       0 500 500 500 i
*  192.168.67.0/24  192.168.79.7         0             0 700 700 700 i
*  192.168.88.0/24  192.168.79.7                       0 700 700 700 i
*>                  192.168.89.8         0             0 800 800 i
```

В этом выражении обозначение ```\1``` подставляет результат, который попал в группу. Номер один указывает на конкретную группу.
В данном случае это группа 1, она же единственная.

Кроме того, в этом выражении перед строкой регулярного выражения стоит буква r.
Это так называемая raw строка.

Тут удобней использовать ее, так как иначе надо будет экранировать обратный слеш, чтобы ссылка на группу сработала корректно:
```python
match = re.search('(\d+) \\1', line)
```

> При использовании регулярных выражений лучше всегда использовать raw строки.

Аналогичным образом можно описать строки, в которых один и тот же номер встречается три раза:
```python
In [3]: for line in bgp.split('\n'):
   ...:     match = re.search(r'(\d+) \1 \1', line)
   ...:     if match:
   ...:         print(line)
   ...:
*  192.168.66.0/24  192.168.79.7                       0 500 500 500 i
*  192.168.67.0/24  192.168.79.7         0             0 700 700 700 i
*  192.168.88.0/24  192.168.79.7                       0 700 700 700 i

```

Аналогичным образом можно ссылаться на результат, который попал в именованную группу:
```python
In [129]: for line in bgp.split('\n'):
     ...:     match = re.search('(?P<as>\d+) (?P=as)', line)
     ...:     if match:
     ...:         print(line)
     ...:
*  192.168.66.0/24   192.168.79.7                       0 500 500 500 i
*  192.168.67.0/24   192.168.79.7         0             0 700 700 700 i
*  192.168.88.0/24   192.168.79.7                       0 700 700 700 i
*>                   192.168.89.8         0             0 800 800 i

```
