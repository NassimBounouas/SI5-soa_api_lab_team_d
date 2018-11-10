# Uberoo Acceptance Scenarios

### Author
__Nikita ROUSSEAU__
### Updated
__00:00 07/11/2018__

## Requirements

- Python 3.6.x
- Dependencies :
  * behave

### Install Dependencies

```bash
pip install --trusted-host pypi.python.org -r requirements.txt
```

## Usage

Run the acceptance scenarios associated to Uberoo API.

### Standalone

```bash
$ python app.py
```

## User Stories

### Personas

  - Gail, a student who lives in Sophia and often order (junk) food from food trucks;
  - Erin, a software developer working in a major company;
  - Jordan, restaurant chef;
  - Jamie, a coursier;

### Week 41: Initial Story set

  - As Gail or Erin, I can order my lunch from a restaurant so that the food is delivered to my place;
  + As Gail, I can browse the food catalogue by categories so that I can immediately identify my favorite junk food;
  + As Erin, I want to know before ordering the estimated time of delivery of the meal so that I can schedule my work around it, and be ready when it arrives.
  + As Erin, I can pay directly by credit card on the platform, so that I only have to retrieve my food when delivered;
  + As Jordan, I want to access to the order list, so that I can prepare the meal efficiently.
  + As Jamie, I want to know the orders that will have to be delivered around me, so that I can choose one and go to the restaurant to begin the course.
  + As Jamie, I want to notify that the order has been delivered, so that my account can be credited and the restaurant can be informed.

### Week 43: First evolution

New personna: Terry, restaurant owner.

  - As Jordan, I want the customers to be able to review the meals so that I can improve them according to their feedback;
  - As a customer (Gail, Erin), I want to track the geolocation of the coursier in real time, so that I can anticipate when I will eat.
  - As Terry, I want to get some statistics (speed, cost) about global delivery time and delivery per coursier.
  
### Week 44: Second evolution

  - As Terry, I can emit a promotional code so that I can attract more customer to my restaurant. 
  - As Jamie, I want to inform quickly that I can't terminate the course (accident, sick), so that the order can be replaced.

### Week 45: Last evolution

  - As Terry, I can emit a promotional code based on my menu contents (e.g., 10% discout for an entry-main course-dessert order), so that I can sell more expensive orders.
  - As Gail or Erin, I can follow the position of Jamie in real time, so that the food ETA can be updated automatically.
