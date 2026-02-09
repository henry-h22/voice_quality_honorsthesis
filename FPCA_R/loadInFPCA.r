# This script is gonna be to load in the data from csvs, and run the FPCA stuff
# It'll create a BUNCH of objects when sourced

library(tidyverse)
library(fda)

pulses <- read.csv("egg_pulses.csv", header = TRUE, check.names = FALSE)