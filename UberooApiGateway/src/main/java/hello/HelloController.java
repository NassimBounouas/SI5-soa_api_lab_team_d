package hello;


import kafka.producer.Sender;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;

@RestController
public class HelloController {

    @Autowired
    private Sender sender;

    @RequestMapping("/")
    public String index() {
        sender.send("Test message from java");
        return "Greetings from Spring Boot!";
    }

}
