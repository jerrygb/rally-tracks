import random
import os
import json

def put_settings(es, params):
    es.cluster.put_settings(body=params["body"])


def register(registry):
    # register a fallback for older Rally versions

    registry.register_param_source("filtered-terms-query-source", FilteredTermsQueryParamSource)
    registry.register_param_source("filtered-terms-phrase-query-source", FilteredTermsPhraseQueryParamSource)
    registry.register_param_source("filtered-terms-phrase-query-analyze-source", FilteredTermsPhraseQueryAnalyzeParamSource)
    try:
        from esrally.driver.runner import PutSettings
    except ImportError:
        registry.register_runner("put-settings", put_settings)


class QueryParamSource:
    # We need to stick to the param source API
    # noinspection PyUnusedLocal
    def __init__(self, track, params, **kwargs):
        self._params = params
        self.infinite = True
        cwd = os.path.dirname(__file__)
        # The terms.txt file has been generated with:
        # sed -n '13~250p' [path_to_rally_data]/geonames/documents.json | shuf | sed -e "s/.*name\": \"//;s/\",.*$//" > terms.txt
        with open(os.path.join(cwd, "pmid_list.txt"), "r") as ins:
            self.terms = [line.strip() for line in ins.readlines()]

    # We need to stick to the param source API
    # noinspection PyUnusedLocal
    def partition(self, partition_index, total_partitions):
        return self


class FilteredTermsQueryParamSource(QueryParamSource):
    def params(self):
        start_index = random.randint(1, 98999)
        query_terms = list(self.terms[start_index:start_index + 999])  # copy
        query_terms.append(str(random.randint(1, 1000)))  # avoid caching
        result = {
            "body": {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "body": self._params["search-term"]
                                }
                            }
                        ],
                        "filter": [
                            {
                                "terms": {
                                    "pmid": query_terms
                                }
                            }
                        ]
                    }
                }
            },
            "index": None
        }
        result_to_write = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "body": self._params["search-term"]
                            }
                        }
                    ],
                    "filter": [
                        {
                            "terms": {
                                "pmid": query_terms
                            }
                        }
                    ]
                }
            }
        }
        if "verbose" in self._params:
            print("Testing with ", len(query_terms), "terms")
            print(result)

            with open('/root/1/' + str(random.randint(1, 1000)) + '.json', 'w') as f:
                f.write(json.dumps(result_to_write, indent=4))
        if "cache" in self._params:
            result["cache"] = self._params["cache"]

        return result

class FilteredTermsPhraseQueryParamSource(QueryParamSource):
    def params(self):
        start_index = random.randint(1, 98999)
        query_terms = list(self.terms[start_index:start_index + 999])  # copy
        query_terms.append(str(random.randint(1, 1000)))  # avoid caching
        result = {
            "body": {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match_phrase": {
                                    "body": self._params["search-phrase"]
                                }
                            }
                        ],
                        "filter": [
                            {
                                "terms": {
                                    "pmid": query_terms
                                }
                            }
                        ]
                    }
                }
            },
            "index": None
        }
        result_to_write = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_phrase": {
                                "body": self._params["search-phrase"]
                            }
                        }
                    ],
                    "filter": [
                        {
                            "terms": {
                                "pmid": query_terms
                            }
                        }
                    ]
                }
            }
        }
        if "verbose" in self._params:
            print("Testing with ", len(query_terms), "terms")
            print(result)

            with open('/root/1/' + str(random.randint(1, 1000)) + '.json', 'w') as f:
                f.write(json.dumps(result_to_write, indent=4))
        if "cache" in self._params:
            result["cache"] = self._params["cache"]

        return result


class FilteredTermsPhraseQueryAnalyzeParamSource(QueryParamSource):
    def params(self):
        start_index = random.randint(1, 98999)
        query_terms = list(self.terms[start_index:start_index + 999])  # copy
        query_terms.append(str(random.randint(1, 1000)))  # avoid caching
        result = {
            "body": {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match_phrase": {
                                    "body": {
                                        "query": self._params["search-phrase"],
                                        "analyzer": "rebuilt_english"
                                    }
                                }
                            }
                        ],
                        "filter": [
                            {
                                "terms": {
                                    "pmid": query_terms
                                }
                            }
                        ]
                    }
                }
            },
            "index": None
        }
        result_to_write = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_phrase": {
                                "body": {
                                    "query": self._params["search-phrase"],
                                    "analyzer": "rebuilt_english"
                                }
                            }
                        }
                    ],
                    "filter": [
                        {
                            "terms": {
                                "pmid": query_terms
                            }
                        }
                    ]
                }
            }
        }
        if "verbose" in self._params:
            print("Testing with ", len(query_terms), "terms")
            with open('/root/2/' + str(random.randint(1, 1000)) + '.json', 'w') as f:
                f.write(json.dumps(result_to_write, indent=4))

        if "cache" in self._params:
            result["cache"] = self._params["cache"]

        return result