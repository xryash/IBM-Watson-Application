import json
import logging
from wiotp.sdk import application as iot

from postgres_repository import EventEntity
from utils import get_digest


class WatsonClient(object):
    def __init__(self, logger, auth_config, events, repository):
        """WatsonClient constructor"""
        self.logger = logger
        self.client = iot.ApplicationClient(config=auth_config)
        self.events = events
        self.repository = repository
        self.active_devices = []


    def connect(self):
        """Connect to a cloud and set callbacks"""
        self.logger.info('.connect() entered')
        self.client.connect()
        self.__subscribe_to_events()
        self.__subscribe_to_statuses()
        self.__set_event_callback(self.__event_callback)
        self.__set_status_callback(self.__status_callback)
        self.repository.create_tables()


    def disconnect(self):
        """Disconnect a client"""
        self.logger.info('.disconnect() entered')

        try:
            self.__set_event_callback()
            self.__set_status_callback()
            self.active_devices = []
            self.client.disconnect()

        except Exception as err:
            print(str(err))


    def __subscribe_to_events(self):
        """Subscribe a client to events contained in the list"""
        self.logger.info('.__subscribe_to_events() entered')
        for event in self.events:
            self.client.subscribeToDeviceEvents(eventId=event)


    def __subscribe_to_statuses(self):
        """Subscribe a client to device statuses"""
        self.logger.info('.__subscribe_to_status() entered')
        self.client.subscribeToDeviceStatus()


    def __set_event_callback(self, func=None):
        """Set a callback for device events"""
        self.logger.info('.__set_event_callback() entered')
        self.client.deviceEventCallback = func


    def __event_callback(self, event):
        """Event callback function"""
        self.logger.info('.__event_callback() entered')
        str = "%s event '%s' received from %s device [%s]: %s"
        self.logger.info(str % (event.format, event.eventId, event.typeId, event.device, json.dumps(event.data)))
        if event.eventId == 'step':
            self.__step_event_handler(event)


    def __step_event_handler(self, event):
        """Handle events with id 'step'"""
        self.logger.info('.__step_event_handler() entered')
        hashcode = get_digest(event.timestamp)
        event_id = event.eventId
        device_id = event.deviceId
        type_id = event.typeId
        time_stamp = event.data['timestamp']
        step_count = event.data['step_count']

        entity = EventEntity(hashcode, event_id,
                             device_id, type_id,
                             time_stamp, step_count)
        self.logger.info('Prepared object: %s' % entity)
        self.repository.save_event(entity)


    def __set_status_callback(self, func=None):
        """Set a callback for device status"""
        self.logger.info('.__set_status_callback() entered')
        self.client.deviceStatusCallback = func


    def __status_callback(self, status):
        """Status callback function"""
        self.logger.info('.__status_callback() entered')
        if status.action is 'Disconnect':
            if status.deviceId in self.active_devices:
                self.active_devices.remove(status.deviceId)
        elif status.action is 'Connect':
            self.active_devices.append(status.deviceId)
        str = '%s - device %s - %s (%s)'
        self.logger.info(str % (status.time.isoformat(), status.device, status.action, status.reason))





