# Delayed Task

## Description
The project provides a delayed task execution capability. Users can define task parameters and a delay period. Upon expiration of the delay, the system initiates task execution.

## Table of Contents
1. [Installation](#installation)
2. [Overview](#overview) 
3. [API Documentation](#api_documentation)
4. [Point to Remember](#points_to_remember)


## Installation
Instructions for setting up your project. For example:

```bash
# Clone the repository
git clone https://github.com/yourusername/project-name.git

# Navigate to the project directory
cd delayed-task

# Run the docker compose file
docker compose up
```
## Overview

The project is a Python application built using FastAPI. To manage tasks, it employs a Redis queue accessed through the Arq library. Tasks are added to the queue using the enqueue_job function. Redis ensures persistent storage of task data, safeguarding it even in case of server downtime. 


## API Documentation

There are 2 API's. One API adds task and the other API returns the remaining time to run the task.

#### 1. Create Task
- **URL**: `/timer`
- **Method**: `POST`
- **Request Body**:
  - `hours` (int): Number of hours after which task will run. (Required)
  - `minutes` (int): Number of minutes after which task will run. (Required)
  - `seconds` (int): Number of seconds after which task will run. (Required)
  - `url` (string): url to make requests. (Required)
- **Response**:
  - `201 Created`: Task created successfully
  - `500 Internal Server Error`: If any exception occurs
- **Example Response**:
```json
{
  "id": "5264ca0402144d18bc94a8adb5d9b9a3",
  "time_left": 28
}
```

#### 2. Get Task information
- **URL**: `/timer/<task_id>`
- **Method**: `GET`
- **Response**:
  - `200 OK`: Task information retrieved
  - `500 Internal Server Error`: If any exception occurs
- **Example Response**:
```json
{
  "id": "5264ca0402144d18bc94a8adb5d9b9a3",
  "time_left": 28
}

{
  "id": "5264ca0402144d18bc94a8adb5d9b9a3",
  "time_left": 0
}
This response will come if the task is already fired and result is stored.

```

## Points to Remember

#### 1. The job will run only 1 time
#### 2. The job result will stay for 10 seconds in the queue
#### 3. The queue data is persistent.

