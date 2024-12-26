# MQTT to Postgres

- Script that connects to an `MQTT broker (EMQX)`, listens for incoming messages on a subscribed topic, and stores the data in a `PostgreSQL` database.
- It logs the timestamp of when the message is received from the EMQX broker (data sent by publisher to the same topic subscribed)
- Calculates the `time difference` between the reception of the message from the broker and time it takes for the data to get updated in the Postgres database.
- Prints the time difference to the console.

-- This enables the tracking of latency between message arrival and database update, which is useful for performance monitoring and debugging.
