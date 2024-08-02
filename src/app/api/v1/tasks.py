import time
from datetime import timedelta
import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from arq.jobs import Job as ArqJob

from ...schemas.request import TimerRequest
from ...schemas.response import TimerResponse
from ...core.utils import queue

logger = logging.getLogger(__name__)
router = APIRouter(tags=["tasks"])

@router.post("/timer", response_model=TimerResponse)
async def create_task(timer_request: TimerRequest) -> JSONResponse:
    """Create new delayed task

    :param timer_request: request for creating delayed task
    :type timer_request: TimerRequest

    :rtype: TimerResponse
    :return: id and time left to execute the generated task
    """
    try:
        delay_seconds = (timer_request.hours * 60 + timer_request.minutes) * 60 + timer_request.seconds

        # Schedule the task with a delay
        job = await queue.pool.enqueue_job("request_url", timer_request.url,_defer_by=timedelta(seconds=delay_seconds), _job_try=1, _queue_name="delayed_task")
        logger.info(f"Task is created")
        response = TimerResponse(id=str(job.job_id), time_left=timedelta(seconds=delay_seconds).total_seconds())
        return JSONResponse(content=response.model_dump(exclude_none=True), status_code=201)
    except Exception as e:
        logger.error(f"Error while adding task to the queue: {str(e)}")
        print(str(e), flush=True)
        response = TimerResponse(id="-1", error=f"{str(e)}")
        return JSONResponse(content=response.model_dump(exclude_none=True), status_code=500)


@router.get("/timer/{task_id}", response_model=TimerResponse, response_model_exclude_none=True)
async def get_task(task_id:str) -> JSONResponse:
    """Return task information

    :param task_id: id of the created task
    :type str: type of id is string

    :rtype: TimerResponse
    :return: id and time left to execute the task
    """
    try:
        job = ArqJob(task_id, queue.pool, _queue_name="delayed_task")
        job_info = await job.info()
        if job_info is None:
            return JSONResponse(content=TimerResponse(id=task_id, time_left=0).model_dump(exclude_none=True), status_code=200)
        delay_time = job_info.score
        current_time = time.time() * 1000
        if delay_time is not None:
            if current_time < delay_time:
                time_left = (delay_time - current_time)
            else:
                time_left = 0
            response = TimerResponse(id=task_id, time_left=int(time_left/1000))
            return JSONResponse(content=response.model_dump(exclude_none=True), status_code=200)
        else:
            return JSONResponse(content=TimerResponse(id=task_id, error="Unable to get timer information").model_dump(exclude_none=True), status_code=200)
    except Exception as e:
        logger.error(f"Error while getting task from the queue: {str(e)}")
        response = TimerResponse(id=task_id, error="Unable to get the task information")
        return JSONResponse(content=response.model_dump(exclude_none=True), status_code=500)
