## Функция range

Функция range возвращает неизменяемую последовательность чисел в виде объекта range.

Синтаксис функции:
```python
range(stop)
range(start, stop[, step])
```

Параметры функции:
* **start** - с какого числа начинается последовательность. По умолчанию - 0
* **stop** - до какого числа продолжается последовательность чисел. Указанное число не включается в диапазон
* **step** - с каким шагом растут числа. По умолчанию 1

Функция range хранит только информацию о значениях start, stop и step.
И вычисляет значения, по мере необходимости.
Это значит, что независимо от размера диапазона, который описывает функция range, она всегда будет занимать фиксированный объем памяти.

Самый простой вариант range передать только значение stop:
```python
In [1]: range(5)
Out[1]: range(0, 5)

In [2]: list(range(5))
Out[2]: [0, 1, 2, 3, 4]
```

Если передаются два аргумента, то первый используется как start, а второй - stop:
```python
In [3]: list(range(1, 5))
Out[3]: [1, 2, 3, 4]
```

И, чтобы указать шаг последовательности, надо передать три аргумента:
```python
In [4]: list(range(0, 10, 2))
Out[4]: [0, 2, 4, 6, 8]

In [5]: list(range(0, 10, 3))
Out[5]: [0, 3, 6, 9]
```

С помощью range можно генерировать и убывающие последовательности чисел:
```python
In [6]: list(range(10, 0, -1))
Out[6]: [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

In [7]: list(range(5, -1, -1))
Out[7]: [5, 4, 3, 2, 1, 0]
```

Для получения убывающей последовательности, надо использовать отрицательный шаг и соответственно указать start - большим числом, а stop - меньшим.

В убывающей последовательности, шаг тоже может быть разным:
```python
In [8]: list(range(10, 0, -2))
Out[8]: [10, 8, 6, 4, 2]
```

Функция поддерживает отрицательные значения start и stop:
```python
In [9]: list(range(-10, 0, 1))
Out[9]: [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1]

In [10]: list(range(0, -10, -1))
Out[10]: [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
```

Объект range поддерживает все [операции](https://docs.python.org/3.6/library/stdtypes.html#sequence-types-list-tuple-range), которые поддерживают последовательности в Python, кроме сложения и умножения.

Проверка входит ли число в диапазон, которые описывает range:
```python
In [11]: nums = range(5)

In [12]: nums
Out[12]: range(0, 5)

In [13]: 3 in nums
Out[13]: True

In [14]: 7 in nums
Out[14]: False
```

> Начиная с версии Python 3.2 эта проверка выполняется за постоянное время (O(1)).

Можно получить конкретный элемент диапазона:
```python
In [15]: nums = range(5)

In [16]: nums[0]
Out[16]: 0

In [17]: nums[-1]
Out[17]: 4
```

Range поддерживает срезы:
```python
In [18]: nums = range(5)

In [19]: nums[1:]
Out[19]: range(1, 5)

In [20]: nums[:3]
Out[20]: range(0, 3)
```

Можно получить длину диапазона:
```python
In [21]: nums = range(5)

In [22]: len(nums)
Out[22]: 5
```

А также минимальный и максимальный элемент:
```python
In [23]: nums = range(5)

In [24]: min(nums)
Out[24]: 0

In [25]: max(nums)
Out[25]: 4
```

Кроме того, объект range поддерживает метод index:
```python
In [26]: nums = range(1, 7)

In [27]: nums.index(3)
Out[27]: 2
```
