import logging

def error_if(val):
    if val:
        logging.info("Failed. Error Code " + str(val))
    else:
        logging.info("Success")

    return val


def fail(msg, src, dest):
    logging.info("[FAILED] " + msg + " src: {0} dest: {1}".format(src, dest))
    return False


def success(msg, src, dest):
    logging.info("Success  " + msg + " src: {0} dest : {1}".format(src, dest))
    return True


def notify_config(msg):
    logging.info("[Configuring " + msg + ']')


def notify(status, msg):
    logging.info("[" + status + "] " + msg)
