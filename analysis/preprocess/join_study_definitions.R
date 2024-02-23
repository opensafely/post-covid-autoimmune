# Load library -----------------------------------------------------------------

library(readr)
library(dplyr)

# Specify command arguments ----------------------------------------------------
print('Specify command arguments')

args <- commandArgs(trailingOnly=TRUE)

if(length(args)==0){
  cohort <- "unvax"
} else {
  cohort <- args[[1]]
}

# Load data set ----------------------------------------------------------------
print("Load data sets")

# outcomes data set
print("Load outcomes data set")

input_outcome <- read_csv(paste0("output/input_",cohort,".csv.gz"))

# history outcomes data set
print("Load history outcomes data set")

input_history <- read_csv(paste0("output/input_",cohort,"_history.csv.gz"))

# Keep columns of interest -----------------------------------------------------

# input_outcome <- input_outcome %>%
#   select(!matches("^tmp_out_|^tmp_cov_bin_|^tmp_sub_bin_|^tmp_exp_"))
  #select(matches("patient_id|^out_date_|^cov_bin_|^cov_num_|^sub_bin_|^cov_cat_|^vax_|has_died|registered"))

input_history <- input_history %>%
  select(matches("patient_id|^cov_bin_history_"))
  #select(patient_id, starts_with("cov_bin_history"))
  
# merge data sets --------------------------------------------------------------
print("Merge data sets")

input <- left_join(input_outcome, input_history, 
               by = c("patient_id")) #left_join or inner_join

# Remove data frame from the environment ---------------------------------------
print("Remove dataframes from the environment")

rm(input_outcome, input_history)

# Save -------------------------------------------------------------------------
print("Save final data set")

#saveRDS(input, file = paste0("output/input_",cohort,"_final.rds"), compress = "gzip")

# Save -------------------------------------------------------------------------

write_csv(input,paste0("output/input_",cohort,"_final.csv.gz"))