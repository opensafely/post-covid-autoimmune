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

# outcomes data set ------------------------------------------------------------
print("Load outcomes data set")

stage1 <- read_rds(paste0("output/input_",cohort,"_stage1.rds")) 

# history outcomes data set ----------------------------------------------------
print("Load history outcomes data set")

input_history <- read_csv(paste0("output/input_",cohort,"_history.csv.gz")) 

# Keep patient and history columns ---------------------------------------------
print("Keep patient and history columns")

input_history <- input_history[grepl("patient_id|^cov_bin_history_", names(input_history))]

# Format columns and add new variable ------------------------------------------
print("Format columns and add new variable")

input_history$patient_id <- as.character(input_history$patient_id)

input_history <- input_history %>%
  mutate(across(contains('_bin'), ~ as.logical(.)),
         # sensitivity variable
         sub_bin_history_composite_ai = cov_bin_history_composite_ai
  )

# Rename columns ---------------------------------------------------------------
print("Rename columns")

names(input_history)[names(input_history) == "cov_bin_history_hashimoto_thyroiditis"] <- "cov_bin_history_hashimoto"
names(input_history)[names(input_history) == "cov_bin_history_iga_vasculitis"] <- "cov_bin_history_iga_vasc"
names(input_history)[names(input_history) == "cov_bin_history_pernicious_anaemia"] <- "cov_bin_history_pern_anaemia"
names(input_history)[names(input_history) == "cov_bin_history_multiple_sclerosis"] <- "cov_bin_history_ms"
names(input_history)[names(input_history) == "cov_bin_history_myasthenia_gravis"] <- "cov_bin_history_myasthenia"
names(input_history)[names(input_history) == "cov_bin_history_longit_myelitis"] <- "cov_bin_history_long_myelitis"

# Set reference level for binaries ---------------------------------------------
print('Set reference level for binaries')

bin_factors <- colnames(input_history)[grepl("_bin_",colnames(input_history))]

input_history[,bin_factors] <- lapply(input_history[,bin_factors], 
                                      function(x) factor(x, levels = c("FALSE","TRUE")))

# Filter history patients ------------------------------------------------------
print("Filter history patients")

input_history <- input_history[input_history$patient_id %in% stage1$patient_id,]

# merge data sets --------------------------------------------------------------
print("Merge data sets")

input <- left_join(stage1, input_history, 
                   by = "patient_id") 

# Remove datasets from the environment -----------------------------------------
print("Remove datasets from environment")

rm(input_history, stage1)

# Save stage 1 new dataset -----------------------------------------------------
print('Save new stage 1 dataset')

saveRDS(input, 
        file = paste0("output/input_",cohort,"_new_stage1.rds"), 
        compress = TRUE)
