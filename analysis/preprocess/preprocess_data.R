# Load libraries ---------------------------------------------------------------
tictoc::tic()
library(magrittr)
library(dplyr)
library(tidyverse)
library(lubridate)
library(data.table)
library(readr)

# Specify command arguments ----------------------------------------------------
args <- commandArgs(trailingOnly=TRUE)
print(length(args))
if(length(args)==0){
  # use for interactive testing
  cohort_name <- "prevax"
} else {
  cohort_name <- args[[1]]
}

fs::dir_create(here::here("output", "not-for-review"))
fs::dir_create(here::here("output", "review"))

#data set
input_path <- paste0("output/input_",cohort_name,".csv.gz")

# Get column names -------------------------------------------------------------

all_cols <- fread(paste0("output/input_",cohort_name,".csv.gz"), 
                  header = TRUE, 
                  sep = ",", 
                  nrows = 0, 
                  stringsAsFactors = FALSE) %>%
  #select(-c(cov_num_systolic_bp_date_measured)) %>% #This column is not needed in Neuro
  names()

#Get columns types based on their names
cat_cols <- c("patient_id", grep("_cat", all_cols, value = TRUE))
bin_cols <- c(grep("_bin", all_cols, value = TRUE), 
              grep("prostate_cancer_", all_cols, value = TRUE),
              "has_follow_up_previous_6months", "has_died", "registered_at_start")
num_cols <- c(grep("_num", all_cols, value = TRUE),
              grep("vax_jcvi_age_", all_cols, value = TRUE))
date_cols <- grep("_date", all_cols, value = TRUE)
# Set the class of the columns with match to make sure the column match the type
col_classes <- setNames(
  c(rep("c", length(cat_cols)),
    rep("l", length(bin_cols)),
    rep("d", length(num_cols)),
    rep("D", length(date_cols))
  ), 
  all_cols[match(c(cat_cols, bin_cols, num_cols, date_cols), all_cols)]
)
# read the input file and specify colClasses
df <- read_csv(input_path, col_types = col_classes) 

df$cov_num_bmi_date_measured <- NULL
df$cov_num_systolic_bp_date_measured <- NULL#This column is not needed in GI
print(paste0("Dataset has been read successfully with N = ", nrow(df), " rows"))
print("type of columns:\n")

#message("Column names found")

# Identify columns containg "_date" --------------------------------------------

#date_cols <- grep("_date", colnames(cols), value = TRUE)

#message("Date columns identified")

# Set class to date ------------------------------------------------------------

#col_classes <- setNames(rep("Date", length(date_cols)), date_cols)

#message("Column classes defined")

# Read cohort dataset ---------------------------------------------------------- 

# df <- fread(paste0("output/input_",cohort_name,".csv.gz", col_types = cols(patient_id = "c", death_date="D"))) %>%
#   select(patient_id, death_date)
# df <- df %>% inner_join(prelim_data, by = "patient_id")

message(paste0("Dataset has been read successfully with N = ", nrow(df), " rows"))

# Add death_date from prelim data ----------------------------------------------

prelim_data <- read_csv("output/index_dates.csv.gz",col_types=cols(patient_id = "c",death_date="D")) %>%
  select(patient_id,death_date)
df <- df %>% inner_join(prelim_data,by="patient_id")

message("Death date added!")
message(paste0("After adding death N = ", nrow(df), " rows"))

# Format columns ---------------------------------------------------------------
# dates, numerics, factors, logicals

df <- df %>%
  mutate( across(contains('_birth_year'),
                 ~ format(as.Date(.,origin='1970-01-01'), "%Y")),
          across(contains('_num') & !contains('date'), ~ as.numeric(.)),
          across(contains('_cat'), ~ as.factor(.)),
          across(contains('_bin'), ~ as.logical(.)))

# Overwrite vaccination information for dummy data and vax cohort only --

if(Sys.getenv("OPENSAFELY_BACKEND") %in% c("", "expectations") &&
   cohort_name %in% c("vax")) {
  source("analysis/preprocess/modify_dummy_vax_data.R")
  message("Vaccine information overwritten successfully")
}

# Describe data ----------------------------------------------------------------

sink(paste0("output/not-for-review/describe_",cohort_name,".txt"))
print(Hmisc::describe(df))
sink()

message ("Cohort ",cohort_name, " description written successfully!")

#Combine BMI variables to create one history of obesity variable ---------------

df$cov_bin_obesity <- ifelse(df$cov_bin_obesity == TRUE | 
                               df$cov_cat_bmi_groups=="Obese",TRUE,FALSE)

# QC for consultation variable--------------------------------------------------
#max to 365 (average of one per day)
df <- df %>%
  mutate(cov_num_consulation_rate = replace(cov_num_consulation_rate, 
                                            cov_num_consulation_rate > 365, 365))

# QC for outpatient variable----------------------------------------------------
#max to 365 (average of one per day)
df <- df %>%
  mutate(cov_num_outpatient_rate = replace(cov_num_outpatient_rate,
                                           cov_num_outpatient_rate > 365, 365))

# Define COVID-19 severity --------------------------------------------------------------

df <- df %>%
  mutate(sub_cat_covid19_hospital = 
           ifelse(!is.na(exp_date_covid19_confirmed) &
                    !is.na(sub_date_covid19_hospital) &
                    sub_date_covid19_hospital - exp_date_covid19_confirmed >= 0 &
                    sub_date_covid19_hospital - exp_date_covid19_confirmed < 29, "hospitalised",
                  ifelse(!is.na(exp_date_covid19_confirmed), "non_hospitalised", 
                         ifelse(is.na(exp_date_covid19_confirmed), "no_infection", NA)))) %>%
  mutate(across(sub_cat_covid19_hospital, factor))

df <- df[!is.na(df$patient_id),]
df[,c("sub_date_covid19_hospital")] <- NULL

message("COVID19 severity determined successfully")

# Create vars for neurodegenerative outcomes -----------------------------------

# Prior diagnosis variable ("_prior") 
# FALSE = anyone who has a diagnosis after the index date/who never has a diagnosis
# TRUE = anyone who has a diagnosis before the index date

df <- df %>%
  mutate(
    # Outcome 1: Inflammatory arthritis
    out_date_ra_prior = ifelse(out_date_ra > index_date_cohort | is.na(out_date_ra), FALSE, TRUE),
    out_date_undiff_eia_prior = ifelse(out_date_undiff_eia > index_date_cohort | is.na(out_date_undiff_eia), FALSE, TRUE),
    out_date_psoa_prior = ifelse(out_date_psoa > index_date_cohort | is.na(out_date_psoa), FALSE, TRUE),
    out_date_axial_prior = ifelse(out_date_axial > index_date_cohort | is.na(out_date_axial), FALSE, TRUE),
    out_date_grp1_ifa_prior = ifelse(out_date_grp1_ifa > index_date_cohort | is.na(out_date_grp1_ifa), FALSE, TRUE),
    # Outcome 2: Connective tissue disorders
    out_date_sle_prior = ifelse(out_date_sle > index_date_cohort | is.na(out_date_sle), FALSE, TRUE),
    out_date_sjs_prior = ifelse(out_date_sjs > index_date_cohort | is.na(out_date_sjs), FALSE, TRUE),
    out_date_sss_prior = ifelse(out_date_sss > index_date_cohort | is.na(out_date_sss), FALSE, TRUE),
    out_date_im_prior = ifelse(out_date_im > index_date_cohort | is.na(out_date_im), FALSE, TRUE),
    out_date_as_prior = ifelse(out_date_as > index_date_cohort | is.na(out_date_as), FALSE, TRUE),
    out_date_grp2_ctd_prior = ifelse(out_date_grp2_ctd > index_date_cohort | is.na(out_date_grp2_ctd), FALSE, TRUE),
    # Outcome 3: Inflammatory skin disease
    out_date_psoriasis_prior = ifelse(out_date_psoriasis > index_date_cohort | is.na(out_date_psoriasis), FALSE, TRUE),
    out_date_hs_prior = ifelse(out_date_hs > index_date_cohort | is.na(out_date_hs), FALSE, TRUE),
    out_date_grp3_isd_prior = ifelse(out_date_grp3_isd > index_date_cohort | is.na(out_date_grp3_isd), FALSE, TRUE),
    # Outcome 4: Autoimmune GI / Inflammatory bowel disease
    out_date_ibd_prior = ifelse(out_date_ibd > index_date_cohort | is.na(out_date_ibd), FALSE, TRUE),
    out_date_crohn_prior = ifelse(out_date_crohn > index_date_cohort | is.na(out_date_crohn), FALSE, TRUE),
    out_date_uc_prior = ifelse(out_date_uc > index_date_cohort | is.na(out_date_uc), FALSE, TRUE),
    out_date_celiac_prior = ifelse(out_date_celiac > index_date_cohort | is.na(out_date_celiac), FALSE, TRUE),
    out_date_grp4_agi_ibd_prior = ifelse(out_date_grp4_agi_ibd > index_date_cohort | is.na(out_date_grp4_agi_ibd), FALSE, TRUE),
    # Outcome 5: Thyroid diseases
    out_date_addison_prior = ifelse(out_date_addison > index_date_cohort | is.na(out_date_addison), FALSE, TRUE),
    out_date_grave_prior = ifelse(out_date_grave > index_date_cohort | is.na(out_date_grave), FALSE, TRUE),
    out_date_hashimoto_thyroiditis_prior = ifelse(out_date_hashimoto_thyroiditis > index_date_cohort | is.na(out_date_hashimoto_thyroiditis), FALSE, TRUE),
    out_date_grp5_atv_prior = ifelse(out_date_grp5_atv > index_date_cohort | is.na(out_date_grp5_atv), FALSE, TRUE),
    # Outcome 6: Autoimmune vasculitis
    out_date_anca_prior = ifelse(out_date_anca > index_date_cohort | is.na(out_date_anca), FALSE, TRUE),
    out_date_gca_prior = ifelse(out_date_gca > index_date_cohort | is.na(out_date_gca), FALSE, TRUE),
    out_date_iga_vasculitis_prior = ifelse(out_date_iga_vasculitis > index_date_cohort | is.na(out_date_iga_vasculitis), FALSE, TRUE),
    out_date_pmr_prior = ifelse(out_date_pmr > index_date_cohort | is.na(out_date_pmr), FALSE, TRUE),
    out_date_grp6_trd_prior = ifelse(out_date_grp6_trd > index_date_cohort | is.na(out_date_grp6_trd), FALSE, TRUE),
    # Outcome 7: Hematologic Diseases
    out_date_immune_thromb_prior = ifelse(out_date_immune_thromb > index_date_cohort | is.na(out_date_immune_thromb), FALSE, TRUE),
    out_date_pernicious_anaemia_prior = ifelse(out_date_pernicious_anaemia > index_date_cohort | is.na(out_date_pernicious_anaemia), FALSE, TRUE),
    out_date_apa_prior = ifelse(out_date_apa > index_date_cohort | is.na(out_date_apa), FALSE, TRUE),
    out_date_aha_prior = ifelse(out_date_aha > index_date_cohort | is.na(out_date_aha), FALSE, TRUE),
    out_date_grp7_htd_prior = ifelse(out_date_grp7_htd > index_date_cohort | is.na(out_date_grp7_htd), FALSE, TRUE),
    # Outcome 8: Inflammatory neuromuscular disease
    out_date_glb_prior = ifelse(out_date_glb > index_date_cohort | is.na(out_date_glb), FALSE, TRUE),
    out_date_multiple_sclerosis_prior = ifelse(out_date_multiple_sclerosis > index_date_cohort | is.na(out_date_multiple_sclerosis), FALSE, TRUE),
    out_date_myasthenia_gravis_prior = ifelse(out_date_myasthenia_gravis > index_date_cohort | is.na(out_date_myasthenia_gravis), FALSE, TRUE),
    out_date_longit_myelitis_prior = ifelse(out_date_longit_myelitis > index_date_cohort | is.na(out_date_longit_myelitis), FALSE, TRUE),
    ut_date_cis_prior = ifelse(out_date_cis > index_date_cohort | is.na(out_date_cis), FALSE, TRUE),
    out_date_grp8_ind_prior = ifelse(out_date_grp8_ind > index_date_cohort | is.na(out_date_grp8_ind), FALSE, TRUE),
    # Outcome 9: Composite autoimmune disease
    out_date_composite_ai_prior = ifelse(out_date_composite_ai > index_date_cohort | is.na(out_date_composite_ai), FALSE, TRUE))

  message("Prior diagnosis variables created")

# Restrict columns and save analysis dataset ---------------------------------

df1 <- df%>% select(patient_id,"death_date",starts_with("index_date_"),
                    has_follow_up_previous_6months,
                    dereg_date,
                    #prior_diagnosis,
                    starts_with("end_date_"),
                    contains("sub_"), # Subgroups
                    contains("exp_"), # Exposures
                    contains("out_"), # Outcomes
                    contains("cov_"), # Covariates
                    contains("qa_"), # Quality assurance
                    contains("step"), # diabetes steps
                    contains("vax_date_eligible"), # Vaccination eligibility
                    contains("vax_date_"), # Vaccination dates and vax type 
                    contains("vax_cat_")# Vaccination products
)

df1[,colnames(df)[grepl("tmp_",colnames(df))]] <- NULL

# Repo specific preprocessing 

saveRDS(df1, file = paste0("output/input_",cohort_name,".rds"), compress = "gzip")

message(paste0("Input data saved successfully with N = ", nrow(df1), " rows"))

# Describe data --------------------------------------------------------------

sink(paste0("output/not-for-review/describe_input_",cohort_name,"_stage0.txt"))
print(Hmisc::describe(df1))
sink()

# Restrict columns and save Venn diagram input dataset -----------------------

df2 <- df %>% select(starts_with(c("patient_id","tmp_out_date","out_date")))

# Describe data --------------------------------------------------------------

sink(paste0("output/not-for-review/describe_venn_",cohort_name,".txt"))
print(Hmisc::describe(df2))
sink()

# SAVE

saveRDS(df2, file = paste0("output/venn_",cohort_name,".rds"))

message("Venn diagram data saved successfully")
tictoc::toc() 