library(readr)
library(dplyr)
library(igraph)
library(threejs)
library(qgraph)

# Data
datadir <- file.path("C:/", "data", "poltweets")
datapath <- file.path(datadir, "climate-tweets_network.csv")

df <- read_csv(datapath)

# Top climate words = klima/klimaet, klimalov, klimakrisen, klimahandling, klimapolitik

climate_words <- c('klima', 'klimalov', 'klimakrisen', 'klimahandling', 'klimapolitik')

extra_stops <- c('.@venstredk-ministre', 'mio.', 'pct.', 'uge', 'stedet', 'forhånd',
                 'gade', 'aften', 'aller', 'april', 'artikel', 'blog', 'billede',
                 'batter', 'blok', 'energi-', 'indhold', 'ord', 'o.a.', 'slut', 
                 'stop', 'å', 'ha', 'ja', 'sider', 'starten', 'start', 'dele')

create_climate_nw <- function(df, word){

  words_keep = df %>%
    filter(climate_tokens == word) %>%
    group_by(tokens) %>%
    summarise(count = n()) %>%
    arrange(desc(count)) %>%
    .$tokens
  words_keep = words_keep[1:50]
  
  df_nw = df %>%
    filter(climate_tokens == word) %>%
    filter(tokens != word,
           tokens2 != word) %>%
    filter(tokens %in% words_keep,
           tokens2 %in% words_keep) %>%
    filter(!(tokens %in% extra_stops),
           !(tokens2 %in% extra_stops)) %>%
    select(tokens, tokens2) %>%
    group_by(tokens, tokens2) %>%
    summarise(weight = n())
  
  # Data cleanup
  for (token in df_nw$tokens){
    cooccs = df_nw %>%
      filter(tokens == token) %>%
      .$tokens2
    
    for (coocc in cooccs){
      df_nw = df_nw %>%
        filter(!(tokens == coocc & tokens2 == token))
    }
  }
  
  qgraph(df_nw, arrows = FALSE, 
         borders = TRUE, 
         color = "white", 
         label.scale = FALSE,
         theme = "Reddit",
         title = paste0("CO-OCCURENCES FOR \"", word, "\""),
         title.cex = 2,
         directed = FALSE,
         layout = "spring")
    
}

create_climate_nw(df = df, word = climate_words[2])


# Andre plotting ting
graph <- graph_from_data_frame(select(df_nw, climate_tokens, tokens), directed = TRUE)

labels <- V(graph)
degrees <- as.numeric(degree(graph, normalized = FALSE, mode = "in"))

plot(graph, vertex.size = degrees)

graphjs(graph, vertex.size = degrees * 10, vertex.label = names(labels))

