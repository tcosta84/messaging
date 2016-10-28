# Messaging Service

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

Messaging is a microservice that let your application send short messages (SMS).

You can:
  - Set an expiration date so that your users do not receive outdated and irrelevant content;

You can't:
  - Send messages larger than 160 chars;

### Installation

Messaging requires [Python](https://python.org/) v3.5+ to run.

Install the dependencies, create database and start the server.

```sh
$ make install
```

#### Docker

You can also install via Docker:

```sh
$ make docker-install
```

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

Method: PUT

Headers:
    - Content-type: application/json

Request example:

    {
        "sender": "21981527318",
        "receiver": "980072800",
        "body": "Hello!",
        "expiration_date": "2016-10-25T15:00"
    }

Successful Respomse Status Code: 201 CREATED

Response example:

    {
        "detail": "Message sent."
    }

Possible errors:

400 BAD REQUEST

- Content-type is not valid (expected "application/json");
- Invalid JSON (ex: empty);
- Validation erros;
- Message size is greater than 160 chars;
- Message is already expired (when "expiration_date" is provided)

404 NOT FOUND

- Mobile User not found (Operator API error)

500 INTERNAL SERVER ERROR

When an unexpected error happens (Service or Operator API error)

**Example Response:**

    {
        "error": "Message not sent. Operator API response: "{description}""
    }

Operator API Errors:

200 OK

- Request is correct, no validation errors but failed due to the Operator API

**Example Response:**

    {
        "error": "Message not sent. Operator API response: "{description}""
    }

**Possible Descriptions:**

- 'Mobile User not found'
- 'Validation exception'
- 'Internal Server Error
