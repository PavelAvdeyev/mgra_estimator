dist <- read.csv('results_project.csv', dec = ',', sep = ';' )
View(dist)

library(ggplot2)

ggplot(dist, aes(x= name, y = time), 
       las = 2) + geom_bar(stat = 'identity',
                           fill = 'slateblue')  + ylim(0,400) + ggtitle('GASTS') +
  xlab('') + ylab('')  + 
  theme(axis.text.x = element_text(angle = 60, 
                                   hjust = 1, colour = 'black', face = 'bold'), 
        plot.title = 
          element_text(size = 16, face = 'bold'))
