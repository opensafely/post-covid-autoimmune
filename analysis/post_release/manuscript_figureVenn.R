# Create directory -------------------------------------------------------------
print("Create directory")

fs::dir_create(here::here("output/post_release/", "figure_venn"))

# Load data --------------------------------------------------------------------
print("Load data")

df <- readr::read_csv(path_venn,
                      show_col_types = FALSE)

colnames(df) <- gsub("_midpoint6","",colnames(df))

# Select single outcomes -------------------------------------------------------
print("Select single outcomes")

df <- df[!grepl("grp[0-9]|composite_ai", df$outcome),]

# Select grouped outcomes ------------------------------------------------------
print("Select grouped outcomes")

# df <- df[grepl("grp[0-9]|composite_ai", df$outcome),]

# Replace NA values with zeros -------------------------------------------------
print("Replace NA values with zeros")

df[is.na(df)] <- 0

# Create Venn for each outcome/cohort combo ------------------------------------
print("Create Venn for each outcome/cohort combo")

for(i in 1:nrow(df)) {
  
  paste0("Outcome: ", df[i,]$outcome,"; Cohort: ",df[i,]$cohort)
  
  venn.plot <- VennDiagram::draw.triple.venn(
    area1 = df[i,]$total_snomed + df[i,]$total_ctv, 
    area2 = df[i,]$total_hes, 
    area3 = df[i,]$total_death,
    n12 = df[i,]$snomed_hes + df[i,]$ctv_hes + df[i,]$snomed_ctv_hes_death,
    n23 = df[i,]$hes_death + df[i,]$snomed_ctv_hes_death, 
    n13 = df[i,]$snomed_death + df[i,]$ctv_death + df[i,]$snomed_ctv_hes_death, 
    n123 = df[i,]$snomed_ctv_hes_death,
    category = c("Primary care","Secondary care","Death registry"),
    col = "white",
    fill = c("#1b9e77","#d95f02","#7570b3"),
    print.mode = c("raw", "percent"),
    sigdigs = 3
  )
  
  grid.draw(venn.plot)
  grid.newpage()
  tiff(paste0("output/post_release/figure_venn/figure_venn-",df[i,]$cohort,"-",df[i,]$outcome,".tiff"), compression = "lzw")
  grid.draw(venn.plot)
  dev.off()
  
}