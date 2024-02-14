# Specify parameters -----------------------------------------------------------
print('Specify parameters')

perpeople <- 100000 # per X people

# Load data --------------------------------------------------------------------
print('Load data')

df <- read.csv("output/post_release/lifetables_compiled.csv")

# Filter data ------------------------------------------------------------------
print("Filter data")

df <- df[df$aer_age=="overall" &
           df$aer_sex=="overall" &
           df$analysis=="main" & 
           df$days==196,]

# Add plot labels --------------------------------------------------------------
print("Add plot labels")

plot_labels <- readr::read_csv("lib/plot_labels.csv",
                               show_col_types = FALSE)

df <- merge(df, plot_labels, by.x = "outcome", by.y = "term", all.x = TRUE)
df <- dplyr::rename(df, "outcome_label" = "label")

# Format data ------------------------------------------------------------------
print("Format data")

df$excess_risk <- round(df$cumulative_difference_absolute_excess_risk*perpeople)
df <- df[,c("outcome_label","cohort","excess_risk")]

# Pivot table ------------------------------------------------------------------
print("Pivot table")

df <- tidyr::pivot_wider(df, 
                         names_from = "cohort",
                         values_from = c("excess_risk"))

# Order outcomes ---------------------------------------------------------------
print("Order outcomes")

df$outcome_label <- factor(df$outcome_label,
                           levels = c(c("Rheumatoid arthritis",
                                        "Undifferentiated inflammatory arthritis",
                                        "Psoriatic arthritis",
                                        "Axial spondyloarthritis",
                                        "Inflammatory arthritis (Group 1)", # group 1
                                        "Systematic lupus erythematosus",
                                        "Sjogren’s syndrome",
                                        "Systemic sclerosis/scleroderma",
                                        "Inflammatory myositis/polymyositis/dermatolomyositis",
                                        "Mixed connective tissue disease",
                                        "Antiphospholipid syndrome",
                                        "Connective tissue disorders (Group 2)", # group 2
                                        "Psoriasis",
                                        "Hydradenitis suppurativa",
                                        "Inflammatory skin disease (Group 3)", # group 3
                                        "Crohn’s disease",
                                        "Ulcerative colitis",
                                        "Celiac disease",
                                        "Inflammatory bowel disease (combined ulcerative colitis and Crohn's)",
                                        "Autoimmune gastrointestinal disease / Inflammatory bowel disease (Group 4)", # group 4
                                        "Addison’s disease",
                                        "Grave’s disease",
                                        "Hashimoto’s thyroiditis",
                                        "Thyroid diseases (Group 5)", # group 5
                                        "Antineutrophilic cytoplasmic antibody (ANCA)-associated",
                                        "Giant cell arteritis",
                                        "Immunoglobulin A (IgA) vasculitis",
                                        "Polymyalgia rheumatica (PMR)",
                                        "Autoimmune vasculitis (Group 6)", # group 6
                                        "Immune thrombocytopenia (formerly known as idiopathic thrombocytopenic purpura)",
                                        "Pernicious anaemia",
                                        "Aplastic anaemia",
                                        "Autoimmune haemolytic anaemia",
                                        "Hematologic diseases (Group 7)", # group 7
                                        "Guillain-Barré",
                                        "Multiple sclerosis",
                                        "Myasthenia gravis",
                                        "Longitudinal myelitis",
                                        "Clinically isolated syndrome",
                                        "Inflammatory neuromuscular disease (Group 8)", # group 8
                                        "Composite autoimmune")))
                           
# Tidy table -------------------------------------------------------------------
print("Tidy table")
                           
df <- df[order(df$outcome_label),
         c("outcome_label","prevax","vax","unvax")]
                           
# Save table -------------------------------------------------------------------
print("Save table")
                           
readr::write_csv(df, "output/post_release/tableAER.csv", na = "-")