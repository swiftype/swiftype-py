<p align="center"><img src="https://github.com/swiftype/swiftype-py/blob/master/logo-site-search.png?raw=true" alt="Elastic Site Search Logo"></p>

> **⚠️ This repository is deprecated ⚠️**
>
> **Please visit [https://github.com/elastic/site-search-python](https://github.com/elastic/site-search-python) for the up to date version. Thank you! - Elastic**

<p align="center">
<a href="https://github.com/swiftype/swiftype-py/releases"><img src="https://img.shields.io/github/release/swiftype/swiftype-py/all.svg?style=flat-square" alt="GitHub release" /></a></p>

> A first-party Python client for the [Elastic Site Search API](https://swiftype.com/documentation/site-search/overview).

## Contents

- [Getting started](#getting-started-)
- [Usage](#usage)
- [Running tests](#running-tests)
- [FAQ](#faq-)
- [Contribute](#contribute-)
- [License](#license-)

---

## Getting started 🐣

You can install the latest version of the Swiftype client using `pip`:

    pip install swiftype

To install locally, clone this repository, `cd` into the directory and run:

    python setup.py install

> **Note:** This client has been developed for the [Elastic Site Search](https://www.swiftype.com/site-search) API endpoints only. You may refer to the [Elastic Site Search API Documentation](https://swiftype.com/documentation/site-search/overview) for additional context.

## Usage

1.  Create an account at [Swiftype](https://swiftype.com/) and get your API key from your [Account Settings](https://app.swiftype.com/settings/account).

2.  Configure your client:

        from swiftype import swiftype
        client = swiftype.Client(api_key='YOUR_API_KEY')

3)  Create an `Engine` named e.g. `youtube`:

        engine = client.create_engine('youtube')

4)  Create your `DocumentType`s:

        client.create_document_type('youtube', 'videos');
        client.create_document_type('youtube', 'channels');

### Indexing

Now you need to create your `Document`s. It's very important to think about the type of each field you create a `Document`. The `DocumentType` the `Document` belongs to will remember each fields type and it is not possible to change it. The type specifies a fields features and you should choose them wisely. For details please have a look at our [Field Types Documentation](https://swiftype.com/documentation/overview#field_types).

Add a `Document` to the `videos` `DocumentType`:

    client.create_document('youtube', 'videos', {
    	'external_id':  'external_id1',
    	'fields': [
    		{'name': 'title', 'value': 'Swiftype Demo', 'type': 'string'},
    		{'name': 'tags', 'value': ['Swiftype', 'Search', 'Full text search'], 'type': 'string'},
    		{'name': 'url', 'value': 'http://www.youtube.com/watch?v=pITuOcGgpBs', 'type': 'enum'},
    		{'name': 'category', 'value': ['Tutorial', 'Product'], 'type': 'enum'},
    		{'name': 'publication_date', 'value': '2012-05-08T12:07Z', 'type': 'date'},
    		{'name': 'likes', 'value': 31, 'type': 'integer'},
    		{'name': 'length', 'value': 1.50, 'type': 'float'}
    	]})

Add a `Document` to the `channels` `DocumentType`:

    client.create_document('youtube', 'channels', {
    	'external_id': 'external_id1',
    	'fields': [
    		{'name': 'title', 'value': 'Swiftype', 'type': 'string'},
    		{'name': 'url', 'value': 'http://www.youtube.com/user/swiftype', 'type': 'enum'},
    		{'name': 'video_views', 'value': 15678, 'type': 'integer'},
    		{'name': 'video_counts', 'value': 6, 'type': 'integer'}
    	]})

### Searching

Now your `Engine` is ready to receive queries. By default, search queries will match any fields that are of type `string` or `text`. You can search each `DocumentType` individually:

    video_results = client.search_document_type('youtube', 'videos', 'swiftype')
    channel_results = client.search_document_type('youtube', 'channels', 'swiftype')

or search all `DocumentType`s on your `Engine` at once:

    results = client.search('youtube', 'swiftype')

### Autocomplete

Finally, as with full-text searches, you may perform autocomplete-style (prefix match) searches as well:

    results = client.suggest('youtube', 'swi')

or

    results = client.suggest_document_type('youtube', 'videos', 'swi')

## API Documentation

### Configuration:

Before issuing commands to the API, configure the client with your API key:

    import swiftype
    client = swiftype.Client(api_key='YOUR_API_KEY')

You can find your API key in your [Account Settings](https://swiftype.com/user/edit).

### Search

If you want to search for e.g. `swiftype` on your `Engine`, you can use:

    results = client.search('youtube', 'swiftype')

To limit the search to only the `videos` DocumentType:

    results = client.search_document_type('youtube', 'videos', 'swiftype')

Both search methods allow you to specify options as an extra parameter to e.g. filter or sort on fields. For more details on these options please have a look at the [Search Options](https://swiftype.com/documentation/searching). Here is an example for showing only `videos` that are in the `category` `Tutorial`:

    results = client.search_document_type('youtube', 'videos', 'swiftype', {'filters': {'videos': {'category': 'Tutorial'}}})

### Autocomplete

Autocompletes have the same functionality as searches. You can autocomplete using all documents:

    results = client.suggest('youtube', 'swi')

or just for one DocumentType:

    results = client.suggest_document_type('youtube', 'videos', 'swi')

or add options to have more control over the results:

    results = client.suggest('youtube', 'swi', {'sort_field': {'videos': 'likes'}})

### Engines

Retrieve every `Engine`:

    engines = client.engines

Create a new `Engine` with the name `youtube`:

    engine = client.create_engine('youtube')

Retrieve an `Engine` by `slug` or `id`:

    engine = client.engine('youtube')

To delete an `Engine` you need the `slug` or the `id` field of an `engine`:

    client.destroy_engine('youtube')

### Document Types

Retrieve `DocumentTypes`s of the `Engine` with the `slug` field `youtube`:

    document_types = client.document_types('youtube')

Show the second batch of documents:

    document_types = client.document_types('youtube', 2)

Create a new `DocumentType` for an `Engine` with the name `videos`:

    document_type = client.create_document_type('youtube', 'videos')

Retrieve an `DocumentType` by `slug` or `id`:

    document_type = client.document_type('youtube', 'videos')

Delete a `DocumentType` using the `slug` or `id` of it:

    client.destroy_document_type('youtube', 'videos')

### Documents

Retrieve all `Document`s of `Engine` `youtube` and `DocumentType` `videos`:

    documents = client.documents('youtube', 'videos')

Retrieve a specific `Document` using its `id` or `external_id`:

    document = client.document('youtube', 'videos', 'external_id1')

Create a new `Document` with mandatory `external_id` and user-defined fields:

    document = client.create_document('youtube', 'videos', {
    	'external_id': 'external_id1',
    		'fields': [
    			{'name': 'title', 'value': 'Swiftype Demo', 'type': 'string'},
    			{'name': 'tags', 'value': ['Swiftype', 'Search', 'Full text search'], 'type': 'string'},
    			{'name': 'url', 'value': 'http://www.youtube.com/watch?v=pITuOcGgpBs', 'type': 'enum'},
    			{'name': 'category', 'value': ['Tutorial', 'Product'], 'type': 'enum'},
    			{'name': 'publication_date', 'value': '2012-05-08T12:07Z', 'type': 'date'},
    			{'name': 'likes', 'value': 31, 'type': 'integer'},
    			{'name': 'length', 'value': 1.50, 'type': 'float'}
    		]})

Create multiple `Document`s at once and return status for each `Document` creation:

    stati = client.create_documents('youtube', 'videos', {
    	'external_id': 'external_id1',
    		'fields': [
    			{'name': 'title', 'value': 'Swiftype Demo', 'type': 'string'},
    			{'name': 'tags', 'value': ['Swiftype', 'Search', 'Full text search'], 'type': 'string'},
    			{'name': 'url', 'value': 'http://www.youtube.com/watch?v=pITuOcGgpBs', 'type': 'enum'},
    			{'name': 'category', 'value': ['Tutorial', 'Product'], 'type': 'enum'},
    			{'name': 'publication_date', 'value': '2012-05-08T12:07Z', 'type': 'date'},
    			{'name': 'likes', 'value': 27, 'type': 'integer'},
    			{'name': 'length', 'value': 1.50, 'type': 'float'}
    		]},	{
    	'external_id': 'external_id2',
    		'fields': [
    			{'name': 'title', 'value': 'Swiftype Search Wordpress Plugin Demo', 'type': 'string'},
    			{'name': 'tags', 'value': ['Swiftype', 'Search', 'Full text search', 'WordPress'], 'type': 'string'},
    			{'name': 'url', 'value': 'http://www.youtube.com/watch?v=rukXYKEpvS4', 'type': 'enum'},
    			{'name': 'category', 'value': ['Tutorial', 'Wordpress'], 'type': 'enum'},
    			{'name': 'publication_date', 'value': '2012-08-15T09:07Z', 'type': 'date'},
    			{'name': 'likes', 'value': 2, 'type': 'integer'},
    			{'name': 'length', 'value': 2.16, 'type': 'float'}
    		]})

Update fields of an existing `Document` specified by `id` or `external_id`:

    client.update_document('youtube','videos','external_id1', {'likes': 28, 'category': ['Tutorial', 'Search']})

Update multiple `Document`s at once:

    stati = client.update_documents('youtube', 'videos', [
    	{'external_id': '2', 'fields': {'likes': 29}},
    	{'external_id': '3', 'fields': {'likes': 4}}
    ])

Create or update a `Document`:

    document = client.create_or_update_document('youtube', 'videos', {
    	'external_id': 'external_id3',
    		'fields': [
    		{'name': 'title', 'value': 'Swiftype Install Type 1: Show results in an overlay', 'type': 'string'},
    		{'name': 'tags', 'value': ['Swiftype', 'Search', 'Full text search', 'Web'], 'type': 'string'},
    		{'name': 'url', 'value': 'http://www.youtube.com/watch?v=mj2ApIx3frs', 'type': 'enum'}
    	]})

Create or update multiple `Documents` at once:

    stati = client.create_or_update_documents('youtube', 'videos', {
    	'external_id': 'external_id4',
    		'fields': [
    			{'name': 'title', 'value': 'Swiftype Install Type 2: Show results on the current page', 'type': 'string'},
    			{'name': 'tags', 'value': ['Swiftype', 'Search', 'Full text search', 'Web'], 'type': 'string'},
    			{'name': 'url', 'value': 'http://www.youtube.com/watch?v=6uaZXYK2WOE', 'type': 'enum'}
    		]}, {
    	'external_id': 'external_id5',
    		'fields': [
    			{'name': 'title', 'value': 'Swiftype Install Type 3: Show results on a new page', 'type': 'string'},
    			{'name': 'tags', 'value': ['Swiftype', 'Search', 'Full text search', 'Web'], 'type': 'string'},
    			{'name': 'url', 'value': 'http://www.youtube.com/watch?v=ebSWAscBPtc', 'type': 'enum'}
    		]});

Destroy a `Document`:

    client.destroy_document('youtube','videos','external_id5')

Destroy multiple `Document`s at once:

    stati = client.destroy_documents('youtube','videos',['external_id2','external_id3','external_id6'])

### Domains

Retrieve all `Domain`s of `Engine` `websites`:

    domains = client.domains('websites')

Retrieve a specific `Domain` by `id`:

    domain = client.domain('websites', 'generated_id')

Create a new `Domain` with the URL `https://swiftype.com` and start crawling:

    domain = client.create_domain('websites', 'https://swiftype.com')

Delete a `Domain` using its `id`:

    client.destroy_domain('websites', 'generated_id')

Initiate a recrawl of a specific `Domain` using its `id`:

    client.recrawl_domain('websites', 'generated_id')

Add or update a URL for a `Domain`:

    client.crawl_url('websites', 'generated_id', 'https://swiftype.com/new/path/about.html')

### Analytics

To get the amount of searches on your `Engine` in the last 14 days use:

    searches = client.analytics_searches('youtube')

You can also use a specific start and/or end date:

    searches = client.analytics_searches('youtube', '2013-01-01', '2013-02-01')

To get the amount of autoselects (clicks on autocomplete results) use:

    autoselects = client.analytics_autoselects('youtube')

As with searches you can also limit by start and/or end date:

    autoselects = client.analytics_autoselects('youtube', 2, 10)

If you are interested in the top queries for your `Engine` you can use:

    top_queries = client.analytics_top_queries('youtube')

To see more top queries you can paginate through them using:

    top_queries = client.analytics_top_queries('youtube', page=2)

Or you can get the top queries in a specific date range:

    top_queries = client.analytics_top_queries_in_range('youtube', '2013-01-01', '2013-02-01')

If you want to improve you search results, you should always have a look at search queries, that return no results and perhaps add some Documents that match for this query or use our pining feature to add Documents for this query:

    top_no_result_queries = client.analytics_top_no_result_queries('youtube')

You can also specify a date range for no result queries:

    top_no_result_queries = client.analytics_top_no_result_queries('youtube', '2013-01-01', '2013-02-01')

## Running Tests

    pip install -r test_requirements.txt
    python tests/test_swiftype.py

## FAQ 🔮

### Where do I report issues with the client?

If something is not working as expected, please open an [issue](https://github.com/swiftype/swiftype-py/issues/new).

### Where can I learn more about Site Search?

Your best bet is to read the [documentation](https://swiftype.com/documentation/site-search).

### Where else can I go to get help?

You can checkout the [Elastic Site Search community discuss forums](https://discuss.elastic.co/c/site-search).

## Contribute 🚀

We welcome contributors to the project. Before you begin, a couple notes...

- Before opening a pull request, please create an issue to [discuss the scope of your proposal](https://github.com/swiftype/swiftype-py/issues).
- Please write simple code and concise documentation, when appropriate.

## License 📗

[MIT](https://github.com/swiftype/swiftype-py/blob/master/LICENSE) © [Elastic](https://github.com/elastic)

Thank you to all the [contributors](https://github.com/swiftype/swiftype-py/graphs/contributors)!
