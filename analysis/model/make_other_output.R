# Load packages ----------------------------------------------------------------
print('Load packages')

library(magrittr)
library(data.table)

# Source functions -------------------------------------------------------------
print('Source functions')

source("analysis/model/fn-check_vitals.R")

# Specify arguments ------------------------------------------------------------
print('Specify arguments')

args <- commandArgs(trailingOnly=TRUE)

if(length(args)==0){
  output <- "table1"
  cohorts <- "prevax;vax;unvax"
} else {
  output <- args[[1]]
  cohorts <- args[[2]]
}

# Separate cohorts -------------------------------------------------------------
print('Separate cohorts')

cohorts <- stringr::str_split(as.vector(cohorts), ";")[[1]]

# Create blank table -----------------------------------------------------------
print('Create blank table')

df <- NULL

# Add output from each cohort --------------------------------------------------
print('Add output from each cohort')

for (i in cohorts) {
  
  tmp <- readr::read_csv(paste0("output/",output,"_",i,"_midpoint6.csv"))
  tmp$cohort <- i
  df <- rbind(df, tmp)
  
}

#Rename columns following OS documents

names(df)[names(df) == "unexposed_events"] <- "unexposed_events_midpoint6"
names(df)[names(df) == "exposed_events"] <- "exposed_events_midpoint6"
names(df)[names(df) == "total_events"] <- "total_events_midpoint6"
names(df)[names(df) == "day0_events"] <- "day0_events_midpoint6"
names(df)[names(df) == "total_exposed"] <- "total_exposed_midpoint6_derived"
names(df)[names(df) == "sample_size"] <- "sample_size_midpoint6"

# Save output ------------------------------------------------------------------
print('Save output')

readr::write_csv(df, paste0("output/",output,"_output_rounded.csv"))