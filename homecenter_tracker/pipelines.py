# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import datetime

import psycopg2

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings


class HomecenterTrackerPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()

        for field_name in field_names:
            value = adapter.get(field_name)

            if field_name == "price":
                adapter[field_name] = self.format_price(value)

            if field_name == "id":
                adapter[field_name] = self.format_id(value)

        return item

    def format_price(self, price):
        return int(price.replace("$", "").replace(".", "").replace(",", "").strip())

    def format_id(self, id_source):
        id_index = id_source.split("/").index("product") + 1
        id = id_source.split("/")[id_index]
        return id


class SaveToPostgresPipeline:
    def __init__(self):
        ## Connection Details
        settings = get_project_settings()
        hostname = settings.get("DB_HOST")
        username = settings.get("DB_USER")
        password = settings.get("DB_PW")
        database = settings.get("DB_NAME")

        ## Create/Connect to database

        try:
            self.connection = psycopg2.connect(
                host=hostname, user=username, password=password, dbname=database
            )

            ## Create cursor, used to execute commands
            self.cur = self.connection.cursor()
            self.connected = True

        except ValueError as e:
            self.connected = False

    def process_item(self, item, spider):
        if not self.connected:
            print("Database connection not established.")
            return item

        try:
            self.cur.execute(
                """INSERT INTO products (
                    id,
                    name
                ) VALUES (
                    %s,
                    %s
                ) ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name RETURNING id""",
                (
                    item["id"],
                    item["name"],
                ),
            )

            ## get the id of the i
            # nserted row from result:
            inserted_id = self.cur.fetchone()
            if inserted_id:
                current_date = datetime.date.today()
                print(f"Inserted row with id: {inserted_id[0]}")
                self.cur.execute(
                    """INSERT INTO track_history (
                        product_id,
                        price,
                        date
                    ) VALUES (
                        %s,
                        %s,
                        %s
                    ) ON CONFLICT DO NOTHING""",
                    (item["id"], item["price"], current_date),
                )

            ## Commit the transaction
            self.connection.commit()

        except psycopg2.Error as e:
            self.connection.rollback()
            print("Could not insert item with id:", item["id"], "Reason:", e)

        return item

    def close_spider(self, spider):

        ## Close cursor & connection to database
        self.cur.close()
        self.connection.close()
