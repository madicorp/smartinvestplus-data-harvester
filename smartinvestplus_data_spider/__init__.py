import pinject

from smartinvestplus_data_spider.pipelines.mongo_dao import MongoDao

CRAWLER_OBJ_GRAPH = pinject.new_object_graph(modules=None, classes=[MongoDao])
