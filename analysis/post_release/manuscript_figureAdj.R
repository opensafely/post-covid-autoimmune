# Load data --------------------------------------------------------------------
print("Load data")

df <- readr::read_csv(path_model_output,
                      show_col_types = FALSE)

# Filter data ------------------------------------------------------------------
print("Filter data")

df <- df[df$analysis=="main" & 
           grepl("day",df$term),
         c("cohort","outcome","outcome_time_median","model","term","hr","conf_low","conf_high")]

df <- df[df$term!="days_pre",]

# Make columns numeric ---------------------------------------------------------
print("Make columns numeric")

df <- df %>% 
  dplyr::mutate_at(c("outcome_time_median","hr","conf_low","conf_high"), as.numeric)

# Add plot labels --------------------------------------------------------------
print("Add plot labels")

plot_labels <- readr::read_csv("lib/plot_labels.csv", show_col_types = FALSE)

df <- merge(df, plot_labels, by.x = "outcome", by.y = "term", all.x = TRUE)
df <- dplyr::rename(df, "outcome_label" = "label")

# Order outcomes ---------------------------------------------------------------
print("Order outcomes")

df$outcome_label <- factor(df$outcome_label,
                           levels = c("Reumatoid arthritis",
                                      "Undifferentiated inflamatory arthritis",
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
                                      "immunoglobulin a (IgA) vasculitis",
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
                                      "Composite autoimmune"))

# Plot data --------------------------------------------------------------------
print("Plot data")

ggplot2::ggplot(data = df,
                mapping = ggplot2::aes(x = outcome_time_median, y = hr, color = cohort)) +
  ggplot2::geom_hline(mapping = ggplot2::aes(yintercept = 1), colour = "#A9A9A9") +
  ggplot2::geom_point(position = ggplot2::position_dodge(width = 0)) +
  ggplot2::geom_errorbar(mapping = ggplot2::aes(ymin = conf_low, 
                                                ymax = conf_high,  
                                                width = 0), 
                         position = ggplot2::position_dodge(width = 0)) +
  ggplot2::geom_line(position = ggplot2::position_dodge(width = 0), ggplot2::aes(linetype=model)) +
  ggplot2::scale_y_continuous(lim = c(0.5,8), breaks = c(0.5,1,2,4,8), trans = "log") +
  ggplot2::scale_x_continuous(lim = c(0,511), breaks = seq(0,511,56), labels = seq(0,511,56)/7) +
  ggplot2::scale_linetype_manual(values=c("solid", "dashed"), 
                                 breaks = c("mdl_max_adj", "mdl_age_sex"),
                                 labels = c("Maximally adjusted","Age- and sex- adjusted")) +
  ggplot2::scale_color_manual(breaks = c("prevax", "vax", "unvax"),
                              labels = c("Pre-vaccination (Jan 1 2020 - Dec 14 2021)",
                                         "Vaccinated (Jun 1 2021 - Dec 14 2021)",
                                         "Unvaccinated (Jun 1 2021 - Dec 14 2021)"),
                              values = c("#d2ac47", "#58764c", "#0018a8")) +
  ggplot2::labs(x = "\nWeeks since COVID-19 diagnosis", y = "Hazard ratio and 95% confidence interval\n") +
  ggplot2::guides(color=ggplot2::guide_legend(ncol = 1, byrow = TRUE),
                  linetype=ggplot2::guide_legend(ncol = 1, byrow = TRUE)) +
  ggplot2::theme_minimal() +
  ggplot2::theme(panel.grid.major.x = ggplot2::element_blank(),
                 panel.grid.minor = ggplot2::element_blank(),
                 panel.spacing.x = ggplot2::unit(0.5, "lines"),
                 panel.spacing.y = ggplot2::unit(0, "lines"),
                 legend.key = ggplot2::element_rect(colour = NA, fill = NA),
                 legend.title = ggplot2::element_blank(),
                 legend.position="bottom",
                 plot.background = ggplot2::element_rect(fill = "white", colour = "white")) +
  ggplot2::facet_wrap(outcome_label~., ncol = 2)

# Save plot --------------------------------------------------------------------
print("Save plot")

ggplot2::ggsave("output/post_release/figureAdj.png", 
                height = 297, width = 210, 
                unit = "mm", dpi = 600, scale = 0.8)