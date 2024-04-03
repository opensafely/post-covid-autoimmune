# Load libraries ---------------------------------------------------------------
print('Load libraries')

library(magrittr)

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

# Select variables of interest -------------------------------------------------

df <- df[grepl("cov_bin_|cov_num_|exposed|sub_bin_|exp_date_", names(df))] 

# Remove columns ---------------------------------------------------------------

df <- df[!grepl("_diabetes_type1_|_diabetes_type2_|_diabetes_other|_diabetes_gestational|_prediabetes|_contraceptive_pill|_replacement_", names(df))] 

# Remove people with history of COVID-19 ---------------------------------------
print("Remove people with history of COVID-19")

df <- df[df$sub_bin_covid19_confirmed_history==FALSE,]

# Format columns ---------------------------------------------------------------
# dates, numerics, factors, logicals

df$sub_bin_covid19_confirmed_history <- as.factor(df$sub_bin_covid19_confirmed_history) 

# Create exposure indicator ----------------------------------------------------
print("Create exposure indicator")

df$exposed <- !is.na(df$exp_date_covid19_confirmed) 

# Filter data ------------------------------------------------------------------
print("Filter data")

df <- df[,c("exposed",
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
                                       "History of inflammatory bowel disease(combined ulcerative colitis and Crohn's)",
                                       "History of Crohn’s disease",
                                       "History of ulcerative colitis",
                                       "History of celiac disease",
                                       "History of autoimmune gastrointestinal disease / inflammatory bowel disease (Group 4)",
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
                                          "TRUE", "FALSE",
                                          "Missing"),
                               labels = c("All",
                                          "TRUE", "FALSE", 
                                          "Missing")) 

# Sort data --------------------------------------------------------------------
print("Sort data")

df <- df[order(df$subcharacteristic, decreasing = TRUE),]
df <- df[order(df$characteristic),]

# Save Table 1 -----------------------------------------------------------------
print('Save Table 1')

write.csv(df, paste0("output/extendedtable1_part2_",cohort,".csv"), row.names = FALSE)

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
print('Save rounded extended table 1')

write.csv(df, paste0("output/extendedtable1_part2_",cohort,"_midpoint6.csv"), row.names = FALSE)