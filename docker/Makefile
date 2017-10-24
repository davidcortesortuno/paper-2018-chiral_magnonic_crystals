#!/bin/bash

# -----------------------------------------------------------------------------

# Build the image using the Dockerfile parameters
image:
	docker build -t oommf .

# Clean all the images
clean_images:
	@echo "This will remove the Docker oommf image "
	docker rmi -f oommf

# -----------------------------------------------------------------------------

# -t run a pseudo TTY, -d detach to run in the background
# -u is to run as user:group so files are not owned by root (somehow it is
# important to run the commands with -t) 
run_simulations:
	@echo "Starting relaxation and excitation of stripes with variable DMI periodicity"
	@echo "------------------------------------------------------"
	@cd ../sim && \
		docker run -t -v `pwd`:/io -u `id -u`:`id -g` \
		oommf /bin/bash -c "make"

generate_data:
	@echo "Generating spatio-temporal data to generate the spin wave spectra"
	@echo "------------------------------------------------------"
	@cd ../sim && \
		docker run -t -v `pwd`:/io -u `id -u`:`id -g` \
		oommf /bin/bash -c "make data"

plot_squared:
	@echo "Plotting spectra with squared power scale"
	@echo "------------------------------------------------------------"
	@cd ../sim && \
		docker run -t -v `pwd`:/io -u `id -u`:`id -g` \
		oommf /bin/bash -c "make plots_squared"

plot_logs:
	@echo "Plotting spectra with log power scale"
	@echo "------------------------------------------------------------"
	@cd ../sim && \
		docker run -t -v `pwd`:/io -u `id -u`:`id -g` \
		oommf /bin/bash -c "make plots_log"
