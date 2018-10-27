package teamd.uberoo.kafka.customserializer;

import com.fasterxml.jackson.databind.ObjectMapper;
import teamd.uberoo.kafka.KafkaMessage;
import org.apache.kafka.common.serialization.Deserializer;

import java.nio.charset.StandardCharsets;
import java.util.Map;

public class KafkaMessageDeserializer implements Deserializer<KafkaMessage> {
    @Override
    public void configure(Map<String, ?> map, boolean b) {

    }

    @Override
    public KafkaMessage deserialize(String s, byte[] bytes) {
        ObjectMapper mapper = new ObjectMapper();
        KafkaMessage kafkaMessage;
        try {
            kafkaMessage = mapper.readValue(bytes, KafkaMessage.class);
        } catch (Exception e) {
            //e.printStackTrace();
            System.out.println("Error while deserializing kafkamessage : " + new String(bytes, StandardCharsets.UTF_8) + " on topic : " + s);
            kafkaMessage = new KafkaMessage();
        }
        return kafkaMessage;
    }

    @Override
    public void close() {

    }
}
