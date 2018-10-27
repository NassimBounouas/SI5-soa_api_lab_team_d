package kafka;

import hello.KafkaMessage;
import org.springframework.kafka.annotation.KafkaListener;

import java.util.concurrent.CountDownLatch;

public class MessageListener {
    public CountDownLatch messageLatch = new CountDownLatch(1);


    @KafkaListener(topics = "${message.topic.name}", containerFactory = "kafkaMessageKafkaListenerContainerFactory")
    public void greetingListener(KafkaMessage message) {
        if (message.getAction() != null && message.getName() != null) {
            System.out.println("Received kafka message: " + message);
        }
        this.messageLatch.countDown();
    }

}
