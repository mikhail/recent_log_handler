import logging

import coloredlogs

import log_handler

log = logging.getLogger('')
stream = logging.StreamHandler()
stream.setLevel(logging.INFO)
log.addHandler(stream)

coloredlogs.install(level='INFO')


@log_handler.on_error(capacity=10)
def main():
    log.debug('Main function starting')
    log.debug('About to run a for loop')
    log.debug('Loop range() parameters are 3, -1, -1')
    log.debug('Starting...')
    for i in range(3, -1, -1):
        log.debug('Ok, inside the loop now. i=%s', i)
        log.info('Rare info log here')
        log.debug("Done with the loop. Let's do some math")
        5 / i

if __name__ == "__main__":
    main()
