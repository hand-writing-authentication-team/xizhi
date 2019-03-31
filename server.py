from multiprocessing import Process
import os
import redis
import pika
import time
import logging

def dealRequest(ch, method, properties, body):
    logging.info(" [x] Received %r" % (body,))
    time.sleep( body.count('.') )
    logging.info(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

class server(object):
    def __init__(self):
        Logger = logging.getLogger(__name__)

        mqHost = os.environ.get('MQ_HOST')
        mqPort = os.environ.get('MQ_PORT')
        mqUser = os.environ.get('MQ_USER')
        mqPw = os.environ.get('MQ_PASSWORD')
        self.queueName = os.environ.get('QUEUE')

        redisHost = os.environ.get('REDIS_HOST')
        redisPort = os.environ.get('REDIS_PORT')
        redisCh = os.environ.get('REDIS_CH')

        loglevel = os.environ.get('LOG_LEVEL')

        if loglevel == None:
            Logger.setLevel(logging.INFO)
            logging.info("logging level is not set, set it as info level")
        else:
            if loglevel == "CRITICAL":
                Logger.setLevel(logging.CRITICAL)
                logging.critical("logging level is now set to CRITICAL")
            elif loglevel == "ERROR":
                Logger.setLevel(logging.ERROR)
                logging.error("logging level is now set to ERROR")
            elif loglevel == "WARNING":
                Logger.setLevel(logging.WARNING)
                logging.warning("logging level is now set to WARNING")
            elif loglevel == "INFO":
                Logger.setLevel(logging.INFO)
                logging.info("logging level is now set to INFO")
            elif loglevel == "DEBUG":
                Logger.setLevel(logging.DEBUG)
                logging.debug("logging level is now set to DEBUG")
            else:
                Logger.setLevel(logging.INFO)
                logging.info("logging level is set to a invalid value, set it as INFO")

        if mqHost == None or mqPort == None or mqUser == None or mqPw == None or self.queueName == None or redisHost == None or redisPort == None or redisCh == None:
            logging.error("one of the required environment variable is not set")
            exit(1)
        
        retryCnt = 0
        self.r = None
        while (retryCnt < 5):
            try:
                self.r = redis.Redis(host=redisHost, port=redisPort)
                self.r.set("xizhi", "ok")
                break
            except redis.ConnectionError:
                logging.error(" [x] redis connection failed, retrying...")
                time.sleep(5)
        if (retryCnt >= 5):
            logging.error(" [x] has retried for 5 times for redis connection, abort")
            exit(1)

        retryCnt = 0

        self.mq = None
        while (retryCnt < 5):
            try:
                credentials = pika.PlainCredentials(mqUser, mqPw)
                connectParam = pika.ConnectionParameters(host = mqHost, port = mqPort, virtual_host = '/', credentials = credentials)
                self.mq = pika.BlockingConnection(connectParam)
                break
            except pika.exceptions.AMQPConnectionError:
                logging.error(" [x] rabbitmq connection failed, retrying...")
                time.sleep(5)
        if (retryCnt >= 5):
            logging.error(" [x] has retried for 5 times for rabbitmq connection, abort")
            exit(1)
        
        ch = self.mq.channel()
        ch.queue_declare(queue=self.queueName, durable=False)
        ch.close()

    def forever_runner(self):
        channel = self.mq.channel()
        channel.basic_consume(queue=self.queueName, on_message_callback=dealRequest)
        startTime = time.time()
        while (True):
            logging.debug(" [x] keeping the server alive for {0}".format(time.time() - startTime))
        
def main():
    xizhi_server = server()
    xizhi_server.forever_runner()

if __name__ == "__main__":
    main()