package hello;

public class KafkaMessage {
    private String action;
    private String name;

    public KafkaMessage() {

    }

    public KafkaMessage(String action, String name) {
        this.action = action;
        this.name = name;
    }

    public String getAction() {
        return action;
    }

    public void setAction(String action) {
        this.action = action;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return "KafkaMessage{" +
                "action='" + action + '\'' +
                ", name='" + name + '\'' +
                '}';
    }
}
