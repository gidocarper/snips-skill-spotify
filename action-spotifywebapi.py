#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes, MqttOptions
import configparser
import io
from musicPlayer import MuuzikPlayer
import toml

USERNAME_INTENTS = "mcitar"
MQTT_BROKER_ADDRESS = "localhost:1883"
MQTT_USERNAME = None
MQTT_PASSWORD = None


def add_prefix(intent_name):
    return USERNAME_INTENTS + ":" + intent_name

def read_configuration_file():
    try:
        cp = configparser.ConfigParser()
        with io.open("config.ini", encoding="utf-8") as f:
            cp.read_file(f)
        return {section: {option_name: option for option_name, option in cp.items(section)}
                for section in cp.sections()}
    except (IOError, configparser.Error):
        return dict()

def intent_callback_playSong(hermes, intent_message):
    hermes.publish_end_session(intent_message.session_id, musicPlayer.play(hermes, intent_message))

def intent_callback_next(hermes, intent_message):
    hermes.publish_end_session(intent_message.session_id, musicPlayer.next(hermes, intent_message))

def intent_callback_previous(hermes, intent_message):
    hermes.publish_end_session(intent_message.session_id, musicPlayer.previous(hermes, intent_message))

def intent_callback_pause(hermes, intent_message):
    hermes.publish_end_session(intent_message.session_id, musicPlayer.pause(hermes, intent_message))

def intent_callback_repeat(hermes, intent_message):
    hermes.publish_end_session(intent_message.session_id, musicPlayer.repeat(hermes, intent_message))


if __name__ == "__main__":
    config = read_configuration_file()
    translator = Translator(config)

    snips_config = toml.load('/etc/snips.toml')
    if 'mqtt' in snips_config['snips-common'].keys():
        MQTT_BROKER_ADDRESS = snips_config['snips-common']['mqtt']
    if 'mqtt_username' in snips_config['snips-common'].keys():
        MQTT_USERNAME = snips_config['snips-common']['mqtt_username']
    if 'mqtt_password' in snips_config['snips-common'].keys():
        MQTT_PASSWORD = snips_config['snips-common']['mqtt_password']
    mqtt_opts = MqttOptions(username=MQTT_USERNAME, password=MQTT_PASSWORD, broker_address=MQTT_BROKER_ADDRESS)

    with Hermes(MQTT_ADDR) as h:
        h.subscribe_intent('previousSong', intent_callback_previous) \
            .subscribe_intent('nextSong', intent_callback_next) \
            .subscribe_intent('mcitar:play', intent_callback_playSong) \
            .subscribe_intent('mcitar:playresource', intent_callback_playSong) \
            .subscribe_intent('mcitar:playSong', intent_callback_playSong) \
            .subscribe_intent('mcitar:pause', intent_callback_pause) \
            .subscribe_intent('resumeMusic', resumeMusic) \
            .subscribe_intent('speakerInterrupt', speakerInterrupt) \
            .subscribe_intent('mcitar:playAlbum', intent_callback_playSong) \
            .subscribe_intent('mcitar:playArtist', intent_callback_playSong) \
            .subscribe_intent('mcitar:playPlaylist', playPlaylist) \
            .subscribe_intent('getInfos', getInfos) \
            .subscribe_intent('addSong', addSong) \
            .subscribe_intent('mcitar:shuffleMode', modeEnable) \
            .subscribe_intent('mcitar:modeEnable', modeEnable) \
            .subscribe_intent('mcitar:modeDisable', modeDisable) \
            .loop_forever()
