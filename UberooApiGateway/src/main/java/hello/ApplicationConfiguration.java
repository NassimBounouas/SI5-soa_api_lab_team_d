package hello;

import kafka.MessageListener;
import kafka.MessageProducer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;
import org.springframework.context.annotation.PropertySources;
import org.springframework.core.env.Environment;
import org.springframework.transaction.annotation.EnableTransactionManagement;
import org.springframework.web.client.RestTemplate;

/**
 * Class name   ApplicationConfiguration
 * Date         29/09/2018
 *
 * @author PierreRainero
 */
@Configuration
@PropertySources({
        //@PropertySource("classpath:db.properties"),
        @PropertySource("classpath:application.properties")
})
@EnableTransactionManagement
public class ApplicationConfiguration {
    @Autowired
    private Environment env;

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
    @Bean
    public MessageProducer messageProducer() {
        return new MessageProducer();
    }

    @Bean
    public MessageListener messageListener() {
        return new MessageListener();
    }

}
