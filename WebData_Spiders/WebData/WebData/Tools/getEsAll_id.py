from elasticsearch_dsl.connections import connections


def get_all_id():
    es = connections.create_connection(hosts=['localhost'])

    all_id = []
    all_data = es.search('qa', body={"query": {"match_all": {}}, "_source": "url", "from": 0, "size": 10000000})['hits']['hits']
    for id in all_data:
        all_id.append(id['_id'])

    return all_id
