# ip_part_comp
GPU enabled computations of particle beds. Year 3 IP by Shermit Singh during degree at University of Southampton

ipf.py is the Python code used to simulate a single droplet in Python.
ip_data.py can be used if so desired to plot the results from the OpenCL simulations. To use, copy log files to a folder and point to it in ip_data.py. The time scale must be adjusted as this will differ based on the log_step used in host.c 

The host.c and propagate.cl files are meant to be used in Visual Studio Community Community 2015 version 14.0.24720.
Files in the clEnqueueTask folder are meant for use with a CPU.
Files in the clEnqueueNDRangeKernel folder are meant for use with a GPU.

Instructions on running are below:
1.	Installing the toolkit
-	First, the appropriate toolkit must be installed. For Nvidia GPU’s the latest CUDA toolkit (version 9.1 as of writing) can be found at https://developer.nvidia.com/cuda-downloads
-	For AMD devices, the AMD APP SDK version 3.0 can be found at http://amd-dev.wpengine.netdna-cdn.com/app-sdk/installers/APPSDKInstaller/3.0.130.135-GA/full/AMD-APP-SDKInstaller-v3.0.130.135-GA-windows-F-x64.exe
2.	Creating the OpenCL project
In Visual Studio, from the menu bar select ‘File’ > ‘New’ > ‘Project’. Expand ‘Visual C++’ in the menu on the left, and select ‘Win32’, then ‘Win32 Console Application’ in the main area. Name the project, and press ‘OK’. In the following Application Wizard, navigate through and tick ‘Empty Project’, and click ‘Finish’
3.	Adding the code to the project
Right-click on ‘Source Files’ within the project in the solution explorer and select ‘Add’ > ‘Existing Item’. Navigate to the provided host file, and repeat for the propagate file
4.	Including OpenCL libraries and linkers
-	Right-click on the project in the solution explorer (the icon is a box around two plus symbols) and select ‘Properties’
-	From the ‘Configurations’ drop-down menu above select ‘All Configurations’.
-	In the menu on the left, navigate to ‘Configuration Properties’ > ‘C/C++’ > ‘General’
-	Add the path to the toolkit installed in Step 1 to the ‘Additional Include Directories’ field. For Nvidia CUDA, this may be something like ‘C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.0\include’ (without quotations)
-	In the menu on the left, navigate to ‘Configuration Properties’ > ‘Linker’ > ‘General’
-	In the ‘Additional Library Directories’ add the path to the appropriate library of the toolkit installed in Step 1. For Nvidia CUDA, this may be something like ‘C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.0\lib\x64’ (without quotations)
-	In the menu on the left, navigate to ‘Configuration Properties’ > ‘Linker’ > ‘Input’
-	Click the drop-down icon in the ‘Additional Dependencies’ Field and select ‘<Edit…>’
-	Add ‘OpenCL.lib’ (without quotations) to the topmost field, and press ‘OK’.
-	Press ‘OK’ again to close the project property page
5.	Running the simulation
-	Navigate to ‘Debug’ in the menu bar and select ‘Start without Debugging’. If successful the console will open, displaying compatible devices. Follow the instructions in the console to run the simulation
6.	Simulation parameters and options
-	Firstly, the ‘file name’ parameter must be changed to point to the location of the propagate file on the system. If this is incorrect, a ‘Failed to load kernel’ message will be printed in the console upon attempting to run the simulation
-	To change the device used for the simulation, scroll to lines 191 and 196 of the host code (GPU). Replace the numbers in the first arguments of the functions as described in the comments in the code. The desired platform and device numbers can be obtained from the list of devices that is displayed upon running the simulation
-	Most parameters of the simulation are defined near the top of the host code, and can be changed if so desired. The time step can be found in line 299 (GPU)
-	The ‘log step’ parameter can be varied to adjust how often log files are created. For simulations of large numbers of particles, this step may want to be increased, sacrificing data resolution in favour of results that take up less storage space on the system
