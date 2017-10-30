#!/bin/bash

# Automated script to reproduce simulations, data and plots

run_all:
	@echo "Building Docker container:"
	@cd docker && make image
	@echo "Running OOMMF simulations for different DMI periodicities"
	@cd docker && \
	   	make run_simulations && \
		make generate_data && \
		make plot_squared && make plot_logs

generate_sim_data:
	@cd docker && \
		make generate_data && \
		make plot_squared && make plot_logs
