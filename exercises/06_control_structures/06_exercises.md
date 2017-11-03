# Задания

{% include "../exercises_intro.md" %}

### Задание 6.1

1. Запросить у пользователя ввод IP-адреса в формате 10.0.1.1.
2. Определить какому классу принадлежит IP-адрес.
3. В зависимости от класса адреса, вывести на стандартный поток вывода:
   * 'unicast' - если IP-адрес принадлежит классу A, B или C
   * 'multicast' - если IP-адрес принадлежит классу D
   * 'local broadcast' - если IP-адрес равен 255.255.255.255
   * 'unassigned' - если IP-адрес равен 0.0.0.0
   * 'unused' - во всех остальных случаях

Подсказка по классам (диапазон значений первого байта в десятичном формате):
* A: 1-127
* B: 128-191
* C: 192-223
* D: 224-239

Ограничение: Все задания надо выполнять используя только пройденные темы.


### Задание 6.1a

Сделать копию скрипта задания 6.1.

Дополнить скрипт:
- Добавить проверку введенного IP-адреса.
- Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой,
   - каждое число в диапазоне от 0 до 255.

Если адрес задан неправильно, выводить сообщение:
* 'Incorrect IPv4 address'

Ограничение: Все задания надо выполнять используя только пройденные темы.


### Задание 6.1b
Сделать копию скрипта задания 6.1a.

Дополнить скрипт:
* Если адрес был введен неправильно, запросить адрес снова.

Ограничение: Все задания надо выполнять используя только пройденные темы.


### Задание 6.2

Список mac содержит MAC-адреса в формате XXXX:XXXX:XXXX.
Однако, в оборудовании cisco MAC-адреса используются в формате XXXX.XXXX.XXXX.

Создать скрипт, который преобразует MAC-адреса в формат cisco
и добавляет их в новый список mac_cisco

Ограничение: Все задания надо выполнять используя только пройденные темы.

```python
mac = ['aabb:cc80:7000', 'aabb:dd80:7340', 'aabb:ee80:7000', 'aabb:ff80:7000']

mac_cisco = []
```

### Задание 6.3

В скрипте сделан генератор конфигурации для access-портов.

Сделать аналогичный генератор конфигурации для портов trunk.

В транках ситуация усложняется тем, что VLANов может быть много, и надо понимать,  что с ними делать. 

Поэтому в соответствии каждому порту стоит список 
и первый (нулевой) элемент списка указывает как воспринимать номера VLANов, которые идут дальше:
* add - значит VLANы надо будет добавить (команда switchport trunk allowed vlan add 10,20)
* del - значит VLANы надо удалить из списка разрешенных (команда switchport trunk allowed vlan remove 17)
* only - значит, что на интерфейсе должны остаться разрешенными только указанные VLANы (команда switchport trunk allowed vlan 11,30)

Задача для портов 0/1, 0/2, 0/4:
* сгенерировать конфигурацию на основе шаблона trunk_template
* с учетом ключевых слов add, del, only

Ограничение: Все задания надо выполнять используя только пройденные темы.

```python
access_template = ['switchport mode access',
                   'switchport access vlan',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk allowed vlan']

fast_int = {'access':{'0/12':'10','0/14':'11','0/16':'17','0/17':'150'}, 
            'trunk':{'0/1':['add','10','20'],
                     '0/2':['only','11','30'],
                     '0/4':['del','17']} }

for intf, vlan in fast_int['access'].items():
    print('interface FastEthernet' + intf)
    for command in access_template:
        if command.endswith('access vlan'):
            print(' {} {}'.format(command, vlan))
        else:
            print(' {}'.format(command))

```
