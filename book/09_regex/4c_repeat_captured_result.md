## Повторение захваченного результата

```python
In [123]: bgp = '''
     ...: R9# sh ip bgp | be Network
     ...:    Network          Next Hop            Metric LocPrf Weight Path
     ...: *  172.16.66.0/24   172.31.79.7                            0 500 500 500 i
     ...: *>                  172.31.89.8                            0 800 700 i
     ...: *  172.16.67.0/24   172.31.79.7              0             0 700 700 700 i
     ...: *>                  172.31.89.8                            0 800 700 i
     ...: *  172.16.88.0/24   172.31.79.7                            0 700 700 700 i
     ...: *>                  172.31.89.8              0             0 800 800 i
     ...: '''

In [126]: for line in bgp.split('\n'):
     ...:     match = re.search(r'(\d+) \1', line)
     ...:     if match:
     ...:         print(line)
     ...:
*  172.16.66.0/24   172.31.79.7                            0 500 500 500 i
*  172.16.67.0/24   172.31.79.7              0             0 700 700 700 i
*  172.16.88.0/24   172.31.79.7                            0 700 700 700 i
*>                  172.31.89.8              0             0 800 800 i

In [127]: for line in bgp.split('\n'):
     ...:     match = re.search(r'(\d+) \1 \1', line)
     ...:     if match:
     ...:         print(line)
     ...:
*  172.16.66.0/24   172.31.79.7                            0 500 500 500 i
*  172.16.67.0/24   172.31.79.7              0             0 700 700 700 i
*  172.16.88.0/24   172.31.79.7                            0 700 700 700 i

```