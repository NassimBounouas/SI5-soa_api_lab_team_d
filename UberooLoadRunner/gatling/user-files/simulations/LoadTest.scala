import io.gatling.core.Predef._
import io.gatling.core.structure.ScenarioBuilder
import io.gatling.http.Predef._
import io.gatling.http.protocol.HttpProtocolBuilder
import scala.concurrent.duration._

import java.util.UUID

class LoadTest extends Simulation {

  val meals_url = "http://localhost:8080"

  val consultMeals = scenario("List available categories")
    .exec(http("Get all categories")
    .post(meals_url + "/list_categories")
    .check(status.is(202), jsonPath("$.callbackUrl").saveAs("callbackurl")))
    .exec(session => {
      val maybeId = session.get("callbackurl").asOption[String]
      println(maybeId.getOrElse("COULD NOT FIND CALLBACK"))
      http("Get all categories RESPONSE")
            .get(maybeId.getOrElse("COULD NOT FIND CALLBACK"))
            .check(status.is(200))
      session
    })

  setUp(consultMeals.inject(rampUsersPerSec(2) to 25 during (10 seconds)))
}