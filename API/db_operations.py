import psycopg2
import constants


class DbSession:
    def __init__(self, credentials, host, db):
        self.connection = psycopg2.connect(host=host, database=db,
                                           user=credentials.db_id, password=credentials.db_pass)

    def __del__(self):
        self.connection.close()

    def upload_package(self, pack):
        cursor = self.connection.cursor()

        try:
            # upload package
            pack_values = pack.to_tuple()
            cursor.execute(constants.PACKAGE_INSERT_QUERY, pack_values)
            count = cursor.rowcount
            print(count, "Record inserted successfully in packages table")

            # upload segments
            seg_values = [(pack.package_id,) + seg.to_tuple() for seg in pack.segments]
            cursor.executemany(constants.SEGMENT_INSERT_QUERY, seg_values)
            count = cursor.rowcount
            print(count, "Record inserted successfully in segments table")

            # upload data
            data_values = [(pack.package_id, seg.segment_id,) + seg.payload.to_tuple() for seg in pack.segments]
            cursor.executemany(pack.segments[0].payload.get_insert_query(), data_values)    # every segment has the
                                                                                            # same type of payload
            count = cursor.rowcount
            print(count, "Record inserted successfully in payload table")
        except (Exception, psycopg2.Error) as error:
            self.connection.rollback()
            raise error
        # commit
        finally:
            cursor.close()
        self.connection.commit()
