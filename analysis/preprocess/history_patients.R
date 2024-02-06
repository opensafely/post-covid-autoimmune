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

stage1 <- read_rds(paste0("output/input_",cohort,"_stage1.rds"))

# history outcomes data set
print("Load history outcomes data set")

input_history <- read_csv(paste0("output/input_",cohort,"_history.csv.gz"))

# Filter outcome patients ------------------------------------------------------
print("Filter outcome patients")

stage1_patients <- stage1 %>%
  select(patient_id)

# Filter history patients ------------------------------------------------------
print("Filter history patients")

input_history <- input_history %>%
  filter(patient_id %in% stage1_patients$patient_id)

# Drop columns from input history ----------------------------------------------
print("Drop columns from input history")

input_history <- input_history %>%
  select(-c("index_date_cohort", "end_date_outcome", "end_date_exposure", "cov_cat_sex", "vax_date_covid_1", 
           "tmp_exp_date_covid19_confirmed_sgss", "tmp_exp_date_covid19_confirmed_snomed", "tmp_exp_date_covid19_confirmed_hes", "tmp_exp_date_covid19_confirmed_death",  
           "dereg_date", "sub_date_covid19_hospital", "vax_jcvi_age_1", "vax_jcvi_age_2", "vax_cat_jcvi_group", "vax_date_eligible", "has_follow_up_previous_6months", "has_died", 
           "registered_at_start", "tmp_sub_bin_covid19_confirmed_history_sgss", "tmp_sub_bin_covid19_confirmed_history_snomed", "tmp_sub_bin_covid19_confirmed_history_hes", 
           "exp_date_covid19_confirmed", "sub_bin_covid19_confirmed_history")) %>%
  mutate(patient_id = as.character(patient_id))

# merge data sets --------------------------------------------------------------
print("Merge data sets")

input <- inner_join(stage1, input_history, 
                   by = "patient_id")

# remove datasets from environment

# Save stage 1 new dataset -----------------------------------------------------
print('Save new stage 1 dataset')

saveRDS(input, 
        file = paste0("output/input_",cohort,"_new_stage1.rds"), 
        compress = TRUE)
