library(ggplot2)
library(ggthemes)

df <- read.csv(file="/home/developer/PycharmProjects/journal_graphs/data/processed/site_counts.tsv",
               header = TRUE,
               sep="\t")
df$site <- factor(df$site, levels = df$site[order(df$count,)])

p<-ggplot(data=df, aes(x=site, y=count)) +
  theme_bw() +
  theme_solarized() +
  scale_colour_solarized('blue') + 
  theme(axis.text.x = element_text(face = "bold", color = "#993333", 
                                     size = 10, angle = 90)) +
  geom_bar(stat="identity")
p