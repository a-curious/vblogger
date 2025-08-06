# VBlogger Debug Commands
# Usage: make <command>

.PHONY: help list-configs table-rocks harriman testing create-config debug-loader

help:
	@echo "Available debug commands:"
	@echo "  make list-configs    - List all available configurations"
	@echo "  make table-rocks     - Run with Table Rocks configuration"
	@echo "  make harriman        - Run with Harriman configuration"
	@echo "  make testing         - Run in testing mode"
	@echo "  make create-config   - Launch configuration creator"
	@echo "  make debug-loader    - Test configuration loader"

list-configs:
	@echo "Debug - List Configurations"
	@echo "==========================="
	python vblogger_main.py --list-configs

table-rocks:
	@echo "Debug - Table Rocks Configuration"
	@echo "=================================="
	python vblogger_main.py --config table_rocks_config

harriman:
	@echo "Debug - Harriman Configuration"
	@echo "=============================="
	python vblogger_main.py --config harriman_20250803_config

testing:
	@echo "Debug - Testing Mode"
	@echo "===================="
	python vblogger_main.py --config table_rocks_config --testing

create-config:
	@echo "Debug - Create Configuration"
	@echo "============================"
	python create_config.py

debug-loader:
	@echo "Debug - Configuration Loader"
	@echo "============================"
	python debug_config_loader.py 