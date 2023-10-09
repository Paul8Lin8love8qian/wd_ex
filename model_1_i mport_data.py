"""
model_1_
本代码有claims的外键约束
"""
import json
import os
import pymysql
import time

# 用于避免转义
if pymysql.__version__ >='1.0.0':
    from pymysql.converters import escape_string
else:
    escape_string = lambda x: pymysql.escape_string(x)

def item_or_property_data(record):
    #record is a dict

    #insert data into table "item" or "property"
    table = record["type"]

    table_id = record["id"]
    if "lastrevid" in record:
        las = record["lastrevid"]
        if "modified" in record:
            mod = record["modified"]
            op = f"INSERT INTO {table} ({table}_id, lastrevid, modified) \
                                VALUES ('{table_id}', '{las}', '{mod}')"
        else:
            op = f"INSERT INTO {table} ({table}_id, lastrevid) \
                            VALUES ('{table_id}', '{las}')"
    elif "modified" in record:
        mod = record["modified"]
        op = f"INSERT INTO {table} ({table}_id, modified) \
                                VALUES ('{table_id}', '{mod}')"
    else:
        op = f"INSERT INTO {table} ({table}_id) VALUES ('{table_id}')"
    cursor.execute(op)

    # insert data into table "item_labels"
    if "labels" in record:
        for language, label in record["labels"].items():
            label_value = escape_string(label["value"]) 
            op_label = f"INSERT INTO {table}_labels (item_label_id, language, value) \
                                    VALUES ('{table_id}', '{language}', '{label_value}')"
            cursor.execute(op_label)

    # insert data into table "item_aliases"
    if "aliases" in record:
        for language, alias in record["aliases"].items():
            for alia in alias:
                alias_value = escape_string(alia["value"])
                op_alias = f"INSERT INTO {table}_aliases (item_alias_id, language, value) \
                                        VALUES ('{table_id}', '{language}', '{alias_value}')"
                cursor.execute(op_alias)

    # insert data into table "item_descriptions"
    if "descriptions" in record:
        for language, description in record["descriptions"].items():
            description_value = escape_string(description["value"])
            op_description = f"INSERT INTO {table}_descriptions (item_description_id, language, value) \
                                    VALUES ('{table_id}', '{language}', '{description_value}')"
            cursor.execute(op_description)

    # insert data into table "sitelinks"
    if table == "item" and ("sitelinks" in record):
        for key, value in record["sitelinks"].items():
            site = escape_string(value["site"])
            title = escape_string(value["title"])
            badges = ""
            for badge in value["badges"]:
                badges = f"{badges} {badge}"
            url = value.get("url")
            if url is not None:
                url = escape_string(url)
                op_sitelink = f"INSERT INTO sitelinks (item_sitelink_id, site, title, badges, url) \
                        VALUES ('{table_id}', '{site}', '{title}', '{badges}', '{url}')"
            else:
                op_sitelink = f"INSERT INTO sitelinks (item_sitelink_id, site, title, badges) \
                        VALUES ('{table_id}', '{site}', '{title}', '{badges}')"
            cursor.execute(op_sitelink)
    


def statement_data(record, snake_id, reference_id):
    #insert data into table "snakes"

    claims = record["claims"] #claims is a dic
    item_id = record["id"]
    for property, claim in claims.items():
        # claim is a list
        for sta_value in claim:
            # sta_value  is a dict
            snake_id = mainsnake_data(sta_value, item_id, snake_id)
            if "qualifiers" in sta_value:
                snake_id = qualifiers_data(sta_value, snake_id)
            if "references" in sta_value:
                snake_id, reference_id = reference_data(sta_value, snake_id, reference_id)
        
    return (snake_id, refenence_id)


def reference_data(sta_value, snake_id, reference_id):
    claim_reference_id = sta_value["id"]
    references = sta_value["references"]
    for reference in references:
        # insert data into table "references"
        snake_order = reference["snaks-order"]
        op_reference = f"INSERT INTO refenences (reference_id, claim_reference_id, snake_order) \
                                        VALUES ({reference_id}, '{claim_reference_id}', '{snake_order}')"
        cursor.execute(op_reference)

        snaks = reference["snaks"]
        for pro, snake in snaks.items():
            # insert data into table "snakes"
            snakes_data(snake, snake_id)

            # insert data into table "references_snake"
            op_reference_snake = f"INSERT INTO references_snake (reference_id, snake_reference_snake_id) \
                                                        VALUES ({reference_id}, {snake_id})"
            cursor.execute(op_reference_snake)
            snake_id += 1
        reference_id += 1
    return (snake_id, reference_id)

def qualifiers_data(sta_value, snake_id):
    
    qualifiers = sta_value["qualifiers"]
    claim_qualifier_id = sta_value["id"]
    for pro, qualifier in qualifiers.items():
        for qua_value in qualifier:
            # insert data into table "snakes"
            snakes_data(qua_value, snake_id)

            #insert data into table "qualifiers"
            op_qualifier = f"INSERT INTO qualifiers (claim_qualifier_id, snake_qualifier_id) \
                                            VALUES ('{claim_qualifier_id}', {snake_id})"
            cursor.execute(op_qualifier)
            snake_id += 1
    return snake_id

def snakes_data(snake, snake_id):
    #insert data into the table "snakes"
    snaketype = snake["snaktype"]
    propert = snake["property"]
    if snaketype == "value":
        datavalue = trs_datavalue(snake["datavalue"])
        datatype = snake["datatype"]
        op_snake = f"INSERT INTO snakes (snake_id, snaketype, property, datavalue, datatype) \
                            VALUES ({snake_id}, '{snaketype}', '{propert}', '{datavalue}', '{datatype}')"
    else:
        op_snake = f"INSERT INTO snakes (snake_id, snaketype, property) \
                            VALUES ({snake_id}, '{snaketype}', '{propert}')"
    cursor.execute(op_snake)



def mainsnake_data(sta_value, item_id, snake_id):
    #sta_value is a dict

    # insert data into table "snakes"
    snakes_data(sta_value["mainsnak"], snake_id)

    # insert data into table "claims"
    claim_id = sta_value["id"]
    property_id = sta_value["mainsnak"]["property"]
    mainsnake_id = snake_id
    rank = sta_value["rank"]
    qualifiers_order = sta_value.get("qualifiers-order")
    #rank 是MySQL的保留字段 用反引号 ` 括起来解决
    if qualifiers_order is not None:
        op_mainsnake = f"INSERT INTO claims (claim_id, item_id, property_id, mainsnake_id, `rank`, qualifiers_order) \
                                    VALUES ('{claim_id}', '{item_id}', '{property_id}', {mainsnake_id}, '{rank}', {qualifiers_order})"
    else:
        op_mainsnake = f"INSERT INTO claims (claim_id, item_id, property_id, mainsnake_id, `rank`) \
                                    VALUES ('{claim_id}', '{item_id}', '{property_id}', {mainsnake_id}, '{rank}')"
    print(op_mainsnake)
    cursor.execute(op_mainsnake)

    snake_id = snake_id + 1
    return snake_id

def trs_datavalue(datavalue):
    # datavalue is a dic

    d_type = datavalue["type"]
    if d_type == "string":
        return datavalue["value"]
    elif d_type == "wikibase-entityid":
        return datavalue["value"]["id"]
    elif d_type == "globecoordinate":
        latitude = str(datavalue["value"]["latitude"])
        longitude = str(datavalue["value"]["longitude"])
        altitude = str(datavalue["value"]["altitude"])
        precision = str(datavalue["value"]["precision"])
        return f"{latitude} {longitude} {altitude} {precision} " + escape_string(datavalue["value"]["globe"])
    elif d_type == "quantity":
        return datavalue["value"]["amount"] + " unit: " + escape_string(datavalue["value"]["unit"])
    elif d_type == "time":
        return datavalue["value"]["time"]
    elif d_type == "monolingualtext":
        return datavalue["value"]["text"]
    else:
        print(f"unkown datatype: {d_type}")

file_path = os.path.join("C", "Users", "zsl", "Desktop", "Database", "example", "chunk_0.json")
test_path = "E:\\code\\python\\wikidata\\wikidata_test.json"
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="13888332103Zsl!",
    database="wikidata_model_1"
)

cursor = connection.cursor()

"""
对于未分割文件
格式为：
[{},\n{},\n]

with open(file_path, 'r', encoding='utf-8') as file:
    for i, line in enumerate(file):
        try:
            line = line.rstrip(",\n") #delete ',' or '\n'
            record = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"the {i} line error")
        else:
            item_or_property_data(record)
            snake_id = 0
            reference_id = 0
            snake_id, refenence_id= statement_data(record, snake_id, reference_id)

"""
#分割文件 格式为["{},{}"]
start_time = time.time()
with open(test_path, 'r', encoding='utf-8') as file:
    data = json.load(file) #file为包含10000个元素的列表
    snake_id = 0
    reference_id = 0
    for record in data:
        item_or_property_data(record)
    for record in data:
        snake_id, refenence_id= statement_data(record, snake_id, reference_id)
end_time = time.time()
print(f"加载到数据库时间：{start_time - end_time} 秒")

cursor.close()
connection.close()