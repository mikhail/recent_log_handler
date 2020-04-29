# RecentHandler for logs

Helper log handler to catch debug logs while preventing them from overwhelming you.

For other approaches check out my post "Practical solutions for your debug logs." on [Medium]( https://medium.com/@mikhail.simin/practical-solutions-for-your-debug-logs-db12f083f539).

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

![image](https://user-images.githubusercontent.com/3210918/80432012-de607200-88a7-11ea-9d7c-4398620ca3c7.png)
