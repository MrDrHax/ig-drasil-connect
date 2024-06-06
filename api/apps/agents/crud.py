from fastapi import HTTPException
import markdown
import requests
from sqlalchemy.orm import Session
from . import models
import boto3
from datetime import datetime, timedelta
from cache.cache_object import cachedData
import json

from config import Config

import logging
logger = logging.getLogger(__name__)