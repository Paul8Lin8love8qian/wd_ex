import json

def load_jsonl_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        data = []
        for line in lines:
            data.append(json.loads(line))
        return data


def read_jsonl(file_name):
    with open(file_name, "r", encoding='utf-8') as f:
        data = []
        lines = f.readlines()
        for line in lines:
            data.append(json.loads(line))
        return data

def write_jsonl(file_name, datas):
    with open(file_name, "w", encoding='utf-8') as f:
        for data in datas:
            json.dump(data, f, ensure_ascii=False)
            f.write("\n")


"""
file_path = "F:\\wikidata\\20141027.json"
output_file = "sub_wikidata.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
    chunk = data[:1000]

with open(output_file, 'w') as outfile:
    json.dump(chunk, outfile)
"""

def split_json_file(file_path, chunk_size):
    with open(file_path, 'r', encoding='utf-8') as file:
        chunk_data = []
        chunk_index = 0
        record_count = 0

        for line in file:
            try:
                line = line.rstrip(",\n")
                #第一行为"[\n", 不是完整的json对象 
                record = json.loads(line) #loads用于加载字符流， load用于加载json文件, #loads加载后是一个list
                print(type(record))
            except json.JSONDecodeError as e:
                print("该行文件格式错误:", e)
            else:
                chunk_data.append(record)
                record_count += 1

                if record_count == chunk_size:
                    output_file = f'F:\\wikidata\\test_chunk_{chunk_index}.json'
                    with open(output_file, 'w', encoding='utf-8') as out_f:
                        #json.dump(chunk_data, out_f) #一整个存为json, 顶级为list
                        for data in chunk_data:
                            json.dump(data, out_f)
                            out_f.write("\n")

                    print(f"Created {output_file} with {record_count} records.")

                    chunk_index += 1
                    record_count = 0
                    chunk_data = []

        if record > 0:
            output_file = f'F:\\wikidata\\chunk_{chunk_index}.json'
            with open(output_file, 'w', encoding='utf-8') as out_f:
                json.dump(chunk_data, out_f)

            print(f"Created {output_file} with {record_count} records.")



file_path = "F:\\wikidata\\20141027.json"
split_json_file(file_path, 10000)
            
