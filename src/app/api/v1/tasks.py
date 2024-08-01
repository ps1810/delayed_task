import time
from datetime import timedelta

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from arq.jobs import Job as ArqJob

from ...schemas.request import TimerRequest
from ...schemas.response import TimerResponse
from ...core.utils import queue

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
        job = await queue.pool.enqueue_job("request_url", timer_request.url,_defer_by=timedelta(seconds=delay_seconds), _job_try=1)

        response = TimerResponse(id=str(job.job_id), time_left=timedelta(seconds=delay_seconds).total_seconds())
        return JSONResponse(content=response.model_dump(exclude_none=True), status_code=201)
    except Exception as e:
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
        job = ArqJob(task_id, queue.pool)
        job_info = await job.info()
        if job_info is None:
            return JSONResponse(content=TimerResponse(id=task_id, time_left=0).dict(), status_code=200)
        delay_time = job_info.score
        current_time = time.time() * 1000
        if current_time < delay_time:
            time_left = (delay_time - current_time)
        else:
            time_left = (current_time - delay_time)
        response = TimerResponse(id=task_id, time_left=int(time_left/1000))
        return JSONResponse(content=response.model_dump(exclude_none=True), status_code=200)
    except Exception as e:
        response = TimerResponse(id=task_id, error="Unable to get the task information")
        return JSONResponse(content=response.model_dump(exclude_none=True), status_code=500)
