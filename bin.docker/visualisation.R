#!/usr/bin/env Rscript
print(.libPaths())
library(ggplot2)
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) {
  cat("Usage: Rscript script.R <arg1> \n")
  quit(status = 1) }
arg <- as.numeric(args[1])
h1 <- read.csv("heaps.txt", sep="\t", header=F) 
colnames(h1) <- c("a", "b", "pangenome")
valu = 2/arg
str(h1)
pdf("heaps.pdf", width=8, height=6)
ggplot()  + 
  geom_line(aes(x=arg:valu, y=h1$pangenome), color="#E74C3C", linewidth=1.2, alpha=0.85) +
  geom_point(aes(x=arg:valu, y=h1$pangenome), color="#C0392B", size=2.5, alpha=0.9) +
  scale_y_continuous(limits = c(min(h1$pangenome)-1000, max(h1$pangenome)+1000), 
                     labels = scales::comma) +
  scale_x_continuous(labels = scales::number_format(accuracy = 0.01)) +
  labs(    subtitle = "Sample fraction vs pangenome size",
    x = "Fraction of Samples",
    y = "Number of Bases in Paths"  ) +
  theme_minimal(base_size = 14) +
  theme(
    panel.grid.major = element_line(color = "grey90", linewidth = 0.5),
    panel.grid.minor = element_line(color = "grey95", linewidth = 0.3),
    panel.background = element_rect(fill = "white", color = NA),
    plot.background = element_rect(fill = "white", color = NA),
    axis.line = element_line(color = "grey30", linewidth = 0.5),
    axis.text = element_text(color = "grey20", size = 12),
    axis.title = element_text(color = "grey10", size = 14, face = "bold"),
    axis.ticks = element_line(color = "grey30"),
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold", margin = margin(b = 10)),
    plot.subtitle = element_text(hjust = 0.5, size = 11, color = "grey40", margin = margin(b = 15)),
    plot.margin = margin(20, 20, 20, 20),
    legend.position = "none"
  )
dev.off()
