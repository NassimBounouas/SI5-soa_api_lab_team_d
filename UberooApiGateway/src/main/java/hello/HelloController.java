package hello;


import kafka.MessageProducer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

    @Autowired
    private MessageProducer producer;

    @RequestMapping("/")
    public String index() {
        producer.sendKafkaMessage(new KafkaMessage("CALL_ON_ROOT", "Test message from java"));
        return "Greetings from Spring Boot!";
    }

}
