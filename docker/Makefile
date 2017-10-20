SOMEVARIABLE=2
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
	@echo "Starting relaxation of stripes with variable DMI periodicity"
	@echo "------------------------------------------------------"
	@cd ../sim && \
		docker run -t -v `pwd`:/io -u `id -u`:`id -g` \
		oommf /bin/bash -c "make"

plot_nebm:
	@echo "Plotting data from NEBM simulation with D = ${DMI}e-4 Jm**-2"
	@echo "------------------------------------------------------------"
	@cd ../ && \
		docker run -t -v `pwd`:/io -u `id -u`:`id -g` \
		nebm /bin/bash -c "python plot/plot_energy_bands.py --method boundary --D_list ${DMI} --snapshots"
	@cd ../ && \
		docker run -t -v `pwd`:/io -u `id -u`:`id -g` \
		nebm /bin/bash -c "python plot/plot_energy_bands.py --method linear_interpolations --D_list ${DMI} --snapshots"
	@cd ../ && \
		docker run -t -v `pwd`:/io -u `id -u`:`id -g` \
		nebm /bin/bash -c "python plot/plot_energy_bands.py --method climbing --D_list ${DMI} --snapshots"
