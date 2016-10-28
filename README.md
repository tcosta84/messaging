# Messaging Service

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

Messaging is a microservice that let your application send short messages (SMS).

You can:
  - Set an expiration date so that your users do not receive outdated and irrelevant content;

You can't:
  - Send messages larger than 160 chars;

### Installation

Messaging requires [Python](https://python.org/) v3.5+ to run.

```sh
$ make install
```

The above command will install the dependencies and create database.
then you can start the server:

```sh
$ make run
```

#### Docker

To make it even simpler, you can also install via Docker:

```sh
$ make docker-install
```

The service is up and running at http://127.0.0.1:5000 ! :)

### Development

Run all test suite and show coverage report:

```sh
$ make test
```

### Usage

To start sending messages you can make a simple call using cURL, like the sample below:

  ```shell
  curl -X PUT -H "Content-type: application/json" -d '{"from": "21981527318", "to": "21980072800", "body": "Hello!"}' -i http://localhost:5000/api/v1/send_sms
  ```

#### API Details

**Method:** PUT

**Headers:**
   - Content-type: application/json

**Request example:**

    {
        "sender": "21981527318",
        "receiver": "980072800",
        "body": "Hello!",
        "expiration_date": "2016-10-25T15:00"
    }

All properties are required except "expiration_date".

**Successful Respomse Status Code:** 201 CREATED

**Successful Response example:**

    {
        "detail": "Message sent."
    }

**Considerations:**
- Any error code different that 201 CREATED means that the **message was no sent.** You can trust that to create your client application. :)
- When the Operator API responds with an error, you will get a 200 OK status from our service. However, it does not mean the message was sent. API expected errors:
	- 'Mobile User not found'
	- 'Validation exception'
	- 'Internal Server Error

**Error Example Response:**

    {
        "error": "Message not sent. Operator API response: "{description}""
    }

**Possible errors:**

400 BAD REQUEST

- Content-type is not valid (expected "application/json");
- Invalid JSON (ex: empty);
- Validation errors;
	- Message size is greater than 160 chars;
	- Message is already expired (when "expiration_date" is provided)

500 INTERNAL SERVER ERROR

When an unexpected error happens.
