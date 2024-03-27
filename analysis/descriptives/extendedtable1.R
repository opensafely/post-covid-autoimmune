# Load libraries ---------------------------------------------------------------
print('Load libraries')

library(magrittr)
#library(dplyr)

# Specify redaction threshold --------------------------------------------------
print('Specify redaction threshold')

threshold <- 6

# Source common functions ------------------------------------------------------
print('Source common functions')

source("analysis/utility.R")

# Specify arguments ------------------------------------------------------------
print('Specify arguments')

args <- commandArgs(trailingOnly=TRUE)

if(length(args)==0){
  cohort <- "prevax"
} else {
  cohort <- args[[1]]
}

# Load data --------------------------------------------------------------------
print("Load data")

df <- readr::read_rds(paste0("output/input_",cohort,"_new_stage1.rds"))

# Format columns ---------------------------------------------------------------
# dates, numerics, factors, logicals

df$sub_bin_covid19_confirmed_history <- as.factor(df$sub_bin_covid19_confirmed_history) 

# Remove people with history of COVID-19 ---------------------------------------
print("Remove people with history of COVID-19")

df <- df[df$sub_bin_covid19_confirmed_history==FALSE,]

# Create exposure indicator ----------------------------------------------------
print("Create exposure indicator")

df$exposed <- !is.na(df$exp_date_covid19_confirmed)

# Define consultation rate groups ----------------------------------------------
print("Define consultation rate groups")

df$cov_cat_consulation_rate <- ""
df$cov_cat_consulation_rate <- ifelse(df$cov_num_consulation_rate==0, "0", df$cov_cat_consulation_rate)
df$cov_cat_consulation_rate <- ifelse(df$cov_num_consulation_rate>=1 & df$cov_num_consulation_rate<=5, "1-5", df$cov_cat_consulation_rate)
df$cov_cat_consulation_rate <- ifelse(df$cov_num_consulation_rate>=6, "6+", df$cov_cat_consulation_rate)

# Define outpatient rate groups ------------------------------------------------
print("Define outpatient rate groups")

df$cov_cat_outpatient_rate <- ""
df$cov_cat_outpatient_rate <- ifelse(df$cov_num_outpatient_rate==0, "0", df$cov_cat_outpatient_rate)
df$cov_cat_outpatient_rate <- ifelse(df$cov_num_outpatient_rate>=1 & df$cov_num_outpatient_rate<=5, "1-5", df$cov_cat_outpatient_rate)
df$cov_cat_outpatient_rate <- ifelse(df$cov_num_outpatient_rate>=6, "6+", df$cov_cat_outpatient_rate)

# Filter data ------------------------------------------------------------------
print("Filter data")

df <- df[,c("exposed",
            "cov_cat_consulation_rate",
            "cov_cat_outpatient_rate",
            "cov_bin_healthcare_worker",
            "cov_bin_liver_disease",
            "cov_bin_ckd",
            "cov_bin_cancer",
            "cov_bin_hypertension",
            "cov_bin_diabetes",
            "cov_bin_obesity",
            "cov_bin_copd",
            "cov_bin_ami",
            "cov_bin_isch_stroke",
            "sub_bin_covid19_confirmed_history", 
            "cov_bin_history_ra",
            "cov_bin_history_undiff_eia",
            "cov_bin_history_psoa",
            "cov_bin_history_axial",
            "cov_bin_history_grp1_ifa",
            "cov_bin_history_sle",
            "cov_bin_history_sjs",
            "cov_bin_history_sss",
            "cov_bin_history_im",
            "cov_bin_history_mctd",
            "cov_bin_history_as",
            "cov_bin_history_grp2_ctd",
            "cov_bin_history_psoriasis",
            "cov_bin_history_hs",
            "cov_bin_history_grp3_isd",
            "cov_bin_history_ibd",
            "cov_bin_history_crohn",
            "cov_bin_history_uc",
            "cov_bin_history_celiac",
            "cov_bin_history_grp4_agi_ibd",
            "cov_bin_history_addison",
            "cov_bin_history_grave",
            "cov_bin_history_hashimoto",
            "cov_bin_history_grp5_atv",
            "cov_bin_history_anca",
            "cov_bin_history_gca",
            "cov_bin_history_iga_vasc",
            "cov_bin_history_pmr",
            "cov_bin_history_grp6_trd",
            "cov_bin_history_immune_thromb",
            "cov_bin_history_pern_anaemia",
            "cov_bin_history_apa",
            "cov_bin_history_aha",
            "cov_bin_history_grp7_htd",
            "cov_bin_history_glb",
            "cov_bin_history_ms",
            "cov_bin_history_myasthenia",
            "cov_bin_history_long_myelitis",
            "cov_bin_history_cis",
            "cov_bin_history_grp8_ind",
            "cov_bin_history_composite_ai")]

df$All <- "All"

# Aggregate data ---------------------------------------------------------------
print("Aggregate data")

df <- tidyr::pivot_longer(df,
                          cols = setdiff(colnames(df),c("patient_id","exposed")),
                          names_to = "characteristic",
                          values_to = "subcharacteristic")

df$total <- 1

df <- aggregate(cbind(total, exposed) ~ characteristic + subcharacteristic, 
                data = df,
                sum)

#df <- df[df$subcharacteristic!=FALSE,]
df$subcharacteristic <- ifelse(df$subcharacteristic=="","Missing",df$subcharacteristic)

# Sort characteristics ---------------------------------------------------------
print("Sort characteristics")

df$characteristic <- factor(df$characteristic,
                            levels = c("All",
                                       "cov_cat_consulation_rate",
                                       "cov_cat_outpatient_rate",
                                       "cov_bin_healthcare_worker",
                                       "cov_bin_liver_disease",
                                       "cov_bin_ckd",
                                       "cov_bin_cancer",
                                       "cov_bin_hypertension",
                                       "cov_bin_diabetes",
                                       "cov_bin_obesity",
                                       "cov_bin_copd",
                                       "cov_bin_ami",
                                       "cov_bin_isch_stroke",
                                       "sub_bin_covid19_confirmed_history", 
                                       "cov_bin_history_ra",
                                       "cov_bin_history_undiff_eia",
                                       "cov_bin_history_psoa",
                                       "cov_bin_history_axial",
                                       "cov_bin_history_grp1_ifa",
                                       "cov_bin_history_sle",
                                       "cov_bin_history_sjs",
                                       "cov_bin_history_sss",
                                       "cov_bin_history_im",
                                       "cov_bin_history_mctd",
                                       "cov_bin_history_as",
                                       "cov_bin_history_grp2_ctd",
                                       "cov_bin_history_psoriasis",
                                       "cov_bin_history_hs",
                                       "cov_bin_history_grp3_isd",
                                       "cov_bin_history_ibd",
                                       "cov_bin_history_crohn",
                                       "cov_bin_history_uc",
                                       "cov_bin_history_celiac",
                                       "cov_bin_history_grp4_agi_ibd",
                                       "cov_bin_history_addison",
                                       "cov_bin_history_grave",
                                       "cov_bin_history_hashimoto",
                                       "cov_bin_history_grp5_atv",
                                       "cov_bin_history_anca",
                                       "cov_bin_history_gca",
                                       "cov_bin_history_iga_vasc",
                                       "cov_bin_history_pmr",
                                       "cov_bin_history_grp6_trd",
                                       "cov_bin_history_immune_thromb",
                                       "cov_bin_history_pern_anaemia",
                                       "cov_bin_history_apa",
                                       "cov_bin_history_aha",
                                       "cov_bin_history_grp7_htd",
                                       "cov_bin_history_glb",
                                       "cov_bin_history_ms",
                                       "cov_bin_history_myasthenia",
                                       "cov_bin_history_long_myelitis",
                                       "cov_bin_history_cis",
                                       "cov_bin_history_grp8_ind",
                                       "cov_bin_history_composite_ai"),
                            labels = c("All",
                                       "Consultation rate",
                                       "Outpatient rate",
                                       "Health care worker",
                                       "Liver disease",
                                       "Chronic kidney disease",
                                       "Cancer",
                                       "Hypertension",
                                       "Diabetes",
                                       "Obesity",
                                       "Chronic obstructive pulmonary disease (COPD)",
                                       "Acute myocardial infarction",
                                       "Ischaemic stroke",
                                       "History of COVID-19",
                                       "History of rheumatoid arthritis",
                                       "History of undifferentiated inflammatory arthritis",
                                       "History of psoriatic arthritis",
                                       "History of axial spondylarthritis",
                                       "History of inflammatory arthritis (Group 1)",
                                       "History of systematic lupus erythematosus",
                                       "History of Sjogren’s syndrome",
                                       "History of Systemic sclerosis/scleroderma",
                                       "History of inflammatory myositis/polymyositis/dermatomyositis",
                                       "History of mixed connective tissue disease",
                                       "History of antiphospholipid syndrome",
                                       "History of connective tissue disorders (Group 2)",
                                       "History of psoriasis",
                                       "History of hydradenitis suppurativa",
                                       "History of inflammatory skin disease (Group 3)",
                                       "History of inflammatory bowel disease(combined ulcerative colitis and Crohn's)",
                                       "History of Crohn’s disease",
                                       "History of ulcerative colitis",
                                       "History of celiac disease",
                                       "History of autoimmune gastrointestinal diseaseI / inflammatory bowel disease (Group 4)",
                                       "History of Addison’s disease",
                                       "History of Grave’s disease",
                                       "History of Hashimoto’s thyroiditis",
                                       "History of Thyroid diseases (Group 5)",
                                       "History of antineutrophilic cytoplasmic antibody (ANCA)-associated",
                                       "History of giant cell arteritis",
                                       "History of immunoglobulin A (IgA) vasculitis",
                                       "History of polymyalgia rheumatica (PMR)",
                                       "History of autoimmune vasculitis (Group 6)",
                                       "History of immune thrombocytopenia (formerly known as idiopathic thrombocytopenic purpura)",
                                       "History of pernicious anaemia",
                                       "History of aplastic anaemia",
                                       "History of autoimmune haemolytic anaemia",
                                       "History of hematologic diseases (Group 7)",
                                       "History of Guillain-Barré",
                                       "History of multiple sclerosis",
                                       "History of myasthenia gravis",
                                       "History of longitudinal myelitis",
                                       "History of clinically isolated syndrome",
                                       "History of inflammatory neuromuscular disease (Group 8)",
                                       "History of composite autoimmune")) 

# Sort subcharacteristics ------------------------------------------------------
print("Sort subcharacteristics")

df$subcharacteristic <- factor(df$subcharacteristic, 
                               levels = c("All",
                                          "0",
                                          "1-5",
                                          "6+",
                                          "Healthcare worker",
                                          "TRUE", "FALSE",
                                          "Missing"),
                               labels = c("All",
                                          "0",
                                          "1-5",
                                          "6+",
                                          "Healthcare worker",
                                          "TRUE", "FALSE", 
                                          "Missing")) 

# Sort data --------------------------------------------------------------------
print("Sort data")

df <- df[order(df$subcharacteristic, decreasing = TRUE),]
df <- df[order(df$characteristic),]

# Save Table 1 -----------------------------------------------------------------
print('Save Table 1')

write.csv(df, paste0("output/extendedtable1_",cohort,".csv"), row.names = FALSE)

# Perform redaction ------------------------------------------------------------
print('Perform redaction')

df[,setdiff(colnames(df),c("characteristic","subcharacteristic"))] <- lapply(df[,setdiff(colnames(df),c("characteristic","subcharacteristic"))],
                                                                             FUN=function(y){roundmid_any(as.numeric(y), to=threshold)})

# Rename columns (output redaction) --------------------------------------------
print("Rename columns for output redaction")

names(df)[names(df) == "total"] <- "total_midpoint6"
names(df)[names(df) == "exposed"] <- "exposed_midpoint6"

# Calculate column percentages -------------------------------------------------

df$Npercent <- paste0(df$total,ifelse(df$characteristic=="All","",
                                      paste0(" (",round(100*(df$total_midpoint6 / df[df$characteristic=="All","total_midpoint6"]),1),"%)")))

df <- df[,c("characteristic","subcharacteristic","Npercent","exposed_midpoint6")]
colnames(df) <- c("Characteristic","Subcharacteristic","N (%) midpoint6 derived","COVID-19 diagnoses midpoint6")

# Save Table 1 -----------------------------------------------------------------
print('Save rounded Table 1')

write.csv(df, paste0("output/extendedtable1_",cohort,"_midpoint6.csv"), row.names = FALSE)