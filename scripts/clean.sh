#!/usr/bin/env bash
find production -mindepth 1 ! -name .gitkeep -delete
find workspace -mindepth 1 ! -name .gitkeep -delete
