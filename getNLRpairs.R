#!/usr/bin/env Rscript

args <- commandArgs(trailingOnly = TRUE)

geneinfo = args[1]
nlrids = args[2]
output = args[3]

library(tidyverse)

# read gene location
df.gene.loca = readr::read_table(geneinfo) %>% 
  dplyr::group_by(Chr, `gene.id`) %>% 
  dplyr::mutate(mean.location = mean(gene.start + gene.end)) %>% 
  dplyr::ungroup()

# Determine whether the start of all genes is less than end
df.gene.loca %>% 
  dplyr::mutate(temp = case_when(gene.end > gene.start ~ "yes",
                                 TRUE ~ "no")) -> df.gene.loca.temp
table(df.gene.loca.temp$temp)

# Read NLR-Annotator result ID
nlr.id = readr::read_table(nlrids, col_names = FALSE, comment = "#") %>% 
  magrittr::set_names(c("id"))


# Start to judge whether it is nlr-pairs
df.gene.loca %>% 
  dplyr::filter(mRNA.id %in% nlr.id$id) -> df.nlr.location

all.res = NULL

for (i in unique(df.nlr.location$Chr)) {
  df.nlr.location %>% 
    dplyr::filter(Chr == i) %>% 
    dplyr::arrange(gene.id)-> df.temp
  
  if (nrow(df.temp) >= 2) {
    df.gene.loca %>% 
      dplyr::filter(Chr == i) -> df.gene.loca.2
    
    for (j in 1:(nrow(df.temp)-1)) {
      for (m in (j+1):nrow(df.temp)) {
        df.temp %>% 
          dplyr::filter(gene.id %in% c(df.temp$gene.id[j], df.temp$gene.id[m])) -> df.temp.2
        
        min.end = min(df.temp.2$gene.end)
        max.start = max(df.temp.2$gene.start)
        
        # Determine the number of genes within the interval length of two genes
        df.gene.loca.2 %>% 
          dplyr::mutate(temp1 = case_when(gene.start < min.end ~ "no", TRUE ~ "yes"),
                        temp2 = case_when(gene.end > max.start ~ "no", TRUE ~ "yes")) %>% 
          dplyr::filter(temp1 == "yes",
                        temp2 == "yes") %>% 
          dplyr::filter(!duplicated(gene.id))-> df.temp.3
        
        if (nrow(df.temp.3) <= 2) {
          data.frame(
            gene.1 = df.temp$gene.id[j],
            gene.2 = df.temp$gene.id[m]
          ) %>% 
            rbind(all.res) -> all.res
        }else{
          next
        }
      }
    }
  }else{
    next
  }
}

# merge information
df.nlr.location %>% 
  dplyr::select(1:5) %>% 
  dplyr::distinct_all() -> df.nlr.location.final

all.res %>% 
  dplyr::filter(gene.1 %in% df.nlr.location.final$gene.id,
                gene.2 %in% df.nlr.location.final$gene.id,
                gene.1 != gene.2) %>% 
  dplyr::mutate(temp = paste0(gene.1, gene.2)) %>% 
  dplyr::filter(!duplicated(temp)) %>% 
  dplyr::left_join(df.nlr.location.final, by = c("gene.1" = "gene.id")) %>% 
  dplyr::rename(chr.1 = Chr,
                start.1 = gene.start,
                end.1 = gene.end,
                strand.1 = gene.strand) %>% 
  dplyr::left_join(df.nlr.location.final, by = c("gene.2" = "gene.id")) %>% 
  dplyr::rename(chr.2 = Chr,
                start.2 = gene.start,
                end.2 = gene.end,
                strand.2 = gene.strand) %>% 
  dplyr::select(gene.1, gene.2, 
                chr.1, chr.2, 
                start.1, start.2,
                end.1, end.2, 
                strand.1, strand.2) %>%  
  data.table::fwrite(output, sep = "\t", col.names = TRUE)
