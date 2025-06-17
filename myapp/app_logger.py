import logging


def get_app_logger():
    return logging.getLogger('myapp')

def try_app_logger():
    logger = get_app_logger()

    print('\n' + '-'*80)
    print(str(logger))
    print("LEVEL:", logger.getEffectiveLevel())
    print("PROPAGATE:", logger.propagate)
    print("HANDLERS:")
    for h in logger.handlers:
        print("  ->", h, h.level)

    logger.debug('DEBUG message')
    logger.info('INFO message')
    logger.warning('WARNING message')
    logger.error('ERROR message')
    logger.critical('CRITICAL message')

    print('-' * 80)
