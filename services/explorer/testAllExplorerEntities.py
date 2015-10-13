from django.test import Client, TestCase
from unittest import skipIf
from urlparse import urlparse

import collections
import multiprocessing
import json
import Queue
import sys
import time
import uuid
import os

# discovery provides some module path settings that are needed to import other
# modules.
import discovery

from mediawiki101 import wikifyNamespace

module_dir = os.path.join(os.environ['worker101dir'],
                          'modules', 'testAllExplorerEntities')
# Have to do some PATH manipulation to load config because it's in the module
# directory and not in the test directory. http://stackoverflow.com/a/4383597
sys.path.insert(0, module_dir)
import config


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


class EntityJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Entity):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class EntityAnalyzer:
    default_number_of_processes = 1
    main_process_sleep_time = 1
    worker_process_sleep_time = 1
    unchecked_entities_file = os.path.join(os.environ['worker101dir'],
                                           'modules', 'testAllExplorerEntities',
                                           'unchecked_entities.json')
    entity_errors_file = os.path.join(os.environ['worker101dir'],
                                      'modules', 'testAllExplorerEntities',
                                      'entity_errors.json')
    assigned_resources_file = os.path.join(os.environ['worker101dir'],
                                           'modules', 'testAllExplorerEntities',
                                           'assigned_resources.json')
    classifier_child_fields = collections.defaultdict(
        lambda: ["fragments"],  # unknown classifiers are treated as fragments
        {
            "Namespace": ["members"],
            "Namespace member": ["folders", "files"],
            "Folder": ["folders", "files"],
            "File": ["fragments"],
            "Fragment": ["fragments"],
        }
    )

    def __init__(self, time_to_run=0, max_out_degree=0):
        """
        :param time_to_run:
            A float giving the time in seconds that should be spent to
            incrementally search for errors. If zero or not present, will
            perform a full search for errors regardless of time taken.
        :param max_out_degree:
            An int giving the number of childs per entity that are added to the
            recursion. If zero or not present, will add all childs.
        """
        self.time_to_run = time_to_run
        self.max_out_degree = max_out_degree

        self.assigned_resources = multiprocessing.Manager().list()
        self.assigned_resources_mutex = multiprocessing.Lock()

        self.unchecked_entities = []
        self.checked_entities = []

        # queue keeping track of entities to analyze
        self.unchecked_entities_queue = multiprocessing.JoinableQueue()
        if not self.time_to_run:
            # Don't use any previous results, get everything from scratch.
            self.entity_errors = {}
            self.unchecked_entities_queue.put(
                Entity("/discovery", "Namespace", "Namespace"))
        else:
            # Continue from previous invocations.
            self.read_entity_errors()
            self.read_unchecked_entities()
            if self.unchecked_entities:
                for entity in self.unchecked_entities:
                    self.unchecked_entities_queue.put(entity)
                self.unchecked_entities = []
                self.read_assigned_resources()
            else:
                self.unchecked_entities_queue.put(
                    Entity("/discovery", "Namespace", "Namespace"))

        self.checked_entities_queue = multiprocessing.Queue()

        # event that is set to true once time_to_run is over
        self.should_stop = multiprocessing.Event()

        try:
            number_of_processes = multiprocessing.cpu_count()
        except NotImplementedError:
            number_of_processes = EntityAnalyzer.default_number_of_processes
        self.processes = [multiprocessing.Process(
                              target=EntityAnalyzer.entity_analyzer_worker,
                              args=(self.unchecked_entities_queue,
                                    self.checked_entities_queue,
                                    self.should_stop,
                                    self.assigned_resources,
                                    self.assigned_resources_mutex,
                                    self.max_out_degree))
                          for _ in range(number_of_processes)]

    def read_unchecked_entities(self):
        """
        Reads self.unchecked_entities from file.
        """
        if not os.path.isfile(EntityAnalyzer.unchecked_entities_file):
            self.unchecked_entities = []
        else:
            with open(EntityAnalyzer.unchecked_entities_file, 'r') as infile:
                raw_unchecked_entities = json.load(infile)
                self.unchecked_entities =\
                    [Entity(e["resource"], e["classifier"], e["name"])
                     for e in raw_unchecked_entities]

    def write_unchecked_entities(self):
        """
        Writes self.uncheck_entities to file.
        """
        with open(EntityAnalyzer.unchecked_entities_file, 'w') as outfile:
            json.dump(self.unchecked_entities, outfile, cls=EntityJsonEncoder,
                      indent=4)

    def read_entity_errors(self):
        """
        Reads self.entity_errors from file.
        """
        if not os.path.isfile(EntityAnalyzer.entity_errors_file):
            self.entity_errors = {}
        else:
            with open(EntityAnalyzer.entity_errors_file, 'r') as infile:
                self.entity_errors = json.load(infile)

    def write_entity_errors(self):
        """
        Writes self.entity_errors to file.
        """
        with open(EntityAnalyzer.entity_errors_file, 'w') as outfile:
            json.dump(self.entity_errors, outfile, indent=4)

    def update_entity_errors(self):
        """
        Uses self.checked_entities to update self.entity_errors.
        """
        for entity, time_taken, error in self.checked_entities:
            if error:
                error_type, error_msg = error
                self.entity_errors[entity.resource] = {
                    "classifier": entity.classifier,
                    "name": entity.name,
                    "time_taken": time_taken,
                    "error": {
                        "type": error_type,
                        "msg": error_msg,
                    },
                }
            else:
                self.entity_errors.pop(entity.resource, None)

    def read_assigned_resources(self):
        """
        Reads self.assigned_resources from file.
        """
        if os.path.isfile(EntityAnalyzer.assigned_resources_file):
            with open(EntityAnalyzer.assigned_resources_file, 'r') as infile:
                raw_assigned_resources = json.load(infile)
                for assigned_resource in raw_assigned_resources:
                    self.assigned_resources.append(assigned_resource)

    def write_assigned_resources(self):
        """
        Writes self.assigned_resources to file.
        """
        with open(EntityAnalyzer.assigned_resources_file, 'w') as outfile:
            json.dump(self.assigned_resources._getvalue(), outfile, indent=4)

    def run(self):
        for process in self.processes:
            process.start()

        if not self.time_to_run:
            self.unchecked_entities_queue.join()
        else:
            time_to_stop = time.time() + self.time_to_run
            while time.time() < time_to_stop:
                time.sleep(EntityAnalyzer.main_process_sleep_time)

        self.should_stop.set()

        # queues needs to be emptied in order to join processes.
        self.deplete_queues()

        for process in self.processes:
            process.join()

        self.write_unchecked_entities()
        self.update_entity_errors()
        self.write_entity_errors()
        self.write_assigned_resources()

        return self.entity_errors

    def deplete_queues(self):
        self.unchecked_entities = []
        try:
            while True:
                unchecked_entity = self.unchecked_entities_queue.get(block=True,
                    timeout=EntityAnalyzer.worker_process_sleep_time)
                self.unchecked_entities.append(unchecked_entity)
                self.unchecked_entities_queue.task_done()
        except Queue.Empty:
            pass

        self.checked_entities = []
        try:
            while True:
                checked_entity, time_taken, error =\
                    self.checked_entities_queue.get(block=True,
                        timeout=EntityAnalyzer.worker_process_sleep_time)
                self.checked_entities.append((checked_entity, time_taken, error))
        except Queue.Empty:
            pass

    @staticmethod  # Method static because else multiprocessing can't pickle it.
    def entity_analyzer_worker(unchecked_entities_queue,
                               checked_entities_queue,
                               should_stop,
                               assigned_resources,
                               assigned_resources_mutex,
                               max_out_degree):
        client = Client()

        def query_and_analyze_entity(entity):
            assigned_resources_mutex.acquire()  # MUTEX ACQUIRE
            try:
                if entity.resource in assigned_resources:
                    # URLs need to be unique for self.entity_errors
                    entity.resource += " (duplicate-" + str(uuid.uuid1()) + ")"
                    return entity, None, -1,\
                           ("ResourceAlreadyAssignedError",
                            "Resource url was already assigned to another "
                            "entity.")
                else:
                    assigned_resources.append(entity.resource)
            finally:
                assigned_resources_mutex.release()  # MUTEX RELEASE

            time_before = time.time()
            try:
                # For some reason this call still produces a traceback if we
                # catch the exception further down, how to suppress these?
                # Seems like Django logging. Do we want to disable that for the
                # test? How?
                response = client.get(entity.resource,
                                      {'format': 'json', 'validate': 'true'})
            except Exception as e:
                time_taken = time.time() - time_before
                return entity, None, time_taken,\
                       (type(e).__name__, str(e))

            time_taken = time.time() - time_before

            if response.status_code != 200:
                return entity, None, time_taken,\
                       ("ResponseStatusNotOkError",
                        "Did not return status ok (200) but instead '{}'."
                        .format(response.status_code))

            parsed_response = json.loads(response.content)
            parsed_classifier = parsed_response['classifier']
            parsed_name = parsed_response['name']
            wikified_name = wikifyNamespace(parsed_name)
            if wikified_name and wikified_name != 'None':
                parsed_name = wikified_name

            if entity.classifier != parsed_classifier:
                return entity, None, time_taken,\
                       ("WrongClassifierError",
                        "Did not have expected classifier '{} but instead '{}'."
                        .format(entity.classifier, parsed_classifier))
            if entity.name != parsed_name:
                return entity, None, time_taken,\
                       ("WrongNameError",
                        "Did not have expected name '{}' but instead '{}'."
                        .format(entity.name, parsed_name))
            return entity, parsed_response, time_taken, None

        while not should_stop.is_set():
            try:
                entity_to_check = unchecked_entities_queue.get(
                    block=True,
                    timeout=EntityAnalyzer.worker_process_sleep_time)
            except Queue.Empty:
                continue

            entity, response, time_taken, error =\
                query_and_analyze_entity(entity_to_check)

            checked_entities_queue.put((entity, time_taken, error))
            if not error:
                for child_field in \
                        EntityAnalyzer.classifier_child_fields[
                            entity.classifier]:
                    for counter, child_entity in enumerate(
                            response[child_field]):
                        if counter == max_out_degree and max_out_degree != 0:
                            break
                        unchecked_entities_queue.put(
                            Entity(child_entity['resource'],
                                   child_entity['classifier'],
                                   child_entity['name']))

            unchecked_entities_queue.task_done()


class ReportBuilder:
    report_file = os.path.join(os.environ['worker101dir'],
                               'modules', 'testAllExplorerEntities',
                               'report.json')
    classifier_report_fields = collections.defaultdict(
        # unknown classifiers are treated as fragments
        lambda: "fragment_errors",
        {
            "Namespace": "namespace_errors",
            "Namespace member": "member_errors",
            "Folder": "folder_errors",
            "File": "file_errors",
            "Fragment": "fragment_errors",
        }
    )
    # Descriptions to all possible error types
    # These are output as is after each exception listing, so they may contain
    # html code. Newlines are replaced with <br>-Tags automatically
    error_descriptions = {
        'ResourceAlreadyAssignedError':
            "This errors occurs if a link to an entity is found, and the link "
            "was already found for an entity higher up in the hierarchy.\n\n"
            "For Example: The top-level Root-Entity has the URL "
            "<code>/</code>, if further down a link to another entity is "
            "found, with exactly that url, it is assumed that the link "
            "generation is faulty, instead of that one url points to two "
            "different entities.\n\n"
            "The URL contains a duplicate annotation, because the analyzer "
            "needs unique urls.",
        'ResponseStatusNotOkError':
            "This error occurs if a http response is not served with message "
            "<code>200 Ok</code>.",
        'WrongClassifierError':
            "This error occurs if the link to an entity specifies another "
            "expected classifier than the entity itself reports.",
        'WrongNameError':
            "This error occurs if the link to an entity specifies another "
            "expected name than the entity itself reports.",
        'ResourceNotFoundException':
            "This error occurs if the explorer script somehow deems an url "
            "invalid, and throws this exception by hand to trigger a "
            "<code>404 not found</code>.\n\n"
            "This is fine behaviour for nonsensical URLs. But no page in the "
            "explorer should produce a link to page that contains this "
            "exception.",
        'ValidationError':
            "This error is thrown by the explorer intern page validation code, "
            "that validates each entities output against a schema."
    }

    def __init__(self):
        self.report = {}

    def run(self, entity_errors):
        def default_entry():
            return {
                "error_counts": collections.defaultdict(lambda: 0),
                "error_list": collections.defaultdict(lambda: []),
                "total_count": 0,
            }

        self.report = {
            "error_descriptions": ReportBuilder.error_descriptions,
            "file_errors": default_entry(),
            "folder_errors": default_entry(),
            "fragment_errors": default_entry(),
            "member_errors": default_entry(),
            "namespace_errors": default_entry(),
            "root_errors": default_entry(),
            "total_count": 0,
        }

        for resource, d in entity_errors.items():
            classifier = d["classifier"]
            name = d["name"]
            time_taken = d["time_taken"]
            error_type = d["error"]["type"]
            error_msg = d["error"]["msg"]

            entity = Entity(resource, classifier, name)

            if resource == "/discovery":
                errors = self.report["root_errors"]
            else:
                errors = self.report[
                    ReportBuilder.classifier_report_fields[classifier]]
            errors["total_count"] += 1
            errors["error_counts"][error_type] += 1
            errors["error_list"][error_type].append({
                "entity": entity,
                "error": error_msg,
                "time_taken": time_taken,
            })

            self.report["total_count"] += 1

        self.write_report()

        return self.report

    def write_report(self):
        """
        Writes self.report to file.
        """
        with open(ReportBuilder.report_file, 'w') as outfile:
            json.dump(self.report, outfile, cls=EntityJsonEncoder, indent=4,
                      sort_keys=True)


@skipIf("TEST_ALL_EXPLORER_ENTITIES" not in os.environ,
        "This module is run from the 101worker module testAllExplorerEntities.")
class AllEntitiesTest(TestCase):
    results = None

    @classmethod
    def setUpClass(cls):
        entity_analyzer = EntityAnalyzer(config.incremental_update_time,
                                         config.max_out_degree)
        entity_errors = entity_analyzer.run()

        report_builder = ReportBuilder()
        report = report_builder.run(entity_errors)

        cls.results = report

    @classmethod
    def tearDownClass(cls):
        pass

    # the following methods just signal to a human test executor where
    # errors happened

    def test_root(self):
        if AllEntitiesTest.results['root_errors']['total_count']:
            self.fail()

    def test_namespaces(self):
        if AllEntitiesTest.results['namespace_errors']['total_count']:
            self.fail()

    def test_members(self):
        if AllEntitiesTest.results['member_errors']['total_count']:
            self.fail()

    def test_folders(self):
        if AllEntitiesTest.results['folder_errors']['total_count']:
            self.fail()

    def test_files(self):
        if AllEntitiesTest.results['file_errors']['total_count']:
            self.fail()

    def test_fragments(self):
        if AllEntitiesTest.results['fragment_errors']['total_count']:
            self.fail()
