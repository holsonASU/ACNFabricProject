This project is for CSE 534 - Advanced Computer Networks at Arizona State University. The contents of this project are as follows.

3DAssets Folder: A vestigal folder from when the project was originally experimenting with 3D rendering on the Graphics node.

Outputs Folder: A folder containing the the output logs from the experiment, the graphs for frame rate and bandwidth, and an Excel spreadsheet for tallying the experiments.

Videos Folder: A misleadingly named folder containing two game screenshots: one at 1080p and the other at 720p. These are the frames used to simulate GPU traffic to the client.

Logs Folder: A folder used to output logs when running code on my personal machine, locally.

GenerateClientCommands.py: A Python script to generate clientCommands2.txt.

RunExperiment.ipynb: The experiment used to run the experiments. The experiment is chosen by a variable in the notebook.

SliceConfiguration.ipynb: The notebook used to set up the FABRIC slice.

client.py: The client script running on the client node.

experimentAnalysis.py: A script that reads the logs in Outputs and calculates the average RTT and graphs.

graphicserver.py: The script running on the graphics server.

logicserver.py: The script that runs on the logic servers.

mesh.py/test.py: Two vestigal files that were from originally experimenting using GPU and 3D rendering.
