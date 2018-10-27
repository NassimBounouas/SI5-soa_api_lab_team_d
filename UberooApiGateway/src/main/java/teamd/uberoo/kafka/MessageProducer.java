package teamd.uberoo.kafka;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.kafka.core.KafkaTemplate;

public class MessageProducer {
    @Autowired
    private KafkaTemplate<String, KafkaMessage> kafkaMessageKafkaTemplate;

    @Value(value = "${message.topic.name}")
    private String kafkaMessageTopicName;

    public void sendKafkaMessage(KafkaMessage message) {
        kafkaMessageKafkaTemplate.send(kafkaMessageTopicName, message);
    }
}
