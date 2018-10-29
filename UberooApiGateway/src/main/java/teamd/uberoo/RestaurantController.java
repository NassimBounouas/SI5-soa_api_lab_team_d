package teamd.uberoo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import teamd.uberoo.kafka.MessageProducer;

@RestController
public class RestaurantController {
    @Autowired
    private MessageProducer producer;

    @RequestMapping("/list_categories")
    public String listCategories() {
        return "ok";
    }
}
