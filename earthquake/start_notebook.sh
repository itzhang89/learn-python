#!/usr/bin/env bash
docker run -p 8888:8888 -m 8g --cpus 4 -v "${PWD}":/home/jovyan/work jupyter/scipy-notebook:lab-3.2.8
