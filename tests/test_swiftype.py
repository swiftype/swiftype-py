from swiftype import swiftype
import os
import time
import unittest2 as unittest
from six.moves.urllib_parse import urlparse, parse_qs
import vcr
from mock import Mock

class TestClientFunctions(unittest.TestCase):

    def setUp(self):
        try:
            api_key = os.environ['API_KEY']
        except:
            api_key = "a-test-api-key"

        self.client = swiftype.Client(api_key=api_key, host='localhost:3000')
        self.engine = 'api-test'
        self.document_type = 'books'

    def test_engines(self):
        with vcr.use_cassette('fixtures/engines.yaml'):
            self.__is_expected_collection(self.client.engines, 200, 3, {'slug': 'api-test'})

    def test_engine(self):
        with vcr.use_cassette('fixtures/engine.yaml'):
            slug = self.client.engine(self.engine)['body']['slug']
            self.assertEqual(slug, self.engine)

    def test_engine_create(self):
        with vcr.use_cassette('fixtures/engine_create.yaml'):
            engine = 'myengine'
            slug = self.client.create_engine(engine)['body']['slug']
            self.assertEqual(slug, engine)

    def test_engine_destroy(self):
        with vcr.use_cassette('fixtures/engine_destroy.yaml'):
            engine = 'myengine'
            response = self.client.destroy_engine(engine)
            self.assertEqual(response['status'], 204)

    def test_document_types(self):
        with vcr.use_cassette('fixtures/document_types.yaml'):
            self.__is_expected_collection(self.client.document_types, 200, 2, {'slug': 'books'}, self.engine)

    def test_document_type(self):
        with vcr.use_cassette('fixtures/document_type.yaml'):
            self.__is_expected_result(self.client.document_type, 200, {'slug': self.document_type}, self.engine, self.document_type)

    def test_create_document_type(self):
        with vcr.use_cassette('fixtures/create_document_type.yaml'):
            document_type = 'videos'
            slug = self.client.create_document_type(self.engine, document_type)['body']['slug']
            self.assertEqual(slug, document_type)

    def test_destroy_document_type(self):
        with vcr.use_cassette('fixtures/destroy_document_type.yaml'):
            document_type = 'videos'
            response = self.client.destroy_document_type(self.engine, document_type)
            self.assertEqual(response['status'], 204)

    def test_documents(self):
        with vcr.use_cassette('fixtures/documents.yaml'):
            self.__is_expected_collection(self.client.documents, 200, 2, {'external_id': '1'}, self.engine, self.document_type)

    def test_documents_pagination(self):
        with vcr.use_cassette('fixtures/documents_pagination.yaml'):
            self.__is_expected_collection(self.client.documents, 200, 2, {'external_id': '1'}, self.engine, self.document_type, 2, 10)

    def test_document(self):
        with vcr.use_cassette('fixtures/document.yaml'):
            external_id = '1'
            id = self.client.document(self.engine, self.document_type, external_id)['body']['external_id']
            self.assertEqual(id, external_id)

    def test_create_document(self):
        with vcr.use_cassette('fixtures/create_document.yaml'):
            doc_id = 'doc_id'
            id = self.client.create_document(self.engine, self.document_type, {'external_id': doc_id})['body']['external_id']
            self.assertEqual(id, doc_id)

    def test_create_documents(self):
        with vcr.use_cassette('fixtures/create_documents.yaml'):
            docs = [{'external_id': 'doc_id1'}, {'external_id': 'doc_id2'}]
            stati = self.client.create_documents(self.engine, self.document_type, docs)['body']
            self.assertEqual(stati, [True, True])

    def test_create_or_update_document(self):
        with vcr.use_cassette('fixtures/create_or_update_document.yaml'):
            id = '1'
            external_id = self.client.create_or_update_document(self.engine, self.document_type, {'external_id': id, 'fields': {}})['body']['external_id']
            self.assertEqual(external_id, id)

    def test_create_or_update_documents(self):
        with vcr.use_cassette('fixtures/create_or_update_documents.yaml'):
            docs = [{'external_id': '1'}, {'external_id': '2'}]
            stati = self.client.create_or_update_documents(self.engine, self.document_type, docs)['body']
            self.assertEqual(stati, [True, True])

    def test_create_or_update_documents_failure(self):
        with vcr.use_cassette('fixtures/create_or_update_documents_failure.yaml'):
            docs = [{'external_id': '1', 'fields': [{'type': 'string', 'name': 'title'}]}] # <= missing 'value'
            stati = self.client.create_or_update_documents(self.engine, self.document_type, docs)['body']
            self.assertEqual(stati, [False])

    def test_create_or_update_documents_verbose(self):
        with vcr.use_cassette('fixtures/create_or_update_documents_verbose.yaml'):
            docs = [{'external_id': '1'}, {'external_id': '2'}]
            stati = self.client.create_or_update_documents_verbose(self.engine, self.document_type, docs)['body']
            self.assertEqual(stati, [True, True])

    def test_create_or_update_documents_verbose_failure(self):
        with vcr.use_cassette('fixtures/create_or_update_documents_verbose_failure.yaml'):
            docs = [{'external_id': '1', 'fields': [{'type': 'string', 'name': 'title'}]}] # <= missing 'value'
            stati = self.client.create_or_update_documents_verbose(self.engine, self.document_type, docs)['body']
            self.assertRegexpMatches(stati[0], r'^Invalid field definition')

    def test_update_document(self):
        with vcr.use_cassette('fixtures/update_document.yaml'):
            document_id = '2'
            id = self.client.update_document(self.engine, self.document_type, document_id, {'title': 'a new title'})['body']['external_id']
            self.assertEqual(id, document_id)

    def test_update_documents(self):
        with vcr.use_cassette('fixtures/update_documents.yaml'):
            documents = [ {'external_id': '1', 'fields': { 'myfieldthathasnotbeencreated': 'foobar' }},
                          {'external_id': '2', 'fields': { 'title': 'new title' }} ]
            stati = self.client.update_documents(self.engine, self.document_type, documents)['body']
            self.assertEqual(stati, [False, True])

    def test_destroy_document(self):
        with vcr.use_cassette('fixtures/destroy_document.yaml'):
            response = self.client.destroy_document(self.engine, self.document_type, 'doc_id')
            self.assertEqual(response['status'], 204)

    def test_destroy_documents(self):
        with vcr.use_cassette('fixtures/destroy_documents.yaml'):
            documents = ['doc_id1', 'doc_id2']
            stati = self.client.destroy_documents(self.engine, self.document_type, documents)['body']
            self.assertEqual(stati, [True, True])

    def test_search(self):
        with vcr.use_cassette('fixtures/search.yaml'):
            total_count = len(self.client.document_types(self.engine)['body'])
            self.assertTrue(total_count > 1)
            self.__is_expected_search_result(self.client.search, total_count)

    def test_search_with_options(self):
        with vcr.use_cassette('fixtures/search_with_options.yaml'):
            total_count = len(self.client.document_types(self.engine)['body'])
            self.assertTrue(total_count > 1)
            response = self.client.search(self.engine, 'query', {'page': 2})
            self.assertEqual(len(response['body']['records']), total_count)

    def test_search_document_type(self):
        with vcr.use_cassette('fixtures/search_document_type.yaml'):
            self.__is_expected_search_result(self.client.search_document_type, 1, [self.document_type])

    def test_search_document_type_with_options(self):
        with vcr.use_cassette('fixtures/search_document_type_with_options.yaml'):
            response = self.client.search_document_type(self.engine, self.document_type, "query", {'page': 2})
            self.assertEqual(len(response['body']['records']), 1)

    def test_suggest(self):
        with vcr.use_cassette('fixtures/suggest.yaml'):
            total_count = len(self.client.document_types(self.engine)['body'])
            self.assertTrue(total_count > 1)
            self.__is_expected_search_result(self.client.suggest, total_count)

    def test_suggest_with_options(self):
        with vcr.use_cassette('fixtures/suggest_with_options.yaml'):
            total_count = len(self.client.document_types(self.engine)['body'])
            self.assertTrue(total_count > 1)
            response = self.client.suggest(self.engine, 'query', {'page': 2})
            self.assertEqual(len(response['body']['records']), total_count)

    def test_suggest_document_type(self):
        with vcr.use_cassette('fixtures/suggest_document_type.yaml'):
            self.__is_expected_search_result(self.client.suggest_document_type, 1, [self.document_type])

    def test_suggest_document_type_with_options(self):
        with vcr.use_cassette('fixtures/suggest_document_type_with_options.yaml'):
            response = self.client.suggest_document_type(self.engine, self.document_type, "query", {'page': 2})
            self.assertEqual(len(response['body']['records']), 1)

    def test_analytics_searches(self):
        with vcr.use_cassette('fixtures/analytics_searches.yaml'):
            searches = self.client.analytics_searches(self.engine)['body']
            self.assertTrue(len(searches) == 15)

    def test_analytics_searches_pagination(self):
        with vcr.use_cassette('fixtures/analytics_searches_pagination.yaml'):
            searches = self.client.analytics_searches(self.engine, '2013-12-31', '2014-01-01')['body']
            self.assertTrue(len(searches) == 2)

    def test_analytics_autoselects(self):
        with vcr.use_cassette('fixtures/analytics_autoselects.yaml'):
            autoselects = self.client.analytics_autoselects(self.engine)['body']
            self.assertTrue(len(autoselects) == 15)

    def test_analytics_autoselects_pagination(self):
        with vcr.use_cassette('fixtures/analytics_autoselects_pagination.yaml'):
            autoselects = self.client.analytics_autoselects(self.engine, '2013-12-31', '2014-01-01')['body']
            self.assertTrue(len(autoselects) == 2)

    def test_analytics_top_queries(self):
        with vcr.use_cassette('fixtures/analytics_top_queries.yaml'):
            top_queries = self.client.analytics_top_queries(self.engine)['body']
            self.assertTrue(len(top_queries) == 2)

    def test_analytics_top_queries_pagination(self):
        with vcr.use_cassette('fixtures/analytics_top_queries_pagination.yaml'):
            top_queries = self.client.analytics_top_queries(self.engine, 2, 10)['body']
            self.assertTrue(len(top_queries) == 2)

    def test_analytics_top_queries_in_range(self):
        with vcr.use_cassette('fixtures/analytics_top_queries_in_range.yaml'):
            top_queries = self.client.analytics_top_queries_in_range(self.engine, '2013-12-31', '2014-01-01')['body']
            self.assertTrue(len(top_queries) == 2)

    def test_analytics_top_no_result_queries(self):
        with vcr.use_cassette('fixtures/analytics_top_no_result_queries.yaml'):
            autoselects = self.client.analytics_top_no_result_queries(self.engine)['body']
            self.assertTrue(len(autoselects) == 2)

    def test_analytics_top_no_result_queries_with_dates(self):
        with vcr.use_cassette('fixtures/analytics_top_no_result_queries_with_dates.yaml'):
            autoselects = self.client.analytics_top_no_result_queries(self.engine, '2013-12-31', '2014-01-01')['body']
            self.assertTrue(len(autoselects) == 2)

    def test_domains(self):
        with vcr.use_cassette('fixtures/domains.yaml'):
            domains = self.client.domains('crawler-demo')['body']
            self.assertTrue(len(domains) == 2)

    def test_domain(self):
        with vcr.use_cassette('fixtures/domain.yaml'):
            domain_id = '52c759423ae7403ec900003b'
            domain = self.client.domain('crawler-demo', domain_id)['body']
            self.assertEqual(domain['id'], domain_id)

    def test_create_domain(self):
        with vcr.use_cassette('fixtures/create_domain.yaml'):
            url = 'http://www.example.com'
            domain_url = self.client.create_domain('crawler-demo', url)['body']['submitted_url']
            self.assertEqual(domain_url, url)

    def test_destroy_domain(self):
        with vcr.use_cassette('fixtures/destroy_domain.yaml'):
            status = self.client.destroy_domain('crawler-demo', '52c759423ae7403ec900003b')['status']
            self.assertEqual(status, 204)

    def test_recrawl_domain(self):
        with vcr.use_cassette('fixtures/recrawl_domain.yaml'):
            domain_id = '52c754fb3ae7406fd3000001'
            domain = self.client.recrawl_domain('crawler-demo', domain_id)['body']
            self.assertEqual(domain['id'], domain_id)

    def test_crawl_url(self):
        with vcr.use_cassette('fixtures/crawl_domain.yaml'):
            domain_id = '52c754fb3ae7406fd3000001'
            url = 'http://crawler-demo-site.herokuapp.com/2012/01/01/first-post.html'
            crawled_url = self.client.crawl_url('crawler-demo', domain_id, url)['body']['url']
            self.assertEqual(crawled_url, url)

    def __is_expected_search_result(self, request, document_type_count, args=[]):
        response = request(self.engine, *(args + ['*']))
        self.assertEqual(len(response['body']['records']), document_type_count)

    def __is_expected_result(self, request, status_code, expected_values, *args):
        response = request(*args)
        self.assertEqual(response['status'], status_code)
        for k,v in expected_values.items():
            self.assertEqual(response['body'][k], v)

    def __is_expected_collection(self, request, status_code, collection_length, expected_values, *args):
        response = request(*args)
        self.assertEqual(response['status'], status_code)
        self.assertEqual(len(response['body']), collection_length)
        for k,v in expected_values.items():
            self.assertEqual(len([item for item in response['body'] if item[k] == v]), 1)

    def __time_name(self):
        return str(int(time.mktime(time.gmtime())))

    def __create_temporary_engine(self, name = None):
        name = name if name else self.__time_name()
        return


class TestClientUsernameAndPassword(unittest.TestCase):

    def setUp(self):
        self.client = swiftype.Client(
            username='some_user',
            password='some_pasword',
            host='localhost:3000'
        )

    def test_engine_create(self):
        with vcr.use_cassette('fixtures/engine_create.yaml'):
            engine = 'myengine'
            slug = self.client.create_engine(engine)['body']['slug']
            self.assertEqual(slug, engine)


class TestPlatformUsers(unittest.TestCase):

    def setUp(self):
        try:
            api_key = os.environ['API_KEY']
        except:
            api_key = "a-test-api-key"

        client_id = '3e4fd842fc99aecb4dc50e5b88a186c1e206ddd516cdd336da3622c4afd7e2e9'
        client_secret = '4441879b5e2a9c3271f5b1a4bc223b715f091e5ed20fe75d1352e1290c7a6dfb'
        self.client = swiftype.Client(api_key=api_key, client_id=client_id, client_secret=client_secret, host='localhost:3000')

    def test_users(self):
        with vcr.use_cassette('fixtures/users.yaml'):
            response = self.client.users()
            self.assertEqual(response['status'], 200)
            self.assertEqual(len(response['body']), 2)

    def test_users_pagination(self):
        with vcr.use_cassette('fixtures/users_pagination.yaml'):
            response = self.client.users(page=2)
            self.assertEqual(response['status'], 200)
            self.assertEqual(len(response['body']), 0)

    def test_user(self):
        with vcr.use_cassette('fixtures/user.yaml'):
            user_id = '12345'
            response = self.client.user(user_id)
            self.assertEqual(response['body']['id'], user_id)

    def test_create_user(self):
        with vcr.use_cassette('fixtures/create_user.yaml'):
            response = self.client.create_user()
            self.assertEqual(response['status'], 200)

    def test_sso_token(self):
        timestamp = 1379382520
        user_id = '5064a7de2ed960e715000276'
        token = self.client._sso_token(user_id, timestamp)
        self.assertEqual(token, '81033d182ad51f231cc9cda9fb24f2298a411437')

    def test_sso_url(self):
        self.client._get_timestamp = Mock(return_value=1379382520)
        user_id = '5064a7de2ed960e715000276'
        url = self.client.sso_url(user_id)
        self.assertEqual(
            parse_qs(urlparse(url).query),
            {
                'user_id': ['5064a7de2ed960e715000276'],
                'client_id': ['3e4fd842fc99aecb4dc50e5b88a186c1e206ddd516cdd336da3622c4afd7e2e9'],
                'token': ['81033d182ad51f231cc9cda9fb24f2298a411437'],
                'timestamp': ['1379382520'],
            },
        )

class TestPlatformResources(unittest.TestCase):

    def setUp(self):
        access_token = '6cf7fbd297f00a8e3863a0595f55ff7d141cbef2fcbe00159d0f7403649b384e'
        self.engine = 'myusersengine'
        self.document_type = 'videos'
        self.client = swiftype.Client(access_token=access_token, host='localhost:3000')

    def test_platform_engine_create(self):
        with vcr.use_cassette('fixtures/platform_engine_create.yaml'):
            response = self.client.create_engine(self.engine)
            self.assertEqual(response['body']['name'], self.engine)

    def test_platform_create_document_type(self):
        with vcr.use_cassette('fixtures/platform_create_document_type.yaml'):
            response = self.client.create_document_type(self.engine, self.document_type)
            self.assertEqual(response['body']['slug'], self.document_type)

    def test_platform_create_document(self):
        with vcr.use_cassette('fixtures/platform_create_document.yaml'):
            doc_id = 'doc_id'
            id = self.client.create_document(self.engine, self.document_type, {'external_id': doc_id})['body']['external_id']
            self.assertEqual(id, doc_id)

    def test_platform_create_documents(self):
        with vcr.use_cassette('fixtures/platform_create_documents.yaml'):
            docs = [{'external_id': 'doc_id1'}, {'external_id': 'doc_id2'}]
            stati = self.client.create_documents(self.engine, self.document_type, docs)['body']
            self.assertEqual(stati, [True, True])

if __name__ == '__main__':
    unittest.main()
