#!/bin/bash

gcloud app deploy && gcloud app logs tail -s default

