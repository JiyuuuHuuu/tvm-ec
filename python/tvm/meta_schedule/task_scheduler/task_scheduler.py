# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Auto-tuning Task Scheduler"""

from typing import Callable, List, Optional

from tvm._ffi import register_object
from tvm.meta_schedule.measure_callback.measure_callback import MeasureCallback
from tvm.runtime import Object

from ..runner import Runner
from ..builder import Builder
from ..database import Database
from ..cost_model import CostModel
from ..tune_context import TuneContext
from .. import _ffi_api


@register_object("meta_schedule.TaskScheduler")
class TaskScheduler(Object):
    """The abstract task scheduler interface.

    Parameters
    ----------
    tasks: List[TuneContext]
        The list of tune context to process.
    builder: Builder
        The builder of the scheduler.
    runner: Runner
        The runner of the scheduler.
    database: Database
        The database of the scheduler.
    measure_callbacks: List[MeasureCallback] = None
        The list of measure callbacks of the scheduler.
    """

    tasks: List[TuneContext]
    builder: Builder
    runner: Runner
    database: Database
    cost_model: Optional[CostModel]
    measure_callbacks: List[MeasureCallback]

    def tune(self) -> None:
        """Auto-tuning."""
        _ffi_api.TaskSchedulerTune(self)  # type: ignore # pylint: disable=no-member

    def next_task_id(self) -> int:
        """Fetch the next task id.

        Returns
        -------
        next_task_id : int
            The next task id.
        """
        return _ffi_api.TaskSchedulerNextTaskId(self)  # type: ignore # pylint: disable=no-member

    def join_running_task(self, task_id: int) -> None:
        """Wait until the task is finished.

        Parameters
        ----------
        task_id : int
            The task id to be joined.
        """
        _ffi_api.TaskSchedulerJoinRunningTask(self, task_id)  # type: ignore # pylint: disable=no-member

    def initialize_task(self, task_id: int) -> None:
        """Initialize modules of the given task.

        Parameters
        ----------
        task_id : int
            The task id to be initialized.
        """
        _ffi_api.TaskSchedulerInitializeTask(self, task_id)  # type: ignore # pylint: disable=no-member

    def set_task_stopped(self, task_id: int) -> None:
        """Set specific task to be stopped.

        Parameters
        ----------
        task_id : int
            The task id to be stopped.
        """
        _ffi_api.TaskSchedulerSetTaskStopped(self, task_id)  # type: ignore # pylint: disable=no-member

    def is_task_running(self, task_id: int) -> bool:
        """Check whether the task is running.

        Parameters
        ----------
        task_id : int
            The task id to be checked.

        Returns
        -------
        running : bool
            Whether the task is running.
        """
        return _ffi_api.TaskSchedulerIsTaskRunning(self, task_id)  # type: ignore # pylint: disable=no-member


@register_object("meta_schedule.PyTaskScheduler")
class _PyTaskScheduler(TaskScheduler):
    """
    A TVM object task scheduler to support customization on the python side.
    This is NOT the user facing class for function overloading inheritance.

    See also: PyTaskScheduler
    """

    def __init__(
        self,
        tasks: List[TuneContext],
        builder: Builder,
        runner: Runner,
        database: Database,
        cost_model: Optional[CostModel] = None,
        measure_callbacks: Optional[List[MeasureCallback]] = None,
        f_tune: Callable = None,
        f_initialize_task: Callable = None,
        f_set_task_stopped: Callable = None,
        f_is_task_running: Callable = None,
        f_join_running_task: Callable = None,
        f_next_task_id: Callable = None,
    ):
        """Constructor."""

        self.__init_handle_by_constructor__(
            _ffi_api.TaskSchedulerPyTaskScheduler,  # type: ignore # pylint: disable=no-member
            tasks,
            builder,
            runner,
            database,
            cost_model,
            measure_callbacks,
            f_tune,
            f_initialize_task,
            f_set_task_stopped,
            f_is_task_running,
            f_join_running_task,
            f_next_task_id,
        )


class PyTaskScheduler:
    """
    An abstract task scheduler with customized methods on the python-side.
    This is the user facing class for function overloading inheritance.

    Note: @derived_object is required for proper usage of any inherited class.
    """

    _tvm_metadata = {
        "cls": _PyTaskScheduler,
        "fields": [
            "tasks",
            "builder",
            "runner",
            "database",
            "cost_model",
            "measure_callbacks",
        ],
        "methods": [
            "tune",
            "initialize_task",
            "set_task_stopped",
            "is_task_running",
            "join_running_task",
            "next_task_id",
        ],
    }

    def __init__(
        self,
        tasks: List[TuneContext],
        builder: Builder,
        runner: Runner,
        database: Database,
        cost_model: Optional[CostModel] = None,
        measure_callbacks: Optional[List[MeasureCallback]] = None,
    ):
        self.tasks = tasks
        self.builder = builder
        self.runner = runner
        self.database = database
        self.cost_model = cost_model
        self.measure_callbacks = measure_callbacks

    def tune(self) -> None:
        """Auto-tuning."""
        # Using self._outer to replace the self pointer
        _ffi_api.TaskSchedulerTune(self._outer())  # type: ignore # pylint: disable=no-member

    def next_task_id(self) -> int:
        """Fetch the next task id.

        Returns
        -------
        next_task_id : int
            The next task id.
        """
        raise NotImplementedError

    def join_running_task(self, task_id: int) -> None:
        """Wait until the task is finished.

        Parameters
        ----------
        task_id : int
            The task id to be joined.
        """
        # Using self._outer to replace the self pointer
        _ffi_api.TaskSchedulerJoinRunningTask(self._outer(), task_id)  # type: ignore # pylint: disable=no-member

    def initialize_task(self, task_id: int) -> None:
        """Initialize modules of the given task.

        Parameters
        ----------
        task_id : int
            The task id to be initialized.
        """
        # Using self._outer to replace the self pointer
        _ffi_api.TaskSchedulerInitializeTask(self._outer(), task_id)  # type: ignore # pylint: disable=no-member

    def set_task_stopped(self, task_id: int) -> None:
        """Set specific task to be stopped.

        Parameters
        ----------
        task_id : int
            The task id to be stopped.
        """
        # Using self._outer to replace the self pointer
        _ffi_api.TaskSchedulerSetTaskStopped(self._outer(), task_id)  # type: ignore # pylint: disable=no-member

    def is_task_running(self, task_id: int) -> bool:
        """Check whether the task is running.

        Parameters
        ----------
        task_id : int
            The task id to be checked.

        Returns
        -------
        running : bool
            Whether the task is running.
        """
        # Using self._outer to replace the self pointer
        return _ffi_api.TaskSchedulerIsTaskRunning(self._outer(), task_id)  # type: ignore # pylint: disable=no-member
