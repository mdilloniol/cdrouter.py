#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for accessing CDRouter Results."""

import io

from requests_toolbelt.downloadutils import stream
from marshmallow import Schema, fields, post_load
from .cdr_datetime import DateTime

class TestCount(object):
    """Model for CDRouter Test Counts.

    :param name: (optional) Name as a string.
    :param count: (optional) Count as a string.
    """
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.count = kwargs.get('count', None)

class TestCountSchema(Schema):
    name = fields.Str()
    count = fields.Str()

    @post_load
    def post_load(self, data):
        return TestCount(**data)

class TestDuration(object):
    """Model for CDRouter Test Durations.

    :param name: (optional) Name as a string.
    :param duration: (optional) Duration as a string.
    """
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.duration = kwargs.get('duration', None)

class TestDurationSchema(Schema):
    name = fields.Str()
    duration = fields.Str()

    @post_load
    def post_load(self, data):
        return TestDuration(**data)

class ResultBreakdown(object):
    """Model for CDRouter Result Breakdowns.

    :param passed: (optional) Pass count as a string.
    :param failed: (optional) Fail count as a string.
    :param skipped: (optional) Skipped count as a string.
    """
    def __init__(self, **kwargs):
        self.passed = kwargs.get('passed', None)
        self.failed = kwargs.get('failed', None)
        self.skipped = kwargs.get('skipped', None)

class ResultBreakdownSchema(Schema):
    passed = fields.Str()
    failed = fields.Str()
    skipped = fields.Str()

    @post_load
    def post_load(self, data):
        return ResultBreakdown(**data)

class TimeBreakdown(object):
    """Model for CDRouter Time Breakdowns.

    :param passed: (optional) Pass duration as a string.
    :param failed: (optional) Fail duration as a string.
    """
    def __init__(self, **kwargs):
        self.passed = kwargs.get('passed', None)
        self.failed = kwargs.get('failed', None)

class TimeBreakdownSchema(Schema):
    passed = fields.Str()
    failed = fields.Str()

    @post_load
    def post_load(self, data):
        return TimeBreakdown(**data)

class SetStats(object):
    """Model for CDRouter Result Set Stats.

    :param frequent_failures: (optional) :class:`results.TestCount <results.TestCount>` list
    :param longest_tests: (optional) :class:`results.TestDuration <results.TestDuration>` list
    :param result_breakdown: (optional) :class:`results.ResultBreakdown <results.ResultBreakdown>` object
    :param time_breakdown: (optional) :class:`results.TimeBreakdown <results.TimeBreakdown>` object
    """
    def __init__(self, **kwargs):
        self.frequent_failures = kwargs.get('frequent_failures', None)
        self.longest_tests = kwargs.get('longest_tests', None)
        self.result_breakdown = kwargs.get('result_breakdown', None)
        self.time_breakdown = kwargs.get('time_breakdown', None)

class SetStatsSchema(Schema):
    frequent_failures = fields.Nested(TestCountSchema, many=True)
    longest_tests = fields.Nested(TestDurationSchema, many=True)
    result_breakdown = fields.Nested(ResultBreakdownSchema)
    time_breakdown = fields.Nested(TimeBreakdownSchema)

    @post_load
    def post_load(self, data):
        return SetStats(**data)

class TestResultBreakdown(object):
    """Model for CDRouter TestResult Breakdowns.

    :param failed_at_least_once: (optional) :class:`results.TestCount <results.TestCount>` list
    :param passed_every_time: (optional) :class:`results.TestCount <results.TestCount>` list
    """
    def __init__(self, **kwargs):
        self.failed_at_least_once = kwargs.get('failed_at_least_once', None)
        self.passed_every_time = kwargs.get('passed_every_time', None)

class TestResultBreakdownSchema(Schema):
    failed_at_least_once = fields.Nested(TestCountSchema, many=True)
    passed_every_time = fields.Nested(TestCountSchema, many=True)

    @post_load
    def post_load(self, data):
        return TestResultBreakdown(**data)

class Progress(object):
    """Model for CDRouter Result Progress.

    :param finished: (optional) Finished count as an int.
    :param total: (optional) Total count as an int.
    :param progress: (optional) Progress as an int.
    :param unit: (optional) Unit as a string.
    """
    def __init__(self, **kwargs):
        self.finished = kwargs.get('finished', None)
        self.total = kwargs.get('total', None)
        self.progress = kwargs.get('progress', None)
        self.unit = kwargs.get('unit', None)

class ProgressSchema(Schema):
    finished = fields.Int()
    total = fields.Int()
    progress = fields.Int()
    unit = fields.Str()

    @post_load
    def post_load(self, data):
        return Progress(**data)

class SingleStats(object):
    """Model for CDRouter Single Results Stats.

    :param result_breakdown: (optional) :class:`results.ResultBreakdown <results.ResultBreakdown>` object
    :param progress: (optional) :class:`results.Progress <results.Progress>` object
    """
    def __init__(self, **kwargs):
        self.result_breakdown = kwargs.get('result_breakdown', None)
        self.progress = kwargs.get('progress', None)

class SingleStatsSchema(Schema):
    result_breakdown = fields.Nested(ResultBreakdownSchema)
    progress = fields.Nested(ProgressSchema)

    @post_load
    def post_load(self, data):
        return SingleStats(**data)

class PackageCount(object):
    """Model for CDRouter Package Counts.

    :param package_name: (optional) Package name as a string.
    :param count: (optional) Count as a string.
    """
    def __init__(self, **kwargs):
        self.package_name = kwargs.get('package_name', None)
        self.count = kwargs.get('count', None)

class PackageCountSchema(Schema):
    package_name = fields.Str()
    count = fields.Str(missing=None)

    @post_load
    def post_load(self, data):
        return PackageCount(**data)

class DeviceCount(object):
    """Model for CDRouter Device Counts.

    :param device_name: (optional) Device name as a string.
    :param count: (optional) Count as a string.
    """
    def __init__(self, **kwargs):
        self.device_name = kwargs.get('device_name', None)
        self.count = kwargs.get('count', None)

class DeviceCountSchema(Schema):
    device_name = fields.Str()
    count = fields.Str(missing=None)

    @post_load
    def post_load(self, data):
        return DeviceCount(**data)

class AllStats(object):
    """Model for CDRouter All Results Stats.

    :param frequent_packages: (optional) :class:`results.PackageCount <results.PackageCount>` list
    :param package_names: (optional) :class:`results.PackageCount <results.PackageCount>` list
    :param frequent_devices: (optional) :class:`results.DeviceCount <results.DeviceCount>` list
    :param device_names: (optional) :class:`results.DeviceCount <results.DeviceCount>` list
    """
    def __init__(self, **kwargs):
        self.frequent_packages = kwargs.get('frequent_packages', None)
        self.package_names = kwargs.get('package_names', None)
        self.frequent_devices = kwargs.get('frequent_devices', None)
        self.device_names = kwargs.get('device_names', None)

class AllStatsSchema(Schema):
    frequent_packages = fields.Nested(PackageCountSchema, many=True)
    package_names = fields.Nested(PackageCountSchema, many=True)
    frequent_devices = fields.Nested(DeviceCountSchema, many=True)
    device_names = fields.Nested(DeviceCountSchema, many=True)

    @post_load
    def post_load(self, data):
        return AllStats(**data)

class Metric(object):
    """Model for CDRouter Metrics.

    :param log_file: (optional) Filepath to logfile as a string.
    :param timestamp: (optional) Timestamp for metric as a `DateTime`.
    :param metric: (optional) Metric name as a string.
    :param value: (optional) Metric value as a string.
    :param units: (optional) Metric units as a string.
    :param result: (optional) Metric result as a string.
    :param interface_1: (optional) First interface as a string.
    :param interface_2: (optional) Second interface as a string.
    :param streams: (optional) Stream count as a string.
    """
    def __init__(self, **kwargs):
        self.log_file = kwargs.get('log_file', None)
        self.timestamp = kwargs.get('timestamp', None)
        self.metric = kwargs.get('metric', None)
        self.value = kwargs.get('value', None)
        self.units = kwargs.get('units', None)
        self.result = kwargs.get('result', None)
        self.interface_1 = kwargs.get('interface_1', None)
        self.interface_2 = kwargs.get('interface_2', None)
        self.streams = kwargs.get('streams', None)

class MetricSchema(Schema):
    log_file = fields.Str()
    timestamp = DateTime()
    metric = fields.Str()
    value = fields.Str()
    units = fields.Str()
    result = fields.Str()
    interface_1 = fields.Str()
    interface_2 = fields.Str()
    streams = fields.Str()

    @post_load
    def post_load(self, data):
        return Metric(**data)

class LogDirFile(object):
    """Model for CDRouter Logdir Files.

    :param name: (optional) Name as a string.
    :param size: (optional) Filesize as an int.
    :param modified: (optional) Last-updated time as a `DateTime`.
    """
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.size = kwargs.get('size', None)
        self.modified = kwargs.get('modified', None)

class LogDirFileSchema(Schema):
    name = fields.Str()
    size = fields.Int()
    modified = DateTime()

    @post_load
    def post_load(self, data):
        return LogDirFile(**data)

class Options(object):
    """Model for CDRouter Result Options.

    :param tags: (optional) Tags as string list.
    :param skip_tests: (optional) Tests to skip as string list.
    :param begin_at: (optional) Test name to begin testing at as string.
    :param end_at: (optional) Test name to end testing at as string.
    :param extra_cli_args: (optional) Extra `cdrouter-cli` arguments as string.
    """
    def __init__(self, **kwargs):
        self.tags = kwargs.get('tags', None)
        self.skip_tests = kwargs.get('skip_tests', None)
        self.begin_at = kwargs.get('begin_at', None)
        self.end_at = kwargs.get('end_at', None)
        self.extra_cli_args = kwargs.get('extra_cli_args', None)

class OptionsSchema(Schema):
    tags = fields.List(fields.Str(), missing=None)
    skip_tests = fields.List(fields.Str(), missing=None)
    begin_at = fields.Str()
    end_at = fields.Str()
    extra_cli_args = fields.Str()

    @post_load
    def post_load(self, data):
        return Options(**data)

class Result(object):
    """Model for CDRouter Results.

    :param id: (optional) Result ID as a string.
    :param created: (optional) Creation time as `DateTime`.
    :param updated: (optional) Last-updated time as `DateTime`.
    :param result: (optional) Result as a string.
    :param status: (optional) Status as a string.
    :param loops: (optional) Loop count as an int.
    :param tests: (optional) Test count as an int.
    :param passed: (optional) Passed count as an int.
    :param fail: (optional) Failed count as an int.
    :param duration: (optional) Duration in seconds as an int.
    :param size_on_disk: (optional) Size on disk in bytes as an int.
    :param starred: (optional) Bool `True` if result is starred.
    :param archived: (optional) Bool `True` if result is archived.
    :param result_dir: (optional) Filepath to result directory as a string.
    :param agent_name: (optional) Agent name as a string.
    :param package_name: (optional) Package name as a string.
    :param device_name: (optional) Device name as a string.
    :param config_name: (optional) Config name as a string.
    :param package_id: (optional) Package ID as a string.
    :param device_id: (optional) Device ID as a string.
    :param config_id: (optional) Config ID as a string.
    :param user_id: (optional) User ID as a string.
    :param note: (optional) Note as a string.
    :param pause_message: (optional) Pause message as a string (if currently paused).
    :param build_info: (optional) Build info as a string.
    :param tags: (optional) Tags as a string list.
    :param testcases: (optional) Testcases as a string list.
    :param options: (optional) :class:`results.Options <results.Options>` object
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.created = kwargs.get('created', None)
        self.updated = kwargs.get('updated', None)
        self.result = kwargs.get('result', None)
        self.status = kwargs.get('status', None)
        self.loops = kwargs.get('loops', None)
        self.tests = kwargs.get('tests', None)
        self.passed = kwargs.get('pass', None)
        self.fail = kwargs.get('fail', None)
        self.duration = kwargs.get('duration', None)
        self.size_on_disk = kwargs.get('size_on_disk', None)
        self.starred = kwargs.get('starred', None)
        self.archived = kwargs.get('archived', None)
        self.result_dir = kwargs.get('result_dir', None)
        self.agent_name = kwargs.get('agent_name', None)
        self.package_name = kwargs.get('package_name', None)
        self.device_name = kwargs.get('device_name', None)
        self.config_name = kwargs.get('config_name', None)
        self.package_id = kwargs.get('package_id', None)
        self.device_id = kwargs.get('device_id', None)
        self.config_id = kwargs.get('config_id', None)
        self.user_id = kwargs.get('user_id', None)
        self.note = kwargs.get('note', None)
        self.pause_message = kwargs.get('pause_message', None)
        self.build_info = kwargs.get('build_info', None)
        self.tags = kwargs.get('tags', None)
        self.testcases = kwargs.get('testcases', None)
        self.options = kwargs.get('options', None)

class ResultSchema(Schema):
    id = fields.Str()
    created = DateTime()
    updated = DateTime()
    result = fields.Str()
    status = fields.Str()
    loops = fields.Int()
    tests = fields.Int()
    passed = fields.Int(attribute='pass', load_from='pass', dump_to='pass')
    fail = fields.Int()
    duration = fields.Int()
    size_on_disk = fields.Int()
    starred = fields.Bool()
    archived = fields.Bool()
    result_dir = fields.Str()
    agent_name = fields.Str()
    package_name = fields.Str()
    device_name = fields.Str()
    config_name = fields.Str()
    package_id = fields.Str()
    device_id = fields.Str()
    config_id = fields.Str()
    user_id = fields.Str()
    note = fields.Str()
    pause_message = fields.Str(missing=None)
    build_info = fields.Str(missing=None)
    tags = fields.List(fields.Str())
    testcases = fields.List(fields.Str(), missing=None)
    options = fields.Nested(OptionsSchema)

    @post_load
    def post_load(self, data):
        return Result(**data)

class ResultsService(object):
    """Service for accessing CDRouter Results."""

    RESOURCE = 'results'
    BASE = RESOURCE + '/'

    def __init__(self, service):
        self.service = service
        self.base = self.BASE

    def list(self, filter=None, type=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        """Get a list of results.

        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param limit: (optional) Limit returned list length.
        :param page: (optional) Page to return.
        :return: :class:`results.Result <results.Result>` list
        """
        schema = ResultSchema(exclude=('result', 'loops', 'tests', 'result_dir', 'agent_name', 'config_name', 'note', 'pause_message', 'testcases', 'options', 'build_info'))
        resp = self.service.list(self.base, filter, type, sort, limit, page)
        return self.service.decode(schema, resp, many=True)

    def list_csv(self, filter=None, type=None, sort=None, limit=None, page=None): # pylint: disable=redefined-builtin
        """Get a list of results as CSV.

        :param filter: (optional) Filters to apply as a string list.
        :param type: (optional) `union` or `inter` as string.
        :param sort: (optional) Sort fields to apply as string list.
        :param limit: (optional) Limit returned list length.
        :param page: (optional) Page to return.
        :rtype: string
        """
        return self.service.list(self.base, filter, type, sort, limit, page, format='csv').text

    def get(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get a result.

        :param id: Result ID as string.
        :return: :class:`results.Result <results.Result>` object
        :rtype: results.Result
        """
        schema = ResultSchema()
        resp = self.service.get_id(self.base, id)
        return self.service.decode(schema, resp)

    def stop(self, id, when=None): # pylint: disable=invalid-name,redefined-builtin
        """Stop a running result.

        :param id: Result ID as string.
        :param when: Must be string `end-of-test` or `end-of-loop`.
        """
        return self.service.post(self.base+str(id)+'/stop/', params={'when': when})

    def stop_end_of_test(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Stop a running result at the end of the current test.

        :param id: Result ID as string.
        """
        return self.stop(id, 'end-of-test')

    def stop_end_of_loop(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Stop a running result at the end of the current loop.

        :param id: Result ID as string.
        """
        return self.stop(id, 'end-of-loop')

    def pause(self, id, when=None): # pylint: disable=invalid-name,redefined-builtin
        """Pause a running result.

        :param id: Result ID as string.
        :param when: Must be string `end-of-test` or `end-of-loop`.
        """
        return self.service.post(self.base+str(id)+'/pause/', params={'when': when})

    def pause_end_of_test(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Pause a running result at the end of the current test.

        :param id: Result ID as string.
        """
        return self.pause(id, 'end-of-test')

    def pause_end_of_loop(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Pause a running result at the end of the current loop.

        :param id: Result ID as string.
        """
        return self.pause(id, 'end-of-loop')

    def unpause(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Unpause a running result.

        :param id: Result ID as string.
        """
        return self.service.post(self.base+str(id)+'/unpause/')

    def edit(self, resource):
        """Edit a result.

        :param resource: :class:`results.Result <results.Result>` object
        :return: :class:`results.Result <results.Result>` object
        :rtype: results.Result
        """
        schema = ResultSchema(exclude=('id', 'created', 'updated', 'result', 'status', 'loops', 'tests', 'pass', 'fail', 'duration', 'size_on_disk', 'result_dir', 'agent_name', 'package_name', 'config_name', 'package_id', 'config_id', 'pause_message', 'build_info', 'options'))
        json = self.service.encode(schema, resource)

        schema = ResultSchema()
        resp = self.service.edit(self.base, resource.id, json)
        return self.service.decode(schema, resp)

    def delete(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Delete a result.

        :param id: Result ID as string.
        """
        return self.service.delete_id(self.base, id)

    def get_shares(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Get shares for a result.

        :param id: Result ID as string.
        :return: :class:`cdrouter.Share <cdrouter.Share>` list
        """
        return self.service.get_shares(self.base, id)

    def edit_shares(self, id, user_ids): # pylint: disable=invalid-name,redefined-builtin
        """Edit shares for a result.

        :param id: Result ID as string.
        :param user_ids: User IDs as int list.
        :return: :class:`cdrouter.Share <cdrouter.Share>` list
        """
        return self.service.edit_shares(self.base, id, user_ids)

    def export(self, id, exclude_captures=False): # pylint: disable=invalid-name,redefined-builtin
        """Export a result.

        :param id: Result ID as string.
        :param exclude_captures: If bool `True`, don't export capture files
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        return self.service.export(self.base, id, params={'exclude_captures': exclude_captures})

    def bulk_export(self, ids, exclude_captures=False):
        """Bulk export a set of results.

        :param ids: String list of result IDs.
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        return self.service.bulk_export(self.base, ids, params={'exclude_captures': exclude_captures})

    def bulk_copy(self, ids):
        """Bulk copy a set of results.

        :param ids: String list of result IDs.
        :return: :class:`results.Result <results.Result>` list
        """
        schema = ResultSchema()
        return self.service.bulk_copy(self.base, self.RESOURCE, ids, schema)

    def bulk_edit(self, _fields, ids=None, filter=None, type=None, all=False): # pylint: disable=redefined-builtin
        """Bulk edit a set of results.

        :param _fields: :class:`results.Result <results.Result>` object
        :param ids: (optional) String list of result IDs.
        :param filter: (optional) String list of filters.
        :param type: (optional) `union` or `inter` as string.
        :param all: (optional) Apply to all if bool `True`.
        """
        return self.service.bulk_edit(self.base, self.RESOURCE, _fields, ids=ids, filter=filter, type=type, all=all)

    def bulk_delete(self, ids=None, filter=None, type=None, all=False): # pylint: disable=redefined-builtin
        """Bulk delete a set of results.

        :param ids: (optional) String list of result IDs.
        :param filter: (optional) String list of filters.
        :param type: (optional) `union` or `inter` as string.
        :param all: (optional) Apply to all if bool `True`.
        """
        return self.service.bulk_delete(self.base, self.RESOURCE, ids=ids, filter=filter, type=type, all=all)

    def all_stats(self):
        """Compute stats for all results.

        :return: :class:`results.AllStats <results.AllStats>` object
        :rtype: results.AllStats
        """
        schema = AllStatsSchema()
        resp = self.service.post(self.base, params={'stats': 'all'})
        return self.service.decode(schema, resp)

    def set_stats(self, ids):
        """Compute stats for a set of results.

        :param id: Result IDs as string list.
        :return: :class:`results.SetStats <results.SetStats>` object
        :rtype: results.SetStats
        """
        schema = SetStatsSchema()
        resp = self.service.post(self.base, params={'stats': 'set'}, json=[{'id': str(x)} for x in ids])
        return self.service.decode(schema, resp)

    def single_stats(self, id): # pylint: disable=invalid-name,redefined-builtin
        """Compute stats for a result.

        :param id: Result ID as string.
        :return: :class:`results.SingleStats <results.SingleStats>` object
        :rtype: results.SingleStats
        """
        schema = SingleStatsSchema()
        resp = self.service.get(self.base+str(id)+'/', params={'stats': 'all'})
        return self.service.decode(schema, resp)

    def list_logdir(self, id, filter=None, sort=None): # pylint: disable=invalid-name,redefined-builtin
        """Get a list of logdir files.

        :param id: Result ID as string.
        :param filter: Filter to apply as string.
        :param sort: Sort field to apply as string.
        :return: :class:`results.LogDirFile <results.LogDirFile>` list
        """
        schema = LogDirFileSchema()
        resp = self.service.list(self.base+str(id)+'/logdir/', filter, sort)
        return self.service.decode(schema, resp, many=True)

    def get_logdir_file(self, id, filename): # pylint: disable=invalid-name,redefined-builtin
        """Download a logdir file.

        :param id: Result ID as string.
        :param filename: Logdir filename as string.
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        resp = self.service.get(self.base+str(id)+'/logdir/'+filename+'/')
        resp.raise_for_status()
        b = io.BytesIO()
        stream.stream_response_to_file(resp, path=b)
        b.seek(0)
        return (b, self.service.filename(resp))

    def download_logdir_archive(self, id, format='zip', exclude_captures=False): # pylint: disable=invalid-name,redefined-builtin
        """Download logdir archive in tgz or zip format.

        :param id: Result ID as string.
        :param format: (optional) Format to download, must be string `zip` or `tgz`.
        :param exclude_captures: If bool `True`, don't include capture files
        :rtype: tuple `(io.BytesIO, 'filename')`
        """
        resp = self.service.get(self.base+str(id)+'/logdir/', params={'format': format, 'exclude_captures': exclude_captures})
        resp.raise_for_status()
        b = io.BytesIO()
        stream.stream_response_to_file(resp, path=b)
        b.seek(0)
        return (b, self.service.filename(resp))

    def get_test_metric(self, id, name, metric): # pylint: disable=invalid-name,redefined-builtin
        """Get a test metric.

        :param id: Result ID as string.
        :param name: Test name as string.
        :param metric: Metric name as string.
        :return: :class:`results.Metric <results.Metric>` object
        :rtype: results.Metric
        """
        schema = MetricSchema()
        resp = self.service.get(self.base+str(id)+'/metrics/'+name+'/'+metric+'/',
                                params={'format': format})
        return self.service.decode(schema, resp, many=True)

    def get_test_metric_csv(self, id, name, metric): # pylint: disable=invalid-name,redefined-builtin
        """Get a test metric as CSV.

        :param id: Result ID as string.
        :param name: Test name as string.
        :param id: Metric name as string.
        :rtype: string
        """
        return self.service.get(self.base+str(id)+'/metrics/'+name+'/'+metric+'/',
                                params={'format': 'csv'}).text
