install.packages('VennDiagram')

require(VennDiagram)
# Adopted from Chen and Boutros, 2011 (DOI: 10.1186/1471-2105-12-35)
# If you want to compare three tools
venn.diagram(
  x = list(
    GASTS = c(1:9, 10:12, 13:705, 707:719),
    Procars = c(720:755, 10:12, 13:705, 756:759),
    MGRA = c(760:766, 707:719, 13:705, 756:759)
  ),
  filename = "Common.jpg",
  col = "transparent",
  fill = c("red", "blue", "green"),
  alpha = 0.5,
  main = 'Common', main.cex = 4,
  label.col = c("darkred", "white", "darkblue", "white", "white", "white", "darkgreen"),
  cex = 2.5, 
  fontfamily = "serif",
  fontface = "bold",
  cat.default.pos = "text",
  cat.col = c("darkred", "darkblue", "darkgreen"),
  cat.cex = 2.5,
  cat.fontfamily = "serif",
  cat.dist = c(0.06, 0.06, 0.03),
  cat.pos = 0
);

#If you want to compare 4 tools

venn.diagram(
  x = list(
    I = c(1:60, 61:105, 106:140, 141:160, 166:175, 176:180, 181:205, 206:220),
    IV = c(531:605, 476:530, 336:375, 376:405, 181:205, 206:220, 166:175, 176:180),
    II = c(61:105, 106:140, 181:205, 206:220, 221:285, 286:335, 336:375, 376:405),
    III = c(406:475, 286:335, 106:140, 141:160, 166:175, 181:205, 336:375, 476:530)
  ),
  filename = "quadruple_Venn.tiff",
  col = "black",
  lty = "dotted",
  lwd = 4,
  fill = c("cornflowerblue", "green", "yellow", "darkorchid1"),
  alpha = 0.50,
  label.col = c("orange", "white", "darkorchid4", "white", "white", "white", "white", "white", "darkblue", "white", "white", "white", "white", "darkgreen", "white"),
  cex = 2.5,
  fontfamily = "serif",
  fontface = "bold",
  cat.col = c("darkblue", "darkgreen", "orange", "darkorchid4"),
  cat.cex = 2.5,
  cat.fontfamily = "serif"
);
