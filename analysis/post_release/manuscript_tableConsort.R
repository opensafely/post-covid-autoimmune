# Load data --------------------------------------------------------------------
print("Load data")

df <- readr::read_csv(path_consort,
                      show_col_types = FALSE)

# Filter data ------------------------------------------------------------------
print("Filter data")

df$removed <- NULL

# Pivot table ------------------------------------------------------------------
print("Pivot table")

df <- df %>%
  dplyr::group_by(Description,cohort) %>%
  dplyr::mutate(N = min(N_midpoint6)) %>%
  dplyr::ungroup() %>%
  unique()

df <- tidyr::pivot_wider(df, 
                         names_from = "cohort",
                         values_from = c("N_midpoint6"))

# Save table -------------------------------------------------------------------
print("Save table")

readr::write_csv(df, "output/post_release/tableConsort.csv", na = "-")