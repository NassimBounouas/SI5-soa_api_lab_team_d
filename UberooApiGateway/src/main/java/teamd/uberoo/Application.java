package teamd.uberoo;

import teamd.uberoo.kafka.KafkaMessage;
import teamd.uberoo.kafka.MessageListener;
import teamd.uberoo.kafka.MessageProducer;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

import java.util.concurrent.TimeUnit;

@Configuration
@EnableAutoConfiguration
@ComponentScan
public class Application {

    public static void main(String[] args) throws InterruptedException {
        ConfigurableApplicationContext context =  SpringApplication.run(Application.class, args);

        MessageProducer producer = context.getBean(MessageProducer.class);
        MessageListener listener = context.getBean(MessageListener.class);
        producer.sendKafkaMessage(new KafkaMessage("HELLO_MESSAGE", "Coucou"));
        listener.messageLatch.await(3, TimeUnit.SECONDS);
    }
}