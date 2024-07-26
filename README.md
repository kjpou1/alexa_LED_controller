# alexa_LED_controller

This project demonstrates how to control hardware components like LEDs on a Raspberry Pi through an Alexa skill, leveraging an IO Inventory module for scalable and maintainable device management. 

It sets up an Alexa skill server using Bottle and ASK SDK, with support for Gevent to handle server operations. The configuration is managed using dotenv, and the project follows best practices for logging and configuration management.

## Table of Contents
- [alexa\_LED\_controller](#alexa_LED_controller)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
    - [SERVER\_HOST](#server_host)
    - [SERVER\_PORT](#server_port)
    - [INTENT](#intent)
    - [DEBUG](#debug)
    - [SSL\_CERTIFICATE](#ssl_certificate)
    - [SSL\_PRIVATE\_KEY](#ssl_private_key)
  - [Generating a Self-Signed SSL Certificate](#generating-a-self-signed-ssl-certificate)
    - [Script: self-signed-certificate.sh](#script-self-signed-certificatesh)
    - [Instructions](#instructions)
  - [Running the Server](#running-the-server)
    - [Running the Server](#running-the-server-1)
  - [Request Handlers](#request-handlers)
    - [LaunchRequestHandler](#launchrequesthandler)
    - [CustomIntentHandler](#customintenthandler)
    - [SessionEndedRequestHandler](#sessionendedrequesthandler)
    - [FallbackIntentHandler](#fallbackintenthandler)
    - [GoodbyeIntentHandler](#goodbyeintenthandler)
    - [HelpIntentHandler](#helpintenthandler)
    - [StopIntentHandler](#stopintenthandler)
  - [Alexa Skill Interaction Model](#alexa-skill-interaction-model)
    - [Interaction Model Definition](#interaction-model-definition)
    - [Explanation of the Interaction Model](#explanation-of-the-interaction-model)
  - [Logging](#logging)
  - [License](#license)
  - [Contributing](#contributing)
  - [Contact](#contact)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/kjpou1/BASIC_ALEXA_ASK_SKILL_TEMPLATE.git
cd BASIC_ALEXA_ASK_SKILL_TEMPLATE
```

2. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Copy `example_env` to `.env` and configure your environment variables:

```bash
cp example_env .env
```

Edit `.env` and set the appropriate values for your configuration.

## Configuration

Configuration settings are managed using environment variables loaded from a `.env` file. The `Config` class in `app/config/config.py` handles loading these settings.

## Environment Variables

The following environment variables are used to configure the application. These should be defined in the `.env` file at the root of the project.

### SERVER_HOST

- **Description**: The host address on which the server will run.
- **Default Value**: `0.0.0.0`
- **Example**: `SERVER_HOST=0.0.0.0`

### SERVER_PORT

- **Description**: The port number on which the server will run.
- **Default Value**: `8080`
- **Example**: `SERVER_PORT=8080`

### INTENT

- **Description**: The custom intent to be handled by the skill.
- **Default Value**: `HelloWorldIntent`
- **Example**: `INTENT=HelloWorldIntent`

### DEBUG

- **Description**: Enables or disables debug mode.
- **Default Value**: `true`
- **Example**: `DEBUG=true`

### SSL_CERTIFICATE

- **Description**: The path to the SSL certificate file.
- **Default Value**: `/etc/ssl/private/insecure.pem`
- **Example**: `SSL_CERTIFICATE="/etc/ssl/private/insecure.pem"`

### SSL_PRIVATE_KEY

- **Description**: The path to the SSL private key file.
- **Default Value**: `/etc/ssl/insecure.key`
- **Example**: `SSL_PRIVATE_KEY="/etc/ssl/insecure.key"`

## Generating a Self-Signed SSL Certificate

For testing purposes, you can generate a self-signed SSL certificate using the provided `self-signed-certificate.sh` script. This is not recommended for production use.

### Script: self-signed-certificate.sh

```bash
#!/bin/bash

# Create necessary directories
sudo mkdir -p /etc/ssl/private

# Create a self signed SSL certificate.
sudo openssl req -new -newkey rsa:4096 -x509 -days 3650 -nodes \
             -subj /C=US/ST=NY/L=NY/O=NA/CN=localhost \
             -keyout /etc/ssl/insecure.key -out /etc/ssl/private/insecure.pem

# Create a DHParam file. Use 4096 bits instead of 2048 bits in production.
sudo openssl dhparam -out /etc/ssl/dhparam.pem 2048
```

### Instructions

1. Make the script executable:

```bash
chmod +x self-signed-certificate.sh
```

2. Run the script to generate the SSL certificate and private key:

```bash
./self-signed-certificate.sh
```

The `PermissionError: [Errno 13] Permission denied` error indicates that the process does not have the necessary permissions to access the certificate and key files. Here’s how you can resolve it:

### Solution

1. **Check File Permissions**
   Ensure that the certificate and key files have the appropriate permissions.

   ```bash
   sudo chmod 644 /etc/ssl/private/insecure.pem
   sudo chmod 644 /etc/ssl/insecure.key
   ```

2. **Ensure Ownership**
   Ensure that the files are owned by the user running the application.

   ```bash
   sudo chown $(whoami):$(whoami) /etc/ssl/private/insecure.pem
   sudo chown $(whoami):$(whoami) /etc/ssl/insecure.key
   ```

### Updated `README.md` for Permissions

```markdown
## Generating a Self-Signed SSL Certificate

### Ensure Directory and File Permissions

1. Create necessary directories:

   ```bash
   sudo mkdir -p /etc/ssl/private
   ```

2. Create the self-signed certificate and key:

   ```bash
   ./self-signed-certificate.sh
   ```

3. Set appropriate permissions:
    if PermissionError: [Errno 13] Permission denied

   ```bash
   sudo chmod 644 /etc/ssl/private/insecure.pem
   sudo chmod 644 /etc/ssl/insecure.key
   ```

4. Ensure ownership:
    PermissionError: [Errno 13] Permission denied

   ```bash
   sudo chown $(whoami):$(whoami) /etc/ssl/private/insecure.pem
   sudo chown $(whoami):$(whoami) /etc/ssl/insecure.key
   ```

This will create the following files:
- `/etc/ssl/insecure.key`: The private key file.
- `/etc/ssl/private/insecure.pem`: The SSL certificate file.
- `/etc/ssl/dhparam.pem`: The DH parameter file.

> [!NOTE]  
>  Ensure the `/etc/ssl/private` directory exists before running the script. This script creates self-signed certificates for testing purposes only and is not recommended for production environments.
> [!WARN]  
>  Permissions are sometimes operating system dependent.  Follow your own permissions strategy.

## Troubleshooting SSL Configuration

If you encounter the following error:
```
oscrypto.errors.LibraryNotFoundError: Error detecting the version of libcrypto
```
It indicates that the required cryptographic libraries are not found on your system. Follow these steps to resolve the issue:

1. Ensure OpenSSL is installed.

### On Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install openssl libssl-dev
```

### On CentOS/RHEL
```bash
sudo yum install openssl openssl-devel
```

### On macOS
If you are using Homebrew, you can install OpenSSL as follows:
```bash
brew install openssl
brew link openssl --force
```

2. Reinstall the `cryptography` library.
```bash
pip uninstall cryptography
pip install cryptography
```

3. Verify OpenSSL version in Python.
```python
import ssl
print(ssl.OPENSSL_VERSION)
```

### Updated Solution for Raspberry Pi

To resolve the `LibraryNotFoundError` related to `libcrypto` on a Raspberry Pi, follow these steps:

### 1. Upgrade `oscrypto` Package

#### Method 1: Directly from GitHub
Install the latest fixed revision of `oscrypto`:

```bash
pip install --force-reinstall https://github.com/wbond/oscrypto/archive/d5f3437ed24257895ae1edd9e503cfb352e635a8.zip
```

#### Method 2: Using `requirements.txt`
Add the GitHub URL to your `requirements.txt`:

```text
# requirements.txt
https://github.com/wbond/oscrypto/archive/d5f3437ed24257895ae1edd9e503cfb352e635a8.zip
```

Then run:

```bash
pip install --force-reinstall -r requirements.txt
```

### 2. Use a Different Version of OpenSSL

If upgrading `oscrypto` does not work, try using OpenSSL version 3.1.x or downgrading to an earlier version like 3.0.9.

For more detailed steps and information, visit the [Snowflake Community article](https://community.snowflake.com/s/article/Python-Connector-fails-to-connect-with-LibraryNotFoundError-Error-detecting-the-version-of-libcrypto).


If you continue to experience issues, you may need to recompile Python with the correct OpenSSL paths.

## Running the Server

The server is run using Gevent.

### Running the Server

```bash
python run.py
```

### Updated Request Handlers Section

## Request Handlers

The Alexa skill uses several request handlers to manage different types of requests. Here are the handlers included in this project:

### LaunchRequestHandler

**Purpose**: Handles the launch request when the user starts the skill.

**Response**: Welcomes the user to the skill.

```python
class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("Handling LaunchRequest")
        template_renderer = JinjaTemplateRenderer()
        speech_text = template_renderer.render_string_template("welcome_text")
        return (
            handler_input.response_builder.speak(speech_text)
            .set_should_end_session(False)
            .response
        )
```

### CustomIntentHandler

**Purpose**: Handles a custom intent to control an LED based on user commands.

**Response**: Turns the LED on or off based on the user's command.

```python
class CustomIntentHandler(AbstractRequestHandler):
    intent = Config().intent

    def can_handle(self, handler_input):
        return is_intent_name(self.intent)(handler_input)

    def handle(self, handler_input):
        logger.info("Handling %s", self.intent)

        # Extract the OnOff slot value from the request
        slots = handler_input.request_envelope.request.intent.slots
        command = slots.get("OnOff").value if slots.get("OnOff") else None

        renderer = JinjaTemplateRenderer()

        if command is None:
            # No command was given
            reprompt_text = renderer.render_string_template("command_reprompt")
            return (
                handler_input.response_builder.speak(reprompt_text)
                .ask(reprompt_text)
                .response
            )
        elif command in ['on', 'off']:
            led_service = LEDService()
            if command == "off":
                # Turn off
                led_service.turn_led_off()
            else:
                # Turn on
                led_service.turn_led_on()

            response_text = renderer.render_string_template('command', onOffCommand=command)
            return (
                handler_input.response_builder.speak(response_text)
                .set_card(SimpleCard("Command", response_text))
                .response
            )
        else:
            # A valid command was not given
            reprompt_text = renderer.render_string_template("command_reprompt")
            return (
                handler_input.response_builder.speak(reprompt_text)
                .ask(reprompt_text)
                .response
            )
```

### SessionEndedRequestHandler

**Purpose**: Handles the end of a session.

**Response**: Logs the reason for the session ending.

```python
class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("Session ended with reason: %s", handler_input.request_envelope.request.reason)
        return handler_input.response_builder.response
```

### FallbackIntentHandler

**Purpose**: Handles unrecognized intents using the `AMAZON.FallbackIntent`.

**Response**: Asks the user to rephrase their request.

```python
class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("Handling AMAZON.FallbackIntent")
        template_renderer = JinjaTemplateRenderer()
        speech_text = template_renderer.render_string_template("command_reprompt")
        return (
            handler_input.response_builder.speak(speech_text)
            .ask(speech_text)  # Keeps the session open to receive further input
            .response
        )
```

### GoodbyeIntentHandler

**Purpose**: Handles the `GoodbyeIntent`.

**Response**: Says goodbye to the user and ends the session.

```python
class GoodbyeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("GoodbyeIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("Handling GoodbyeIntent")
        template_renderer = JinjaTemplateRenderer()
        speech_text = template_renderer.render_string_template("goodbye")
        return (
            handler_input.response_builder.speak(speech_text)
            .set_should_end_session(True)
            .response
        )
```

### HelpIntentHandler

**Purpose**: Handles the `AMAZON.HelpIntent`.

**Response**: Provides help information to the user.

```python
class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("Handling AMAZON.HelpIntent")
        template_renderer = JinjaTemplateRenderer()
        speech_text = template_renderer.render_string_template("help")
        return (
            handler_input.response_builder.speak(speech_text)
            .ask(speech_text)  # Keeps the session open to receive further input
            .response
        )
```

### StopIntentHandler

**Purpose**: Handles the `AMAZON.StopIntent`.

**Response**: Says goodbye to the user and ends the session.

```python
class StopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("Handling AMAZON.StopIntent")
        template_renderer = JinjaTemplateRenderer()
        speech_text = template_renderer.render_string_template("stop")

        return (
            handler_input.response_builder.speak(speech_text)
            .set_should_end_session(True)
            .response
        )
```


## Alexa Skill Interaction Model

The Alexa skill is defined by an interaction model, which specifies the intents, slots, and sample utterances that the skill recognizes.

### Interaction Model Definition

Here is the JSON definition of the interaction model for this skill:

```json
{
    "interactionModel": {
        "languageModel": {
            "invocationName": "light wizard",
            "intents": [
                {
                    "name": "AMAZON.CancelIntent",
                    "samples": []
                },
                {
                    "name": "AMAZON.HelpIntent",
                    "samples": []
                },
                {
                    "name": "AMAZON.StopIntent",
                    "samples": []
                },
                {
                    "name": "AMAZON.NavigateHomeIntent",
                    "samples": []
                },
                {
                    "name": "AMAZON.FallbackIntent",
                    "samples": []
                },
                {
                    "name": "OnOffIntent",
                    "slots": [
                        {
                            "name": "OnOff",
                            "type": "OnOffValue",
                            "samples": [
                                "{OnOff}"
                            ]
                        }
                    ],
                    "samples": [
                        "turn {OnOff}",
                        "{OnOff}",
                        "switch {OnOff}"
                    ]
                }
            ],
            "types": [
                {
                    "name": "OnOffValue",
                    "values": [
                        {
                            "name": {
                                "value": "off"
                            }
                        },
                        {
                            "name": {
                                "value": "on"
                            }
                        }
                    ]
                }
            ]
        },
        "dialog": {
            "intents": [
                {
                    "name": "OnOffIntent",
                    "confirmationRequired": false,
                    "prompts": {},
                    "slots": [
                        {
                            "name": "OnOff",
                            "type": "OnOffValue",
                            "confirmationRequired": false,
                            "elicitationRequired": true,
                            "prompts": {
                                "elicitation": "Elicit.Slot.1602566410765.1538124825991"
                            }
                        }
                    ]
                }
            ],
            "delegationStrategy": "ALWAYS"
        },
        "prompts": [
            {
                "id": "Elicit.Slot.1602566410765.1538124825991",
                "variations": [
                    {
                        "type": "PlainText",
                        "value": "Do you want to turn your LED on or off"
                    }
                ]
            }
        ]
    }
}
```

### Explanation of the Interaction Model

- **Invocation Name**: The name users say to start the skill (e.g., "Alexa, open hello world").
- **Intents**: The actions that the skill can perform, each represented by an intent. This includes built-in intents like `AMAZON.HelpIntent` and custom intents like `HelloWorldIntent`.
- **Slots**: Parameters that the intents can accept. In this case, `HelloWorldIntent` has a `firstname` slot of type `AMAZON.FirstName`.
- **Samples**: Example phrases users can say to invoke each intent. These help Alexa recognize different ways users might phrase their requests.
- **Dialog**: Defines the dialog management for the intents, including slot elicitation prompts to gather necessary information from the user.
- **Prompts**: Predefined responses Alexa can use to prompt the user for more information.


## Logging

Logging is configured to provide detailed information about the server's operations. Logs include timestamps, log levels, and messages, which are crucial for debugging and monitoring.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

If you want to contribute to this project, please fork the repository and submit a pull request with your changes.

## Contact

For any questions or issues, please open an issue on GitHub.




