from django.test import Client, TestCase
from json import loads
from unittest import skipIf
from urlparse import urlparse

import multiprocessing
import json
import os

# discovery provides some module path settings that are needed to import other
# modules.
import discovery

from mediawiki101 import wikifyNamespace


# Descriptions to all possible error types
# These are output as is after each exception listing, so they may contain html
# code. Newline are repalce with <br>-Tags automatically
error_descriptions = {
    'ResourceAlreadyAssignedError':
        "This errors occurs if a link to an entity is found, and the link was "
        "already found for an entity higher up in the hierarchy.\n\n"
        "For Example: The top-level Root-Entity has the URL <code>/</code>, if "
        "further down a link to another entity is found, with exactly that"
        " url, it is assumed that the link generation is faulty, instead of "
        "that one url points to two different entities.",
    'ResponseStatusNotOkError':
        "This error occurs if a http response is not served with message "
        "<code>200 Ok</code>.",
    'WrongClassifierError':
        "This error occurs if the link to an entity specifies another expected "
        "classifier than the entity itself reports.",
    'WrongNameError':
        "This error occurs if the link to an entity specifies another expected "
        "name than the entity itself reports.",
    'ResourceNotFoundException':
        "This error occurs if the explorer script somehow deems an url "
        "invalid, and throws this exception by hand to trigger a "
        "<code>404 not found</code>.\n\n"
        "This is fine behaviour for nonsensical URLs. But no page in the "
        "explorer should produce a link to page that contains this exception.",
    'ValidationError':
        "This error is thrown by the explorer intern page validation code, "
        "that validates each entities output against a schema."
}


class Entity:
    def __init__(self, resource, classifier, name):
        self.resource = self.get_resource_url(resource)
        self.classifier = classifier
        self.name = name

    def __str__(self):
        return "Entity: (resource: {}, classifier: {}, name: {})".format(
            self.resource, self.classifier, self.name)

    @staticmethod
    def get_resource_url(resource):
        url = urlparse(resource)
        resource = url.path
        if resource[-1] == '/':
            resource = resource[:-1]
        return resource


class Result:
    def __init__(self):
        self.error_dict = {}
        self.number_dict = {}
        self.total_count = 0

    # Result convert to True if it contains atleast one error
    # Requires crunch_numbers to be run already
    def __bool__(self):
        return self.total_count
    __nonzero__ = __bool__

    def add_result(self, msg):
        entity, error_msg, error_type = msg
        if error_type not in self.error_dict:
            self.error_dict[error_type] = []
        self.error_dict[error_type].append({
            'entity': entity,
            'error': error_msg,
        })

    def crunch_numbers(self):
        for error_type in self.error_dict:
            count = len(self.error_dict[error_type])
            self.number_dict[error_type] = count
            self.total_count += count


class Checker:
    def __init__(self):
        self.root_entities = [Entity("/discovery", "Namespace", "Namespace")]
        self.namespace_entities = []
        self.member_entities = []
        self.folder_entities = []
        self.file_entities = []
        self.fragment_entities = []

        self.root_results = Result()
        self.namespace_results = Result()
        self.member_results = Result()
        self.folder_results = Result()
        self.file_results = Result()
        self.fragment_results = Result()

        self.number_of_processes_default = 1
        try:
            self.number_of_processes = multiprocessing.cpu_count()
        except NotImplementedError:
            self.number_of_processes = self.number_of_processes_default
        self.pool = multiprocessing.Pool(processes=self.number_of_processes)

    def check_all_entities(self):
        self.check_root_entities()
        self.check_namespace_entities()
        self.check_member_entities()
        self.check_folder_entities()
        self.check_file_entities()
        self.check_fragment_entities()

        results = {
            'root_errors': self.root_results,
            'namespace_errors': self.namespace_results,
            'member_errors': self.member_results,
            'folder_errors': self.folder_results,
            'file_errors': self.file_results,
            'fragment_errors': self.fragment_results
        }
        return results

    def check_root_entities(self):
        rep_errs = self.check_entity_parallel(self.root_entities)
        self.process_result(rep_errs, self.root_results,
                            self.namespace_entities, 'members')

    def check_namespace_entities(self):
        rep_errs = self.check_entity_parallel(self.namespace_entities)
        self.process_result(rep_errs, self.namespace_results,
                            self.member_entities, 'members')

    def check_member_entities(self):
        rep_errs = self.check_entity_parallel(self.member_entities)
        self.process_result_two(rep_errs, self.member_results,
                                self.folder_entities, 'folders',
                                self.file_entities, 'files')

    def check_folder_entities(self):
        while True:
            rep_errs = self.check_entity_parallel(self.folder_entities)
            self.folder_entities = []
            self.process_result_two(rep_errs, self.folder_results,
                                    self.file_entities, 'files',
                                    self.folder_entities, 'folders')
            # Loops until no new "level" of folders is found.
            # Since backreferences are caught as ResourceAlreadyAssignedErrors
            # and thus not added to folder_entitites, this will always
            # terminate.
            if not self.folder_entities:
                break

    def check_file_entities(self):
        rep_errs = self.check_entity_parallel(self.file_entities)
        self.process_result(rep_errs, self.file_results,
                            self.fragment_entities, 'fragments')

    def check_fragment_entities(self):
        while True:
            rep_errs = self.check_entity_parallel(self.fragment_entities)
            self.fragment_entities = []
            self.process_result(rep_errs, self.fragment_results,
                                self.fragment_entities, 'fragments')
            if not self.fragment_entities:
                break

    # Spawns workers to process source with check_entity and
    # returns the collected results.
    def check_entity_parallel(self, source):
        results = [self.pool.apply_async(check_entity, (entity,))
                   for entity in source]
        rep_errs = [result.get() for result in results]
        return rep_errs

    @staticmethod
    def process_result(rep_errs, results,
                       child, child_field):
        for (entity, response, (error_type, error_msg)) in rep_errs:
            if error_type:
                results.add_result((entity, error_msg, error_type))
            elif response:
                for child_entity in response[child_field]:
                    child.append(Entity(child_entity['resource'],
                                        child_entity['classifier'],
                                        child_entity['name']))

    @staticmethod
    def process_result_two(rep_errs, results,
                           child1, child1_field,
                           child2, child2_field):
        for (entity, response, (error_type, error_msg)) in rep_errs:
            if error_type:
                results.add_result((entity, error_msg, error_type))
            elif response:
                for child_entity in response[child1_field]:
                    child1.append(Entity(child_entity['resource'],
                                         child_entity['classifier'],
                                         child_entity['name']))
                for child_entity in response[child2_field]:
                    child2.append(Entity(child_entity['resource'],
                                         child_entity['classifier'],
                                         child_entity['name']))


assigned_resources = multiprocessing.Manager().list()
assigned_resources_mutex = multiprocessing.Lock()
# is the mutex really necessary since assigned_resources already is
# a multiprocessing list?

# for url querying
client = Client()


# Ideally this function would be a method of class Checker. But this is
# impossible because multiprocessing can't pickle methods.
def check_entity(entity):
    already_assigned = False
    # MUTEX
    assigned_resources_mutex.acquire()
    try:
        if entity.resource in assigned_resources:
            already_assigned = True
        else:
            assigned_resources.append(entity.resource)
    finally:
        assigned_resources_mutex.release()
    # MUTEX
    if already_assigned:
        return entity, None, ("ResourceAlreadyAssignedError",
                              "resource url was already assigned to "
                              "another entity")

    try:
        # For some reason this call still produces Tracebacks if we catch
        # the exception further down, how to supress these?
        response = client.get(entity.resource,
                              {'format': 'json',
                               'validate': 'true'})

    except Exception as e:
        return entity, None, (type(e).__name__, str(e))

    if response.status_code != 200:
        return entity, None, ("ResponseStatusNotOkError",
                              "Did not return status ok (200) but instead ("
                              + str(response.status_code) + ")")

    parsed_response = loads(response.content)
    parsed_classifier = parsed_response['classifier']
    parsed_name = parsed_response['name']
    wikified_name = wikifyNamespace(parsed_name)

    if wikified_name and wikified_name != 'None':
        parsed_name = wikified_name

    if entity.classifier != parsed_classifier:
        return entity, None, ("WrongClassifierError",
                              "Did not have expected classifier '{} but "
                              "instead '{}'".format(
                                  entity.classifier,
                                  parsed_classifier))
    if entity.name != parsed_name:
        return entity, None, ("WrongNameError",
                              "Did not have expected name '{}' but "
                              "instead '{}'".format(entity.name,
                                                    parsed_name))
    return None, parsed_response, (None, None)


@skipIf("TEST_ALL_EXPLORER_ENTITIES" not in os.environ,
        "This module is run from the 101worker module testAllExplorerEntities.")
class AllEntitiesTest(TestCase):
    results = None

    @classmethod
    def setUpClass(cls):
        checker = Checker()
        cls.results = checker.check_all_entities()

        log = {
            'total_count': 0,
            'error_descriptions': error_descriptions
        }

        def add_result(result_name):
            result = cls.results[result_name]
            result.crunch_numbers()
            log[result_name] = {
                'total_count': result.total_count,
                'error_counts': result.number_dict,
                'error_list': result.error_dict,
            }
            log['total_count'] += result.total_count

        add_result('root_errors')
        add_result('namespace_errors')
        add_result('member_errors')
        add_result('folder_errors')
        add_result('file_errors')
        add_result('fragment_errors')

        outpath = os.path.join(os.environ['worker101dir'],
                               'modules', 'testAllExplorerEntities',
                               'results.json')
        with open(outpath, 'w') as outfile:
            json.dump(log, outfile, cls=LogEncoder, sort_keys=True, indent=4)

    @classmethod
    def tearDownClass(cls):
        pass

    # the following methods just signal to a human test executor where
    # errors happened

    def test_root(self):
        if AllEntitiesTest.results['root_errors']:
            self.fail()

    def test_namespaces(self):
        if AllEntitiesTest.results['namespace_errors']:
            self.fail()

    def test_members(self):
        if AllEntitiesTest.results['member_errors']:
            self.fail()

    def test_folders(self):
        if AllEntitiesTest.results['folder_errors']:
            self.fail()

    def test_files(self):
        if AllEntitiesTest.results['file_errors']:
            self.fail()

    def test_fragments(self):
        if AllEntitiesTest.results['fragment_errors']:
            self.fail()


# Custom JSON encoder
class LogEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Entity):
            return obj.__dict__
        if isinstance(obj, Exception):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
