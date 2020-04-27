# log_handler

Helper log handler to catch debug logs while preventing them from overwhelming you.

## Usage
Use it as a decorator with parameters!

Full example is in the example.py file

```python
@log_handler.on_error(capacity=10)
def main():
    log.debug('Frequent and verbose debug logs')

    for i in range(100, -1, -1):
        log.debug('Ok, inside the loop now. i=%s', i)
        log.info('Rare info log here')
        log.debug('Obnoxious debug log here')
        5 / i  # something that causes a bug sometimes but not always
```

![image](https://user-images.githubusercontent.com/3210918/80431456-5a59ba80-88a6-11ea-8299-b0d36706a287.png)
