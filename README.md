# CS147LinkerAndLoder
Author: Nicholas Hernandez
Email: Nicholas.John.Hernandez@gmail.com

Summary:
Takes the instructions written in CS147DV assembly and converts them to hexadecimal.

Requirements:
	Any Python version 2.6+ 

Usage:

OSX & Linux:
	Open terminal and cd into the directory containing the CS147DVCompiler python file.
	Run the following command:

	$ python3 CS147DVCompiler.py AssemblyCode.txt HexidecimalOutput.dat

Windows:
	Open Command Prompt and cd into the directory containing the CS147DVCompiler python file.
	Run the following command:

	$ py CS147DVCompiler.py AssemblyCode.txt HexidecimalOutput.dat


Note: assemblyCode is the source file with the lines written in CS147DV
Note2: hexadecimalOutput is the destination, and this file can be used by ModelSim.


Semantics:
	require ; at the end of each line
	require whitespace between each argument
	each line can only contain 1 assembly command
	Comments are not allowed
	Immediate can be either (signed)decimal or (unsigned)hex

