package teamd.uberoo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import teamd.uberoo.kafka.KafkaMessage;
import teamd.uberoo.kafka.MessageProducer;

@RestController
public class RestaurantController {
    @Autowired
    private MessageProducer producer;

    @RequestMapping(value = "/list_categories", method = RequestMethod.POST)
    public String listCategories() {
        producer.sendKafkaMessage(new KafkaMessage("CATEGORY_LIST_REQUEST", "{ \"id_request\": 1}"));
        return "ok";
    }

    @RequestMapping(value = "/categories", method = RequestMethod.GET)
    public String categoriesresponse(@RequestParam("id") long id) {
        return "GET with parameter : " + id;
    }

    @RequestMapping(value = "/list_meal_by_category", method = RequestMethod.POST)
    public String listMealByCategory() {
        producer.sendKafkaMessage(new KafkaMessage("MEAL_LIST_REQUEST", "{ \"id_request\": 1, \"id_category\": 1}"));
        return "ok";
    }

    @RequestMapping(value = "/meal_list", method = RequestMethod.GET)
    public String listMealResponse(@RequestParam("id") long id) {
        return "GET with parameter : " + id;
    }
}
