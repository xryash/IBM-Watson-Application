import psycopg2
import logging


class EventEntity(object):
    def __init__(self, hashcode, event_id,
                 device_id, type_id, time_stamp,
                 step_count):
        """EventEntity constructor"""
        self.hashcode = hashcode
        self.event_id = event_id
        self.device_id = device_id
        self.type_id = type_id
        self.time_stamp = time_stamp
        self.step_count = step_count


    def __str__(self):
        return 'EventEntity(hashcode={},event_id={},device_id={},type_id={},time_stamp={},step_count={})'\
            .format(self.hashcode, self.event_id,
                    self.device_id, self.type_id, self.time_stamp,
                    self.step_count)


class PostgresConnector(object):
    def __init__(self, host, database, port, user, password):
        """PostgresConnector constructor"""
        self.logger = logging.getLogger(__name__)
        self.logger.info('.__init__() entered')
        self.host = host
        self.database = database
        self.port = port
        self.user = user
        self.password = password
        self.connection = None


    SAVE_EVENT_QUERY = 'INSERT INTO step_events VALUES (%s, %s, %s, %s, %s, %s)'
    GET_DEVICE_EVENTS = 'SELECT * FROM step_events WHERE device_id = %s'
    GET_ALL_EVENTS = 'SELECT * FROM step_events'

    TABLES_SCRIPTS = [
        """
        CREATE TABLE IF NOT EXISTS step_events (
            hashcode VARCHAR(64) PRIMARY KEY,
            event_id VARCHAR(32) NOT NULL,
            device_id VARCHAR(32) NOT NULL,
            type_id VARCHAR(32) NOT NULL,
            time_stamp VARCHAR(32),
            step_count INTEGER  NOT NULL
        )
        """
    ]

    def __connect(self):
        """Connect to a database"""
        self.logger.info('.connect() entered')
        if self.connection is None:
            try:
                self.connection = psycopg2.connect(host=self.host, database=self.database,
                                                   port=self.port, user=self.user,
                                                   password=self.password)
            except (psycopg2.DatabaseError) as error:
                self.logger.error('.connect() received exception: %s' % str(error))
                self.connection = None
                return 0
        return 1


    def __disconnect(self):
        """Disconnect from a database"""
        if self.connection is not None:
            self.logger.info('.disconnect() entered')
            try:
                self.connection.close()
                self.connection = None
            except (psycopg2.DatabaseError) as error:
                self.logger.error('.disconnect() received exception: %s' % str(error))
                return 0
        return 1


    def create_tables(self):
        """Create tables in a database"""
        self.logger.info('.create_tables() entered')
        try:
            if self.__connect() is 1:
                cursor = self.connection.cursor()
                for table in self.TABLES_SCRIPTS:
                    cursor.execute(table)
                cursor.close()
                self.connection.commit()
                if self.__disconnect() is 1:
                    return 1
        except (psycopg2.DatabaseError, psycopg2.DataError) as error:
            self.logger.error('.create_tables() received exception: %s' % str(error))
        finally:
            return 0


    def save_event(self, entity):
        """Save event data to database"""
        self.logger.info('.save_event() entered')
        try:
            if self.__connect() is 1:
                cursor = self.connection.cursor()
                cursor.execute(self.SAVE_EVENT_QUERY, [entity.hashcode, entity.event_id,
                                                       entity.device_id, entity.type_id, entity.time_stamp,
                                                       entity.step_count])
                cursor.close()
                self.connection.commit()
                if self.__disconnect() is 1:
                    return 1
        except (psycopg2.DatabaseError, psycopg2.DataError) as error:
            self.logger.error('.save_event() received exception: %s' % str(error))
        finally:
            return 0


    def get_events(self, device_id = None):
        """Get all events about specific device or all devices"""
        self.logger.info('.get_events() entered')
        try:
            if self.__connect() is 1:
                cursor = self.connection.cursor()
                if device_id is None:
                    cursor.execute(self.GET_ALL_EVENTS)
                else:
                    cursor.execute(self.GET_DEVICE_EVENTS, [device_id])
                result = cursor.fetchall()
                if self.__disconnect() is 1:
                    return result
        except (psycopg2.DatabaseError, psycopg2.DataError) as error:
            self.logger.error('.get_events() received exception: %s' % str(error))
        return []
