
###################### IMPORT OPTIONAL LIBRARIES #############################################

import numpy as np  			# Numpy - Python'S Numerical Library
import mpl_toolkits 			# Toolkits Are Collections Of Application-Specific Functions That Extend Matplotlib
from copy import deepcopy  		# Python Module For Copying Objects
import matplotlib 			# Visualization With Python
import matplotlib.pyplot as plt 	# Provides A Matlab-Like Plotting Framework

###################### IMPORT OPENQUAKE LIBRARIES ############################################

from openquake.hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueParser		# Reads An Earthquake Catalogue To CSV
from openquake.hmtk.parsers.catalogue.csv_catalogue_parser import CsvCatalogueWriter  		# Writes An Earthquake Catalogue To CSV
from openquake.hmtk.plotting.seismicity.catalogue_plots import build_filename, plot_magnitude_time_density, plot_depth_histogram, plot_magnitude_depth_density, plot_observed_recurrence
from openquake.hmtk.plotting.seismicity.catalogue_plots import plot_magnitude_time_scatter
from openquake.hmtk.seismicity.catalogue import Catalogue
from openquake.hmtk.plotting.seismicity.catalogue_plots import plot_magnitude_time_scatter

###################### IMPORT OPENQUAKE-DECLUSTERING LIBRARIES ################################

#################################################################
###### There Are Two Type Of Declustering Method So It Is #######
###### Needed To Import The Methods At First And Then Add #######
###### The Distance-Time Window To Apply On Methods	 #######
#################################################################

from openquake.hmtk.seismicity.declusterer.dec_gardner_knopoff import GardnerKnopoffType1
from openquake.hmtk.seismicity.declusterer.dec_afteran import Afteran
from openquake.hmtk.seismicity.declusterer.base import BaseCatalogueDecluster
from openquake.hmtk.seismicity.declusterer.distance_time_windows import GardnerKnopoffWindow, GruenthalWindow, UhrhammerWindow, BaseDistanceTimeWindow

print("Everything Imported OK!")

#======================================================================================================

#################################################################
###### Now Let'S Read The Catalogue Withing Given Location ######
#################################################################

catalogue_filename = '/home/nima/wd/decluster-method/HMTK/input_data/Aegean_reduced_catalog.csv'
parser = CsvCatalogueParser(catalogue_filename) 							# Calls The Catalogue
catalogue = parser.read_file(start_year=1500, end_year=2020) 					# Read The Catalogue

#################################################################
###### Just Showing If The Catlogue Is Imported Correctly  ######
#################################################################

print("The catalogue contains %g events" % catalogue.get_number_events())
print(catalogue.data['magnitude'])
print(catalogue.load_to_array(['year', 'longitude', 'latitude', 'depth', 'magnitude']))
print("Everything Imported OK!")
print("The catalogue contains %g events" % catalogue.get_number_events())
catalogue.sort_catalogue_chronologically()

################################################# DECLUSTERING ###################################

#################################################################
###### Calling out the declustering method, each mehod needs ####
###### a catalogue and a specific configuration so that the  ####
###### proccess will be done accroding to the plan ##############
#################################################################

declust_method1 = GardnerKnopoffType1()
declust_method2 = Afteran()

declust_config1 = {"time_distance_window": GardnerKnopoffWindow(), "fs_time_prop": 1.0, "time_cutoff": 100} # given in days
declust_config_afteran = {"time_distance_window":  GruenthalWindow(), "time_window": 100.0}
declust_config2 = {"time_distance_window": GruenthalWindow(), "fs_time_prop": 1.0, "time_cutoff": 100} # given in days
declust_config3 = {"time_distance_window": UhrhammerWindow(), "fs_time_prop": 1.0, "time_cutoff": 100} # given in days
#declust_config4 = {"time_distance_window": BaseDistanceTimeWindow(), "fs_time_prop": 1.0, "time_cutoff": 100} # given in days


cluster_index1, cluster_flag1 = declust_method1.decluster(catalogue, declust_config1)
print(cluster_index1)
cluster_index2, cluster_flag2 = declust_method1.decluster(catalogue, declust_config2)
print(cluster_index2)
cluster_index3, cluster_flag3 = declust_method1.decluster(catalogue, declust_config3)
print(cluster_index3)
cluster_index4, cluster_flag4 = declust_method2.decluster(catalogue, declust_config_afteran)
print(cluster_index4)

#===================================================================================================================#

data1 = np.column_stack([catalogue.get_decimal_time(), catalogue.data['magnitude'], catalogue.data['longitude'], catalogue.data['latitude'], cluster_index1, cluster_flag1])
print('      Time    Magnitude    Long.    Lat.   Cluster No. Index (-1 = foreshock, 0 = mainshock, 1 = afterschock)')
for row in data1:
    print('%14.8f  %6.2f  %8.3f  %8.3f  %6.0f  %6.0f' %(row[0], row[1], row[2], row[3], row[4], row[5]))
catalogue_dec1 = deepcopy(catalogue)
catalogue_dec2 = deepcopy(catalogue)
catalogue_dec3 = deepcopy(catalogue)
catalogue_dec4 = deepcopy(catalogue)


catalogue_fore_after1 = deepcopy(catalogue)
catalogue_fore_after2 = deepcopy(catalogue)
catalogue_fore_after3 = deepcopy(catalogue)
catalogue_fore_after4 = deepcopy(catalogue)




# Logical indexing: Chossing the outputs for the main events: Cluster_flag = 0
mainshock_flag1 = cluster_flag1 == 0
Fore_After_flag1 = cluster_flag1 == (1 or -1)
mainshock_flag2 = cluster_flag2 == 0
Fore_After_flag2 = cluster_flag2 == (1 or -1)
mainshock_flag3 = cluster_flag3 == 0
Fore_After_flag3 = cluster_flag3 == (1 or -1)
mainshock_flag4 = cluster_flag4 == 0
Fore_After_flag4 = cluster_flag4 == (1 or -1)



# Filtering the foreshocks and aftershocks in the copy of the catalogue
catalogue_dec1.purge_catalogue(mainshock_flag1)
catalogue_dec2.purge_catalogue(mainshock_flag2)
catalogue_dec3.purge_catalogue(mainshock_flag3)
catalogue_dec4.purge_catalogue(mainshock_flag4)


catalogue_fore_after1.purge_catalogue(Fore_After_flag1)
catalogue_fore_after2.purge_catalogue(Fore_After_flag2)
catalogue_fore_after3.purge_catalogue(Fore_After_flag3)
catalogue_fore_after4.purge_catalogue(Fore_After_flag4)






# Printing the number of events considered main shocks
print('Declustering: ok')
print("Number of events in original catalogue: %g" % catalogue.get_number_events())
print('Number of mainshocks for knopoff: %g' % catalogue_dec1.get_number_events())
print('Number of mainshocks for Gruenthal: %g' % catalogue_dec2.get_number_events())
print('Number of mainshocks Uhrhammer: %g' % catalogue_dec3.get_number_events())
print('Number of mainshocks Afteran: %g' % catalogue_dec4.get_number_events())

'''
plt.figure(0)
plt.plot(catalogue.data['longitude'], catalogue.data['latitude'], 'bo')
plt.plot(catalogue_dec1.data['longitude'], catalogue_dec1.data['latitude'], 'ro')
plt.show()
plt.figure(1)
plt.plot(catalogue.data['longitude'], catalogue.data['latitude'], 'bo')
plt.plot(catalogue_dec2.data['longitude'], catalogue_dec2.data['latitude'], 'ro')
plt.show()
plt.figure(2)
plt.plot(catalogue.data['longitude'], catalogue.data['latitude'], 'bo')
plt.plot(catalogue_dec3.data['longitude'], catalogue_dec3.data['latitude'], 'ro')
plt.show()

############################### Results Of Declustering Including Main-Shock And Clusters ###################################

#plt.show()
#plt.savefig('test.png')
'''
output_cat_dec = '/home/nima/wd/decluster-method/HMTK/output_data/hmtk_decluster_knopoff.knopoff.csv';
cat_csv = CsvCatalogueWriter(output_cat_dec);
cat_csv.write_file(catalogue_dec1);
print("Catalogue successfully written to %s" % output_cat_dec)

output_cat_dec = '/home/nima/wd/decluster-method/HMTK/output_data/hmtk_decluster_knopoff.Gru.csv';
cat_csv = CsvCatalogueWriter(output_cat_dec);
cat_csv.write_file(catalogue_dec2);
print("Catalogue successfully written to %s" % output_cat_dec)

output_cat_dec = '/home/nima/wd/decluster-method/HMTK/output_data/hmtk_decluster_knopoff.Uhr.csv';
cat_csv = CsvCatalogueWriter(output_cat_dec);
cat_csv.write_file(catalogue_dec3);
print("Catalogue successfully written to %s" % output_cat_dec)

output_cat_dec = '/home/nima/wd/decluster-method/HMTK/output_data/hmtk_decluster_Afteran.GRU.csv';
cat_csv = CsvCatalogueWriter(output_cat_dec);
cat_csv.write_file(catalogue_dec4);
print("Catalogue successfully written to %s" % output_cat_dec)

output_cat_dec = '/home/nima/wd/decluster-method/HMTK/output_data/Fore_After_knopoff.csv';
cat_csv = CsvCatalogueWriter(output_cat_dec);
cat_csv.write_file(catalogue_fore_after1);
print("Catalogue successfully written to %s" % output_cat_dec)

output_cat_dec = '/home/nima/wd/decluster-method/HMTK/output_data/Fore_After_Gruenthal.csv';
cat_csv = CsvCatalogueWriter(output_cat_dec);
cat_csv.write_file(catalogue_fore_after2);
print("Catalogue successfully written to %s" % output_cat_dec)

output_cat_dec = '/home/nima/wd/decluster-method/HMTK/output_data/Fore_After_Uhrhammer.csv';
cat_csv = CsvCatalogueWriter(output_cat_dec);
cat_csv.write_file(catalogue_fore_after3);
print("Catalogue successfully written to %s" % output_cat_dec)

output_cat_dec = '/home/nima/wd/decluster-method/HMTK/output_data/Fore_After_Afteran.csv';
cat_csv = CsvCatalogueWriter(output_cat_dec);
cat_csv.write_file(catalogue_fore_after4);
print("Catalogue successfully written to %s" % output_cat_dec)

print("Declustering Has Been Done Successfully!")
