OOMMF="/home/david/opt/oommf-1.2a5bis/oommf.tcl"

all:
	make relaxation
	make dynamics

relaxation:
	for w in 0 25 50 75 100; do \
		tclsh $(OOMMF) boxsi -threads 4 -parameters "w $${w}" OOMMF_static.mif; \
		mv InitialMagnetisation-Oxs*.omf InitialMagnetisation_w$${w}.omf; \
		mv InitialMagnetisation.odt InitialMagnetisation_w$${w}.odt; \
	done

dynamics:
	for w in 0 25 50 75 100; do \
		tclsh $(OOMMF) boxsi -threads 4 -parameters "w $${w} INIT_STATE InitialMagnetisation_w$${w}.omf" OOMMF_dynamics.mif; \
		mkdir -p omfs_w$${w}; \
		mv SWDynamics*.omf omfs_w$${w}/; \
	done

data:
	for w in 0 25 50 75 100; do \
		tclsh "~/opt/oommf-1.2a5bis/oommf.tcl" avf2ovf -grid irreg \
		InitialMagnetisation_w$${w}.omf > InitialMagnetisation_w$${w}_ordered.omf; \
		python ../data_plot/OOMMF_generate_data.py \
	   	--omfs "omfs_w$${w}" \
		--initial_state "InitialMagnetisation_w$${w}_ordered.omf" \
		--out_name "w$${w}" \
		--Ms "0.658e6"; \
	done

plots_squared:
	for w in 0; do \
		python ../data_plot/OOMMF_process_data.py \
		--omfs "omfs_w$${w}" \
	   	--out_name "w$${w}" --vminf 1 --vmaxf 10 --ylim 0 30 \
		--scale power2 --pdf_name "spectra_w$${w}_squared"; \
	done
	for w in 25 50 75 100; do \
		python ../data_plot/OOMMF_process_data.py \
	   	--omfs "omfs_w$${w}" \
	   	--out_name "w$${w}" --vminf 1 --vmaxf 200 --ylim 0 30 \
		--scale power2 --pdf_name "spectra_w$${w}_squared"; \
	done

plots_log:
	for w in 0 25 50 75 100; do \
		python ../data_plot/OOMMF_process_data.py \
	   	--omfs "omfs_w$${w}" \
	   	--out_name "w$${w}" --vminf 9 --vmaxf 1 --ylim 0 30 \
		--pdf_name "spectra_w$${w}_log10" \
	   	--get_data "spectra_w$${w}_log10.dat"; \
	done
