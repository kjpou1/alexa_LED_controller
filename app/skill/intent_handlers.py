import logging

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_model.ui import SimpleCard  

from app.config.config import Config
from app.helpers.template_renderer import JinjaTemplateRenderer
from app.service.led_service import LEDService

# Set up logging
logger = logging.getLogger(__name__)

# Initialize Jinja2 template renderer with YAML templates
# Make sure this is executed before any usage in the handlers.
JinjaTemplateRenderer.initialize(
    template_folder="views", yaml_file="app/resources/templates.yaml"
)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

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


import logging
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model.ui import SimpleCard
from app.service.led_service import LEDService
from app.helpers.template_renderer import JinjaTemplateRenderer
from app.config.config import Config

logger = logging.getLogger(__name__)

class CustomIntentHandler(AbstractRequestHandler):
    """
    Handler for Custom Intent. Manages the LED based on user commands.
    """

    intent = Config().intent

    def can_handle(self, handler_input):
        """
        Determines if this handler can handle the given request.
        
        :param handler_input: The input request from Alexa.
        :return: True if the intent matches, False otherwise.
        """
        return is_intent_name(self.intent)(handler_input)

    def handle(self, handler_input):
        """
        Handles the custom intent to turn the LED on or off.
        
        :param handler_input: The input request from Alexa.
        :return: A response indicating the result of the command.
        """
        logger.info("Handling %s", self.intent)

        # Extract the OnOff slot value from the request
        slots = handler_input.request_envelope.request.intent.slots
        command = slots.get("OnOff").value if slots.get("OnOff") else None

        renderer = JinjaTemplateRenderer()

        if command is None:
            # No command was given
            reprompt_text = renderer.render_string_template("command_reprompt")
            return (
                handler_input.response_builder
                .speak(reprompt_text)
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
                handler_input.response_builder
                .speak(response_text)
                .set_card(SimpleCard("Command", response_text))
                .response
            )
        else:
            # A valid command was not given
            reprompt_text = renderer.render_string_template("command_reprompt")
            return (
                handler_input.response_builder
                .speak(reprompt_text)
                .ask(reprompt_text)
                .response
            )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        logger.info(
            "Session ended with reason: %s",
            handler_input.request_envelope.request.reason,
        )
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for AMAZON.FallbackIntent."""

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("Handling AMAZON.FallbackIntent")
        # speech_text = "Sorry, I didn't understand that. Can you please rephrase?"
        template_renderer = JinjaTemplateRenderer()
        speech_text = template_renderer.render_string_template("command_reprompt")
        return (
            handler_input.response_builder.speak(speech_text)
            .ask(speech_text)  # Keeps the session open to receive further input
            .response
        )


class GoodbyeIntentHandler(AbstractRequestHandler):
    """Handler for Goodbye Intent."""

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


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for AMAZON.HelpIntent."""

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


class StopIntentHandler(AbstractRequestHandler):
    """Handler for AMAZON.StopIntent."""

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
