### INSERT
Добавим записи в таблицу. Есть несколько вариантов добавления записей, в зависимости от того, все ли поля будут заполнены и будут ли они идти по порядку определения полей или нет.

Если мы будем указывать значения для всех полей, то добавить запись можно таким образом (порядок полей должен соблюдаться):
```
sqlite> INSERT into switch values ('0000.AAAA.CCCC', 'sw1', 'Cisco 3750', 'London, Green Str');
```

Если нужно указать не все поля, или указать их в произвольном порядке, используется такая запись:
```
sqlite> INSERT into switch (mac, model, location, hostname)
   ...> values ('0000.BBBB.CCCC', 'Cisco 3850', 'London, Green Str', 'sw5');
```