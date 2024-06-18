# Load libraries ---------------------------------------------------------------
print('Load libraries')

library(data.table)
library(readr)
library(dplyr)
library(stringr)

# Specify redaction threshold --------------------------------------------------

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

# Identify outcomes ------------------------------------------------------------
print('Identify outcomes')

active_analyses <- readr::read_rds("lib/active_analyses.rds")

outcomes <- gsub("out_date_","",
                 unique(active_analyses[active_analyses$cohort==cohort &
                                          active_analyses$analysis=="main",]$outcome))

# Load Venn data ---------------------------------------------------------------
print('Load Venn data')

venn <- readr::read_rds(paste0("output/venn_",cohort,".rds"))

# rename columns ---------------------------------------------------------------
print("Rename temporary outcomes columns")

venn <- venn %>%
  rename_with(~ str_replace(., "tmp_out_date_hashimoto_thyroiditis_", "tmp_out_date_hashimoto_")) %>%
  rename_with(~ str_replace(., "tmp_out_date_longit_myelitis_", "tmp_out_date_long_myelitis_")) %>%
  rename_with(~ str_replace(., "tmp_out_date_pernicious_anaemia_", "tmp_out_date_pern_anaemia_")) %>%
  rename_with(~ str_replace(., "tmp_out_date_multiple_sclerosis_", "tmp_out_date_ms_")) %>%
  rename_with(~ str_replace(., "tmp_out_date_myasthenia_gravis_", "tmp_out_date_myasthenia_")) %>%
  rename_with(~ str_replace(., "tmp_out_date_iga_vasculitis_", "tmp_out_date_iga_vasc_")) %>%
  rename_with(~ str_replace(., "tmp_out_date_undiff_eia", "tmp_out_date_undiff_eia_snomed")) %>%
  rename_with(~ str_replace(., "tmp_out_date_as", "tmp_out_date_as_snomed"))

# Create empty output table ----------------------------------------------------
print('Create empty output table')

df <- data.frame(outcome = character(),
                 only_ctv = numeric(),
                 only_snomed = numeric(),
                 only_hes = numeric(),
                 only_death = numeric(),
                 snomed_ctv = numeric(),
                 snomed_hes = numeric(),
                 snomed_death = numeric(),
                 ctv_hes = numeric(),
                 ctv_death  = numeric(),
                 hes_death = numeric(),
                 snomed_ctv_hes_death = numeric(),
                 total_ctv = numeric(),
                 total_snomed = numeric(),
                 total_hes = numeric(),
                 total_death = numeric(),
                 total = numeric(),
                 error = character(),
                 stringsAsFactors = FALSE)

# Populate Venn table for each outcome -----------------------------------------
print('Populate Venn table for each outcome')

for (outcome in outcomes) {
  
  print(paste0("Outcome: ", outcome))
  
  # Load model input data ------------------------------------------------------
  print('Load model input data')
  
  model_input <- readr::read_rds(paste0("output/model_input-cohort_",cohort,"-main-",outcome,".rds"))  
  model_input <- model_input[!is.na(model_input$out_date),c("patient_id","out_date")]
  
  if (nrow(model_input)>0) {
    
    # Filter Venn data based on model input --------------------------------------
    print('Filter Venn data based on model input')
    
    tmp <- venn[venn$patient_id %in% model_input$patient_id,
                c("patient_id",colnames(venn)[grepl(outcome,colnames(venn))])]
    
    colnames(tmp) <- gsub(paste0("tmp_out_date_",outcome,"_"),"",colnames(tmp))
    
    # Identify and add missing columns -------------------------------------------
    print('Identify and add missing columns')
    
    complete <- data.frame(patient_id = tmp$patient_id,
                           ctv = as.Date(NA),
                           snomed = as.Date(NA),
                           hes = as.Date(NA),
                           death = as.Date(NA))
    
    complete[,setdiff(colnames(tmp),"patient_id")] <- NULL
    notused <- NULL
    
    if (ncol(complete)>1) {
      tmp <- merge(tmp, complete, by = c("patient_id"))
      notused <- setdiff(colnames(complete),"patient_id")
    }
    
    # Calculate the number contributing to each source combination ---------------
    print('Calculate the number contributing to each source combination')
    
    tmp$snomed_contributing <- !is.na(tmp$snomed) & 
      is.na(tmp$ctv) &
      is.na(tmp$hes) & 
      is.na(tmp$death)
    
    tmp$ctv_contributing <- is.na(tmp$snomed) & 
      !is.na(tmp$ctv) &
      is.na(tmp$hes) & 
      is.na(tmp$death)
    
    tmp$hes_contributing <- is.na(tmp$snomed) & 
      is.na(tmp$ctv) &
      !is.na(tmp$hes) & 
      is.na(tmp$death)
    
    tmp$death_contributing <- is.na(tmp$snomed) & 
      is.na(tmp$ctv) &
      is.na(tmp$hes) & 
      !is.na(tmp$death)
    
    tmp$snomed_hes_contributing <- !is.na(tmp$snomed) & 
      is.na(tmp$ctv) &
      !is.na(tmp$hes) & 
      is.na(tmp$death)
    
    tmp$snomed_ctv_contributing <- !is.na(tmp$snomed) & 
      !is.na(tmp$ctv) &
      is.na(tmp$hes) & 
      is.na(tmp$death)
    
    tmp$snomed_death_contributing <- !is.na(tmp$snomed) & 
      is.na(tmp$ctv) &
      is.na(tmp$hes) & 
      !is.na(tmp$death)
    
    tmp$hes_death_contributing <- is.na(tmp$snomed) & 
      is.na(tmp$ctv) &
      !is.na(tmp$hes) & 
      !is.na(tmp$death)
    
    tmp$ctv_hes_contributing <- is.na(tmp$snomed) & 
      !is.na(tmp$ctv) &
      !is.na(tmp$hes) & 
      is.na(tmp$death)
    
    tmp$ctv_death_contributing <- is.na(tmp$snomed) & 
      !is.na(tmp$ctv) &
      is.na(tmp$hes) & 
      !is.na(tmp$death)
    
    tmp$snomed_ctv_hes_death_contributing <- !is.na(tmp$snomed) & 
      !is.na(tmp$ctv) &
      !is.na(tmp$hes) & 
      !is.na(tmp$death)
    
    # Record the number contributing to each source combination ------------------
    print('Record the number contributing to each source combination')
    
    df[nrow(df)+1,] <- c(outcome,
                         ctv_snomed = nrow(tmp %>% filter(ctv_contributing==T)),
                         only_snomed = nrow(tmp %>% filter(snomed_contributing==T)),
                         only_hes = nrow(tmp %>% filter(hes_contributing==T)),
                         only_death = nrow(tmp %>% filter(death_contributing==T)),
                         snomed_ctv = nrow(tmp %>% filter(snomed_ctv_contributing==T)),
                         snomed_hes = nrow(tmp %>% filter(snomed_hes_contributing==T)),
                         snomed_death = nrow(tmp %>% filter(snomed_death_contributing==T)),
                         ctv_hes = nrow(tmp %>% filter(ctv_hes_contributing==T)),
                         ctv_death = nrow(tmp %>% filter(ctv_death_contributing==T)),
                         hes_death = nrow(tmp %>% filter(hes_death_contributing==T)),
                         snomed_ctv_hes_death = nrow(tmp %>% filter(snomed_ctv_hes_death_contributing==T)),
                         total_snomed = nrow(tmp %>% filter(!is.na(snomed))),
                         total_ctv = nrow(tmp %>% filter(!is.na(ctv))),
                         total_hes = nrow(tmp %>% filter(!is.na(hes))),
                         total_death = nrow(tmp %>% filter(!is.na(death))),
                         total = nrow(tmp),
                         error = "")
    
    # Replace source combinations with NA if not in study definition -----------
    print('Replace source combinations with NA if not in study definition')
    
    source_combos <- c("only_snomed", "only_ctv","only_hes","only_death",
                       "snomed_ctv", "snomed_hes","snomed_death", "ctv_hes", "ctv_death","hes_death",
                       "snomed_ctv_hes_death",
                       "total_snomed", "total_ctv", "total_hes","total_death")
    source_consid <- source_combos
    
    if (!is.null(notused)) {
      for (i in notused) {
        
        # Add variables to consider for Venn plot to vector
        source_consid <- source_combos[!grepl(i,source_combos)]
        
        # Replace unused sources with NA in summary table
        for (j in setdiff(source_combos,source_consid)) {
          df[df$outcome==outcome,j] <- NA
        }
        
      }
    }
    
  } else {
    
    # Record empty outcome -----------------------------------------------------
    print('Record empty outcome')
    
    df[nrow(df)+1,] <- c(outcome,
                         only_snomed = NA,
                         only_ctv = NA,
                         only_hes = NA,
                         only_death = NA,
                         snomed_ctv = NA,
                         snomed_hes = NA,
                         snomed_death = NA,
                         ctv_hes = NA,
                         ctv_death = NA,
                         hes_death = NA,
                         snomed_ctv_hes_death = NA,
                         total_snomed = NA,
                         total_ctv = NA,
                         total_hes = NA,
                         total_death = NA,
                         total = NA,
                         error = "No outcomes in model input")
    
    
  }
  
}

# Remove grouped and composite outcomes ----------------------------------------
print("Remove grouped and composite outcomes")

df <- df[!grepl("grp[0-9]|composite_ai", df$outcome),]

# Character to numeric ---------------------------------------------------------
print("Character to numeric")

df <- df %>%
  mutate_at(vars(matches("snomed|ctv|hes|death|total")),function(x) as.numeric(as.character(x)))

# Create grouped outcomes contribution counts function -------------------------
print("Create function for grouped and composite outcomes")

df_grp <- function(df){

  # Create group variable
  df <- as_tibble(df) %>%
    mutate(grp = case_when(
      outcome %in% c("ra","undiff_eia","psoa","axial") ~  "grp1_ifa", 
      outcome %in% c("sle","sjs","sss","im","mctd","as") ~ "grp2_ctd",
      outcome %in% c("psoriasis","hs") ~ "grp3_isd", 
      outcome %in% c("ibd","crohn","uc","celiac") ~ "grp4_agi_ibd", 
      outcome %in% c("addison","grave","hashimoto") ~ "grp5_atv", 
      outcome %in% c("anca","gca","iga_vasc","pmr") ~ "grp6_trd", 
      outcome %in% c("immune_thromb","pern_anaemia","apa","aha") ~ "grp7_htd", 
      outcome %in% c("glb","ms","myasthenia","long_myelitis","cis") ~ "grp8_ind"))
  
  # Summarise by group
  df <- df %>%
    group_by(grp) %>%
    summarise_if(is.numeric, sum, na.rm = T) %>%
    ungroup()
  
  # Summarise composite autoimmune components 
  composite_ai <- df %>%
    summarise_if(is.numeric, sum, na.rm = T)
  
  # Add outcome (grp) column and name 
  composite_ai$grp <- "composite_ai"

  # Bind grouped and composite dataframes
  df_grp <- rbind(df, composite_ai)
  
  # add error column
  df_grp$error <- "" #NA
  
  # Rename column
  df_grp <- rename(df_grp, outcome = grp)
  
}

# Apply function
df_full <- df_grp(df)

# Bind original df with grouped df
df <- bind_rows(df, df_full)

# Record cohort ----------------------------------------------------------------
print('Record cohort')

df$cohort <- cohort

# Save Venn data -----------------------------------------------------------------
print('Save Venn data')

write.csv(df, paste0("output/venn_",cohort,".csv"), row.names = FALSE)

# Perform redaction ------------------------------------------------------------
print('Perform redaction')

df[,setdiff(colnames(df),c("outcome"))] <- lapply(df[,setdiff(colnames(df),c("outcome"))],
                                                  FUN=function(y){roundmid_any(as.numeric(y), to=threshold)})

# Rename columns (output redaction) --------------------------------------------

names(df)[names(df) == "only_snomed"] <- "only_snomed_midpoint6"
names(df)[names(df) == "only_ctv"] <- "only_ctv_midpoint6"
names(df)[names(df) == "only_hes"] <- "only_hes_midpoint6"
names(df)[names(df) == "only_death"] <- "only_death_midpoint6"
names(df)[names(df) == "snomed_hes"] <- "snomed_hes_midpoint6"
names(df)[names(df) == "snomed_ctv"] <- "snomed_ctv_midpoint6"
names(df)[names(df) == "snomed_death"] <- "snomed_death_midpoint6"
names(df)[names(df) == "ctv_hes"] <- "ctv_hes_midpoint6"
names(df)[names(df) == "hes_death"] <- "hes_death_midpoint6"
names(df)[names(df) == "ctv_death"] <- "ctv_death_midpoint6"
names(df)[names(df) == "snomed_ctv_hes_death"] <- "snomed_ctv_hes_death_midpoint6"

# Recalculate sources totals and total midpoint6 derived column ----------------
print("Recalculate total (midpoint6 derived) column")

df$total_snomed_midpoint6_derived <- rowSums(df[,c("only_snomed_midpoint6", "snomed_ctv_midpoint6", "snomed_hes_midpoint6", "snomed_death_midpoint6", "snomed_ctv_hes_death_midpoint6")], na.rm = T)

df$total_ctv_midpoint6_derived <- rowSums(df[,c("only_ctv_midpoint6", "snomed_ctv_midpoint6", "ctv_hes_midpoint6", "ctv_death_midpoint6", "snomed_ctv_hes_death_midpoint6")], na.rm = T)

df$total_hes_midpoint6_derived <- rowSums(df[,c("only_hes_midpoint6", "snomed_hes_midpoint6",  "ctv_hes_midpoint6", "hes_death_midpoint6", "snomed_ctv_hes_death_midpoint6")], na.rm = T)

df$total_death_midpoint6_derived <- rowSums(df[,c("only_death_midpoint6", "snomed_death_midpoint6", "hes_death_midpoint6", "ctv_death_midpoint6", "snomed_ctv_hes_death_midpoint6")], na.rm = T)

df$total_midpoint6_derived <- rowSums(df[,c("only_ctv_midpoint6", "only_snomed_midpoint6", "only_hes_midpoint6", "only_death_midpoint6",
                                            "ctv_hes_midpoint6", "ctv_death_midpoint6", "hes_death_midpoint6",
                                            "snomed_ctv_midpoint6", "snomed_hes_midpoint6", "snomed_death_midpoint6", "snomed_ctv_hes_death_midpoint6")], na.rm = T)

# Remove total columns ---------------------------------------------------------
print("Remove total columns")

df$total_ctv <- NULL
df$total_snomed <- NULL
df$total_hes <- NULL
df$total_death <- NULL
df$total <- NULL

# Relocate columns -------------------------------------------------------------
print("Relocate columns following empty df")

df <- df %>%
  relocate(c(total_snomed_midpoint6_derived, total_ctv_midpoint6_derived, total_hes_midpoint6_derived, total_death_midpoint6_derived, total_midpoint6_derived), 
           .before = error)

# Save rounded Venn data -------------------------------------------------------
print('Save rounded Venn data')

write.csv(df, paste0("output/venn_",cohort,"_midpoint6.csv"), row.names = FALSE)