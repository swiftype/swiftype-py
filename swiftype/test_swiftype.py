import swiftype
import os
import time
import unittest

class TestClientFunctions(unittest.TestCase):
    def setUp(self):
        try:
            api_key = os.environ['API_KEY']
        except:
            api_key = "DUMMY_KEY"

        self.client = swiftype.Client(api_key=api_key, host=os.environ['API_HOST'])
        self.engine = 'engine'
        self.document_type = 'doctype'

    def test_engines(self):
        self.__is_expected_collection(self.client.engines, 200, 2, {'id': '1'})

    def test_engine(self):
        slug = self.client.engine(self.engine)['body']['slug']
        self.assertEquals(slug, self.engine)

    def test_engine_create(self):
        slug = self.client.create_engine(self.engine)['body']['slug']
        self.assertEqual(slug, self.engine)

    def test_engine_delete(self):
        response = self.client.destroy_engine(self.engine)
        self.assertEqual(response['status'], 204)

    def test_document_types(self):
        self.__is_expected_collection(self.client.document_types, 200, 2, {'slug': 'doctype1'}, self.engine)

    def test_document_type(self):
        self.__is_expected_result(self.client.document_type, 200, {'slug': self.document_type}, self.engine, self.document_type)

    def test_create_document_type(self):
        slug = self.client.create_document_type(self.engine, self.document_type)['body']['slug']
        self.assertEqual(slug, self.document_type)

    def test_destroy_document_type(self):
        response = self.client.destroy_document_type(self.engine, self.document_type)
        self.assertEqual(response['status'], 204)

    def test_documents(self):
        self.__is_expected_collection(self.client.documents, 200, 2, {'external_id': '1'}, self.engine, self.document_type)

    def test_documents_pagination(self):
        self.__is_expected_collection(self.client.documents, 200, 2, {'external_id': '1'}, self.engine, self.document_type, 2, 10)

    def test_document(self):
        external_id = '1'
        id = self.client.document(self.engine, self.document_type, external_id)['body']['external_id']
        self.assertEqual(id, external_id)

    def test_create_document(self):
        doc_id = 'doc_id'
        id = self.client.create_document(self.engine, self.document_type, {'external_id': doc_id})['body']['external_id']
        self.assertEqual(id, doc_id)

    def test_create_documents(self):
        docs = [{'external_id': 'doc_id1'}, {'external_id': 'doc_id2'}]
        stati = self.client.create_documents(self.engine, self.document_type, docs)['body']
        self.assertEqual(stati, [True, True])

    def test_create_or_update_document(self):
        id = '1'
        external_id = self.client.create_or_update_document(self.engine, self.document_type, {'external_id': id, 'fields': {}})['body']['external_id']
        self.assertEqual(external_id, id)

    def test_create_or_update_documents(self):
        docs = [{'external_id': '1'}, {'external_id': '2'}]
        stati = self.client.create_or_update_documents(self.engine, self.document_type, docs)['body']
        self.assertEqual(stati, [True, True])

    def test_update_document(self):
        document_id = '1'
        id = self.client.update_document(self.engine, self.document_type, document_id, {'title': 'title'})['body']['id']
        self.assertEqual(id, document_id)

    def test_update_documents(self):
        documents = [{'external_id': '1'}, {'external_id': '2'}]
        stati = self.client.update_documents(self.engine, self.document_type, documents)['body']
        self.assertEqual(stati, [True, True])

    def test_destroy_document(self):
        response = self.client.destroy_document(self.engine, self.document_type, 'id')
        self.assertEqual(response['status'], 204)

    def test_destroy_documents(self):
        documents = ['1', '2']
        stati = self.client.destroy_documents(self.engine, self.document_type, documents)['body']
        self.assertEqual(stati, [True, True])

    def test_search(self):
        total_count = len(self.client.document_types(self.engine)['body'])
        self.assertTrue(total_count > 1)
        self.__is_expected_search_result(self.client.search, total_count)

    def test_search_with_options(self):
        total_count = len(self.client.document_types(self.engine)['body'])
        self.assertTrue(total_count > 1)
        response = self.client.search(self.engine, 'query', {'page': 2})
        self.assertEqual(len(response['body']['records']), total_count)

    def test_search_document_type(self):
        self.__is_expected_search_result(self.client.search_document_type, 1, [self.document_type])

    def test_search_document_type_with_options(self):
        response = self.client.search_document_type(self.engine, self.document_type, "query", {'page': 2})
        self.assertEqual(len(response['body']['records']), 1)

    def test_suggest(self):
        total_count = len(self.client.document_types(self.engine)['body'])
        self.assertTrue(total_count > 1)
        self.__is_expected_search_result(self.client.suggest, total_count)

    def test_suggest_with_options(self):
        total_count = len(self.client.document_types(self.engine)['body'])
        self.assertTrue(total_count > 1)
        response = self.client.suggest(self.engine, 'query', {'page': 2})
        self.assertEqual(len(response['body']['records']), total_count)

    def test_suggest_document_type(self):
        self.__is_expected_search_result(self.client.suggest_document_type, 1, [self.document_type])

    def test_suggest_document_type_with_options(self):
        response = self.client.suggest_document_type(self.engine, self.document_type, "query", {'page': 2})
        self.assertEqual(len(response['body']['records']), 1)

    def test_analytics_searches(self):
        searches = self.client.analytics_searches(self.engine)['body']
        self.assertTrue(len(searches) == 1)

    def test_analytics_searches_pagination(self):
        searches = self.client.analytics_searches(self.engine, '2013-01-01', '2013-02-01')['body']
        self.assertTrue(len(searches) == 0)

    def test_analytics_autoselects(self):
        autoselects = self.client.analytics_autoselects(self.engine)['body']
        self.assertTrue(len(autoselects) == 1)

    def test_analytics_autoselects_pagination(self):
        autoselects = self.client.analytics_autoselects(self.engine, '2013-01-01', '2013-02-01')['body']
        self.assertTrue(len(autoselects) == 0)

    def test_analytics_top_queries(self):
        top_queries = self.client.analytics_top_queries(self.engine)['body']
        self.assertTrue(len(top_queries) == 2)

    def test_analytics_top_queries_pagination(self):
        top_queries = self.client.analytics_top_queries(self.engine, 2, 10)['body']
        self.assertTrue(len(top_queries) == 0)

    def test_analytics_top_queries_in_range(self):
        top_queries = self.client.analytics_top_queries_in_range(self.engine, '2013-01-01', '2013-02-01')['body']
        self.assertTrue(len(top_queries) == 1)

    def test_analytics_top_no_result_queries(self):
        autoselects = self.client.analytics_top_no_result_queries(self.engine)['body']
        self.assertTrue(len(autoselects) == 2)

    def test_analytics_top_no_result_queries_with_dates(self):
        autoselects = self.client.analytics_top_no_result_queries(self.engine, '2013-01-01', '2013-02-01')['body']
        self.assertTrue(len(autoselects) == 0)

    def test_domains(self):
        domains = self.client.domains(self.engine)['body']
        self.assertTrue(len(domains) == 2)

    def test_domain(self):
        domain_id = 'domain_id'
        domain = self.client.domain(self.engine, domain_id)['body']
        self.assertEqual(domain['id'], domain_id)

    def test_create_domain(self):
        url = 'http://www.example.com'
        domain_url = self.client.create_domain(self.engine, url)['body']['submitted_url']
        self.assertEqual(domain_url, url)

    def test_destroy_domain(self):
        status = self.client.destroy_domain(self.engine, 'domain_id')['status']
        self.assertEqual(status, 204)

    def test_recrawl_domain(self):
        domain_id = 'domain_id'
        domain = self.client.recrawl_domain(self.engine, domain_id)['body']
        self.assertEqual(domain['id'], domain_id)

    def test_crawl_url(self):
        domain_id = 'domain_id'
        url = 'http://www.example.com'
        crawled_url = self.client.crawl_url(self.engine, domain_id, url)['body']['url']
        self.assertEqual(crawled_url, url)

    def __is_expected_search_result(self, request, document_type_count, args=[]):
        response = request(self.engine, *(args + ['*']))
        self.assertEqual(len(response['body']['records']), document_type_count)

    def __is_expected_result(self, request, status_code, expected_values, *args):
        response = request(*args)
        self.assertEqual(response['status'], status_code)
        for k,v in expected_values.iteritems():
            self.assertEqual(response['body'][k], v)

    def __is_expected_collection(self, request, status_code, collection_length, expected_values, *args):
        response = request(*args)
        self.assertEqual(response['status'], status_code)
        self.assertEqual(len(response['body']), collection_length)
        for k,v in expected_values.iteritems():
            self.assertEqual(len([item for item in response['body'] if item[k] == v]), 1)

    def __time_name(self):
        return str(int(time.mktime(time.gmtime())))

    def __create_temporary_engine(self, name = None):
        name = name if name else self.__time_name()
        return

if __name__ == '__main__':
    unittest.main()
