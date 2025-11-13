
library(tximport)
library(GenomicFeatures)
library(ggplot2)
library(DESeq2)
library(pheatmap)
library(RColorBrewer)
library(org.Hs.eg.db)
library(openxlsx)
library(dplyr)

#------------------------------------------------------------------------------
#
# README !!!
# W pliku są zrobione wszystkie zadania. Znajdują się w nim także moje
# komentarze, podzielone na
# (PL)* - zapytanie: Czy dobrze to rozumiem
# (PL)** sugestia: co mogło być skomentowane na zajęciach - nie zwróciłem uwagi
# / nie było wspomnanie i potem szukałem  
# (ENG)*** sugestia: co mogło by się pojawić w kodzie - nie było dla mnie od razu
# oczywiste - pierwszy kontakt z funkcjami / analizami
# jeżeli przy komentarzu nie ma * to są to moje notatki w skrypcie, nieistotne
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Working sheet for DESeq2 practice
# Write down code according to instructions. Follow DESeq2 vignette for help:
# https://bioconductor.org/packages/devel/bioc/vignettes/DESeq2/inst/doc/DESeq2.html
#------------------------------------------------------------------------------
#______________________________________________________________________________
#
# 1. Setting working directory and reading files.
#______________________________________________________________________________

# Function for importing RSEM data, changing transcript counts to gene counts
# based on annotation, importing it to a txi object

import_2_txi = function(dir, gtf, exclude_samples = NULL) {
  
  # Set directory, extract file paths and sample names
  samples = list.files(dir, pattern = "isoforms.results")
  
  # Exclude specified samples if any
  if (!is.null(exclude_samples)) {
    samples = setdiff(samples, exclude_samples)
  }
  
  # Prepare file paths and set sample names
  files = file.path(dir, samples)
  names(files) = sub(".isoforms.results", "", samples)
  
  # Make a Txdb object from genome annotation used for mapping
  txdb = makeTxDbFromGFF(gtf)
  k = keys(txdb, keytype = "TXNAME")
  tx2gene = AnnotationDbi::select(txdb, k, "GENEID", "TXNAME")
  
  # Import RSEM output on transcript level as gene counts using tx2gene to avoid 
  # zero length estimation for some genes
  txi = tximport(files, type = "rsem", txIn = TRUE, txOut = FALSE,
                  tx2gene = tx2gene)
  
  return(txi)
}

#==============================================================================
# 1) Set working directory

getwd() # ustawiona na moje użytkownika ~ "/mnt/chr11/Data/TSG/studenci/ms488923"

# 2) Use import_2_txi function above to import RSEM files as a txi object
# (it will take a little while). Specify directory to the RSEM files (dir) and
# directory to the annotation file (gtf).
#______________________________________________________________________________
#
# Cel 
# (import_2_txi)
# Przygotowujemy dane do analizy 
# `makeTxDbFromGFF` - jest to obiekt który przechowuje adnotacje transkryptów
# `keys` - wyciąga identyfikatory 
# `AnnotationDbi` - tabela zawierająca informacje gen - id transkryptu 
# `tximport` - odpowiada za obrobienie danych w celu przygotowania do analizy
# - zliczenie count'ów, długości, zapobiega 
#
# (DESeqDataSetFromTximport)
# Funkcja ta tworzy obiekt który zawiera informacje o eksperymencie (metadane)
# oraz macierze zliczeń i informacje genach. Jest ważna ponieważ będziemy się nią
# Posługiwać przez wszystkie analizy 
# 
# 
# Teoria**  
# - Komenatrz dotyczący funkcji import_2_txi, bo tam można by omówić po kolei co 
# robi, żeby zrozumieć jak takie obiekty są skonstruowane, +- jak działają, 
# jak problemy się pojawiają i co one rozwiązują. Też że zmienia się format.
# - Skomentował bym też `DESeqDataSetFromTximport`, ponieważ struktura danych tego
# obiektu potem jest wszędzie używana i trzeba się z nią zapoznać 
#
# # Kod 
# chcemy skorzystać z `DESeqDataSetFromTximport`, który łączy nam zsumowane odczyty
# (txi), oraz metadane (colData) 
# factor - tworzy nam kolumne z danymi kategorycznymi, na poszczególne klasy 
# colData.- tworzym df z metadanymi, poniea
#______________________________________________________________________________

path_files = '/mnt/chr11/Data/TSG/Public/lab4'
path_addnotation = 'labs3/files/hg38.ncbiRefSeq.gtf.gz'
txi = import_2_txi(
  dir=path_files, 
  gtf=path_addnotation
  )

#______________________________________________________________________________
#
# 2. Creating a dds object
#______________________________________________________________________________
#==============================================================================
# creating table with metadata - probe | condition | batch *** 
# 1) Create coldata: this is a data frame with sample names as row names and
#   independent variables in the columns
# a) Use colnames on txi$counts to see sample names
sample_names = colnames(txi$counts)
# b) Use the sample names to create a factor "condition".
#    You can use the rep() function. Check ?rep for details.
condition = factor(rep(c("CCCP", "Control", "Sucrose", "Torin1"), each=3))

# c) Create a factor for replicate number — these can be numeric values 
#    stored as character variables, e.g. "1" or "rep1"
replicate = factor(rep(c('rep1', 'rep2', 'rep3'), times=4))

# b)* Instead of manually creating the factors, try using strsplit() on sample 
#     names. Check the structure of the output.
# generalnie tak się powinno robić bo pozwala na automatyzacje
# UWAGA - trzeba dać levels - jak nie ma controlnej jako pierwszej to
# DESeqDataSetFromTximport nie znormalizuje poprawnie danych (dokumentacja) 
parts = strsplit(sample_names, "_")
condition = factor(sapply(parts, `[`, 1), levels = c("Control", "CCCP", "Sucrose", "Torin1"))  
replicate = factor(sapply(parts, '[', 2), levels = c("rep1", "rep2", "rep3"))
print(replicate)

# c) Create a data frame coldata with condition and replicate factors as 
#    columns with the same names. Add sample names as row names.
coldata = data.frame(
  condition = condition,
  replicate = replicate,
  row.names = sample_names
)


# 2) Use DESeqDataSetFromTximport to create a DESeqDataSet.
#    Include both design variables, but condition is more important.
dds = DESeqDataSetFromTximport(
  txi = txi,
  colData = coldata,
  design = ~ condition + replicate
)

# 3) Use relevel to correct the reference level of condition to "Control"
dds$condition = relevel(dds$condition, ref = "Control")

#______________________________________________________________________________
#
# 3. Variance stabilizing transformation and visualization 
#______________________________________________________________________________

# Function to plot row standard deviations versus row means (or rank of means) 
# for a numeric matrix.
# Inspired by vsn::meanSdPlot, simplified for direct use on assay(vsd) matrices.

meanSdPlot = function(x, ranks = TRUE, 
                       xlab = ifelse(ranks, "rank(mean)", "mean"),
                       ylab = "sd", bins=50) {
  n = nrow(x)
  px   = rowMeans(x, na.rm = TRUE)
  py   = sqrt(rowVars(x, mean = px, na.rm = TRUE))
  rpx  = rank(px, na.last = FALSE, ties.method = "random")
  
  ## run median with centers at dm, 2*dm, 3*dm,... and width 2*dm
  dm        = 0.025
  midpoints = seq(dm, 1-dm, by = dm)
  within    = function(x, x1, x2) { (x >= x1) & (x <= x2) }
  mediwind  = function(mp) median(py[within(rpx/n, mp - 2*dm, mp + 2*dm)], 
                                  na.rm = TRUE)
  rq.sds    = sapply(midpoints, mediwind)
  
  res = if(ranks) {
    list(rank = midpoints*n, sd = rq.sds, px = rpx, py = py)
  } else {
    list(quantile = quantile(px, probs = midpoints, na.rm = TRUE), 
         sd = rq.sds, px = px, py = py)
  }
  
  fmt = function() function(x) format(round(x, 0), nsmall = 0L, 
                                      scientific = FALSE)
  
  res$gg = ggplot(data.frame(px = res$px, py = res$py),
                  aes_string(x = "px", y = "py")) + xlab(xlab) + ylab(ylab) +
    geom_hex(bins = bins) +
    scale_fill_gradient(name = "count", trans = "log", labels = fmt()) + 
    geom_line(aes_string(x = "x", y = "y"),
              data = data.frame(x = res[[1]], y = res$sd), color = "red")
  
  print(res$gg)
}

#==============================================================================
#______________________________________________________________________________
# 
#
# 1)* 
# Wstęp teoretyczny  
# vst (variance stabilizing transformation) jest to transformacja oparta na 
# negatywnym modelu dwumianowym (nie mogę pisać tutaj tex'a więc mówię w skrócie)
# chodzi o to, że chcemy uzyskać interpretowalny operator wariancji. Jednak okazuje
# się, że w teori operatory rozkładu zliczeńe wynoszą odpowiednio E(X) = lambda Var(X)=lambda^2
# co chcemy zrobić, to zastować transformate na operator wariancji t(Var(X)) żeby 
# otrzymać jakąś stałą liczbę i pozbyć się niezależności. 
# Wykresy
# Na wykresie pierwszym (dds), widzimy, zależność wariancji +- Var(X) = 10 * E(X),
# Nie pozwala nam ona na jej interpretacje
# Na wykresie drugim (vsd), widzimy już unormalizowane wyniki, i mozemy zobaczyć,
# jak rośnie wartość operatora wariancji względem średniej.
# Niestety nie udało mi się znaleźć jak wydobyć jaki ostatecznie wynik numeryczny,
# został zastosowany do przeskalowania danych, jeżeli da się to zrobić 
# bym był wdzięczny za podpowiedź
# 
# 2)*
# Tutaj bierzemy najbardziej rozrzucone zmienne, i szukamy danych które są 
# nietypowe. Widzimy że pomiędzy próbami, nie ma znaczącej różnicy. Widzimy natomiast 
# różnicę pomiędzy poszczególnymi związkami do grupy kontrolnej. Nie omawiam związków,
# nie taki jest cel. 
#
# 3)* 
# Tutaj mamy analize replikatów, sprawdzamy czy istnieje silna korelacja między próbkami,
# Z wykresu widać, że jest wszystko w porządku. Gdyby dane były bardziej rozmyte,
# trzeba by czyścić dane. 
#
# 4)*
#
# Wstęp teoretyczny
# O samej metodzie to polega na tym, że (znowu bez wzorów - brak latex'a),
# Mając dane i jakąs ilośc cech k, będziemy chcieli znaleźć przesztrzeń, 
# która jest transformacją naszej obecnej w przestrzeni próby losowej ().
#
# Transformacja przenosi nas w przestrzeń rozkładów rozkładów normalnych, i znajduje,
# osie (wektory własne), które ją rozpinaja oraz wariancje pomiędzy poszczególnymi,
# przestrzeniami. Procent wariancji, mówi nam intuicyjnie ile informacji dana przestrzeń
# zawiera z wyjściowych danych. Matematycznie to nami mówi ile informacji o położeniu,
# wynika z tego wymiaru. 
# 
#
# Wykresy niczym się nie różnią, na ćwiczeniach było mówione, wzieliśmy za dużo,
# elementów. Widać różnicę przy 100. Poniżej doszło do mnie, że możliwe że jest to
# domyślna wartość
# 
# 5) * 
# Tutaj miałem zagwozdkę, po przejrzeniu ponownie top1000, mam tezę, że `plotPCA` domyślnie
# wybiera 1000 najbardziej aktywnych genów, nie mogłem tego znaleźć w dokumentacji.
# Wtedy te nasze analizy będą się różnić ponieważ są dla wszystkich genów. I oczywiscie
# mając więcej zmiennych (genów) PCA będzie miało mniejsze wartości na poszczególnych
# wartościach własnych co się przekłada na mniejsza wyjaśnialność.
# 
#______________________________________________________________________________
# 1) Use vst function (blind=F) on dds and visualize the effects with meanSdPlot,
# compare the plot with one created from dds (use assay).
# Funkcja odpowiada za 
vsd = vst(dds, blind=FALSE)
metadata((vsd))
meanSdPlot(assay(dds), ranks=TRUE)
meanSdPlot(assay(vsd), ranks=TRUE)
# 2) Create a heatmap with top 100 genes by variance, use clustering and scale
# by rows.
#TODO - trzeba porównać całość 
rv = rowVars(assay(vsd))
top100 = order(rv, decreasing = TRUE)[1:100]
mat_top = assay(vsd)[top100, ]
# standaryzacja - średnia 0, odchylenie 1 
mat_scaled = t(scale(t(mat_top)))
# skala z kolorami 
hm_cols = colorRampPalette(brewer.pal(9, "YlGnBu"))(100)
# heatmap
png("heatmap_top100_vst_scaled.png", width = 1600, height = 1200, res = 180)
pheatmap(
  mat_scaled,
  clustering_distance_rows = "euclidean",
  clustering_distance_cols = "euclidean",
  show_rownames = FALSE,
  annotation_col = as.data.frame(coldata),
  color = hm_cols,
  scale = "row"
)
dev.off()
dev.list()
# a) Use base R png function to save the plot as a PNG file.


# 3) Create a heatmap of the sample-to-sample distances, as rownames use
# sample names e.g. from rownames(coldata).
# You can change color palette - to check available options run:
# display.brewer.all(type = "seq")
# ustalenie wartości
sample_dists = dist(t(assay(vsd)))
sample_mat = as.matrix(sample_dists)
rownames(sample_mat) = colnames(vsd)
colnames(sample_mat) = colnames(vsd)
# ustalenie kolorów
dist_cols = colorRampPalette(rev(brewer.pal(9, "Blues")))(100)

# heatmapa
png("sample_distance_vst.png", width = 1400, height = 1200, res = 160)
pheatmap(
  sample_mat,
  clustering_distance_rows = "euclidean",
  clustering_distance_cols = "euclidean",
  color = dist_cols
)
dev.off()
dev.list()


# 4) Create a PCA plot.
pca_data = plotPCA(vsd, intgroup = c("condition"), returnData = TRUE)
percentVar = round(100 * attr(pca_data, "percentVar"))
# wykres
png("PCA_vsd_condition.png", width = 1200, height = 900, res = 150)
ggplot(pca_data, aes(PC1, PC2, color = condition)) +
  geom_point(size = 3) +
  xlab(paste0("PC1: ", percentVar[1], "%")) +
  ylab(paste0("PC2: ", percentVar[2], "%")) +
  theme_bw()
dev.off(3)
dev.list()
# a) Use base R png function to save the plot as a PNG file.
# wyżej


# b) Create PCA only for 'condition' for top 1000 genes and save the plot.
top1000 = order(rv, decreasing = TRUE)[1:1000]
vsd_top = vsd[top1000, ]

pca_top = plotPCA(vsd_top, intgroup = c("condition"), returnData = TRUE)
percentVar_top = round(100 * attr(pca_top, "percentVar"))

png("PCA_vsd_top1000_condition.png", width = 1200, height = 900, res = 150)
ggplot(pca_top, aes(PC1, PC2, color = condition)) +
  geom_point(size = 3) +
  xlab(paste0("PC1: ", percentVar_top[1], "%")) +
  ylab(paste0("PC2: ", percentVar_top[2], "%")) +
  theme_bw()
dev.off(4)
dev.list()
# zapis

# 5)* PCA analysis
# a)* Remove genes (rows) with zero variance from vst transformed data
# tworzymy macierz z danych po transformacji vst 
nz_vsd = assay(vsd) 
nz_v = rowVars(nz_vsd)
nz_vsd = nz_vsd[nz_v > 0, ]
# b)* run prcomp on transposed matrix, use scale.=TRUE. Check structure of 
# the output.
pc = prcomp(t(nz_vsd), scale. = TRUE)
# pc$x -współrzędne próbek
# pc$dev - wariancja
# pc$rotation - wkłady poszczególlnych genów pr 

# c)* Create a data frame for plotting custom PCA plot with PC1 and PC2 for 
#  all genes ($x). Use condition as color variable in ggplot2.
pc_df = data.frame(
  PC1 = pc$x[, 1],
  PC2 = pc$x[, 2],
  condition = coldata$condition,
  sample = rownames(coldata)
)
png("PCA_custom_PC1_PC2.png", width = 1200, height = 900, res = 150)
ggplot(pc_df, aes(PC1, PC2, color = condition, label = sample)) +
  geom_point(size = 3) +
  geom_text(vjust = -0.7, size = 3) +
  theme_bw()
dev.off(3)
dev.list()

# d)* Create a data frame with PC number and explained variance using $sdev. 
# PC number variable should be an ordered factor. Create a screeplot with
# ggplot2 (x= PC number, y = Percent of explained variance)
explained = pc$sdev^2 / sum(pc$sdev^2) * 100 # odchylenie standrdowe^2 i wtedy wariancje normalizujemy 

scree = data.frame(
  PC = factor(seq_along(explained), levels = seq_along(explained), ordered = TRUE),
  variance = explained
)
png("PCA_scree.png", width = 1200, height = 900, res = 150)
ggplot(scree, aes(x = PC, y = variance)) +
  geom_col(fill = "steelblue") +
  ylab("Percent of explained variance") +
  theme_bw()
dev.off(3)
dev.list()
# e)* Create a barplot of genes that mostly contribute to PC3 - both on the top
# and bottom values of $rotation - a Top 20 Loadings barplot. Use ordered 
# factor for sorted plotting.
pc3_load = pc$rotation[, 3] 
ord_pos = order(pc3_load, decreasing = TRUE)[1:20]
ord_neg = order(pc3_load, decreasing = FALSE)[1:20]

top_pos = data.frame(
  gene = factor(names(pc3_load)[ord_pos], levels = names(pc3_load)[ord_pos], ordered = TRUE),
  loading = pc3_load[ord_pos]
)

top_neg = data.frame(
  gene = factor(names(pc3_load)[ord_neg], levels = names(pc3_load)[ord_neg], ordered = TRUE),
  loading = pc3_load[ord_neg]
)

png("PCA_loadings_PC3_toppos.png", width = 1600, height = 900, res = 150)
ggplot(top_pos, aes(x = gene, y = loading)) +
  geom_col(fill = "tomato") +
  coord_flip() +
  ggtitle("Top 20 positive loadings (PC3)") +
  theme_bw()
dev.off(3)
dev.list()

png("PCA_loadings_PC3_topneg.png", width = 1600, height = 900, res = 150)
ggplot(top_neg, aes(x = gene, y = loading)) +
  geom_col(fill = "forestgreen") +
  coord_flip() +
  ggtitle("Top 20 negative loadings (PC3)") +
  theme_bw()
dev.off(3)
dev.list()

#______________________________________________________________________________
#
# 4. Differential analysis #TODO JUTRO 
#______________________________________________________________________________
#==============================================================================
# 
# Cel
# Celem DE (differential) jest znalezienie genów, które zmieniają swoją ekspresję
# (tutaj poziom mRNA), między różnymi warunkami biologicznymi, problemy polegają na
# - szum biologiczny - różnice ekspresji pomiędzy różnymi komórkami
# - szum techniczny - związek z eksperymentem
# - efekt eksperymentalny - tą część chcemy wychwycić, wskazuje na zmiany względem
# różnych warunków planowanych
# 
# Tutaj następuje analiza statystyczna, osobno dla każdego genu, robimy
# K_{ij} \sim \mathrm{NB}(\mu_{ij}, \alpha_i)
# 
# $K_{ij}$ - liczba odczytów genu $i$ w próbce $j$ 
# $\mu_{ij}$ = s_jq_{ij}
# $s_j$ - współczynnik normalizacji dla próbki
# $q_{ij}$ - oczekiwana ekspresja  
# $\alpha_i$ - dyspersja
# 
# do miar Log2 fold change w znaczeniu biologicznym 
# średnia ekspresja A / średnia ekspresja B w logarytmie - pozwala to na 
# 
# Korekta wielokrotnego testowania (nie wiedziałem tego) (FDR)
# #TODO - później - tutaj testujemy czy istnieją istotnne zmiany WALD albo lrt 
#
# ______________________________________________________________________________
#
# 1) Because of visual analysis it shows that we don't have batch effect
# Remove replicate variable from the design
design(dds) = ~ condition

# 2) Pre-filter dds object to keep only rows that have a count of at least 10 
# for a minimal number of samples. 
keep = rowSums(counts(dds) >= 10) >= 2
dds = dds[keep, ]

# 3) Perform differential analysis
dds = DESeq(dds)


# 4)*** Look at available results with resultsNames ***#TODO - TUTAJ LITERÓWKA result -> results
resultsNames(dds)

# 5) Get results for every comparison and use summary
rn = resultsNames(dds)
res_list = lapply(rn, function(nm) results(dds, name = nm))
names(res_list) = rn
summaries = lapply(res_list, summary)
summary(res_list[2])  # prints summary per contrast


#* nie wiem dlaczego, ale nie jestem w stanie załadow lapply na summary,
# dostaje zawsze none
rn <- resultsNames(dds)
res_list = lapply(rn, function(nm) results(dds, name=nm))
df <- data.frame(
  name = rn,
  results = I(lapply(rn, function(nm) results(dds, name = nm))),
  summary = I(lapply(rn, function(nm) summary(results(dds, name = nm))))
)
# poniższe summary działa poprawnie..
for i in length(rn) {
  summary(df$results[[i]])  
}

# a)* Use resultsNames(dds) vector with lapply to extract results as a list. 
# Name the list. Use lapply to print summaries.
# - print nie działa (wyżej df) dostaje wartości, rozumiem że chodziło o automatyzacje
# ale nie mogę umieśccić wyników summary w tabeli (są None)

# 6) Get significant results with p-adjusted < 0.05 using subset
# rozwiązanie w a)* 

# a)* Use lapply on the result list to get significant results
sig_list = lapply(df$results, function(res) {
  subset(res, padj < 0.05)
})

# 7) Export whole results (without subsetting) to csv files
invisible(lapply(names(res_list), function(nm) {
  df = as.data.frame(res_list[[nm]])
  write.csv(df, paste0("DESeq2_results_", nm, ".csv"), row.names = TRUE)
}))

# a)* Use lapply to save results as csv files. Use list names to give 
# corresponding file names
# powyżej 

# 8) Add gene_biotype annotation as a new column to the significant results.
# Use org.Hs.eg.db as annotation with the mapIds() function 
# (keytype = "SYMBOL", column = "GENETYPE").
sig_annot = lapply(sig_list, function(df) {
  syms = rownames(df)
  biotype = mapIds(
    org.Hs.eg.db,
    keys = syms,
    keytype = "SYMBOL",   
    column = "GENETYPE",  
    multiVals = "first"
  )
  df$gene_biotype = biotype[rownames(df)]
  df
})

# a)* Use lapply to modify in the same way the list of significant results
# powyżej 

# 9) Write significant results to an Excel file
#    a) Extract the row names into a vector called 'genes' and use cbind() 
#       to add it as the first column
sig_with_gene_col = lapply(sig_annot, function(df) {
  genes = rownames(df)
  cbind(gene = genes, df)
})

wb = openxlsx::createWorkbook()
# b)* Use lapply to modify the significant result list as described

invisible(lapply(names(sig_with_gene_col), function(nm) {
  openxlsx::addWorksheet(wb, sheetName = gsub("[^A-Za-z0-9_]", "_", nm))
  openxlsx::writeData(wb, sheet = nm, x = sig_with_gene_col[[nm]])
}))

#    c) Use the openxlsx package to save the results as an .xlsx file, 
#       with one results table per sheet 
#       (see: https://ycphs.github.io/openxlsx/ )
openxlsx::saveWorkbook(wb, file = "DESeq2_significant_results.xlsx", overwrite = TRUE)


# d)* Use lapply on the significant result list to write data to workbook sheets


#______________________________________________________________________________
#
# 5. Visualization of the DE analysis
#______________________________________________________________________________
#==============================================================================
# 1) View a dispersion plot in DESeq2.
#    The dispersion measures how much gene counts vary across replicates 
#    beyond what is expected from a Poisson distribution.
#    Additional reading and explanation: 
#    https://hbctraining.github.io/DGE_workshop/lessons/04_DGE_DESeq2_analysis.html
png("DESeq2_dispersion.png", width = 1400, height = 1000, res = 160)
plotDispEsts(dds)e
dev.list()
dev.off(3)
# 2) Create MA plots:
# a) Create MA plot for chosen comparison for raw data
chosen = rn[1] 
res_chosen = results(dds, name = chosen)
png(paste0("MA_raw_", gsub("[^A-Za-z0-9_]", "_", chosen), ".png"),
    width = 1400, height = 1000, res = 160)
plotMA(res_chosen, ylim = c(-5, 5))
dev.off()
# It is more useful to visualize the MA-plot for the shrunken log2 fold changes, 
# which remove the noise associated with log2 fold changes from low count genes 
# without requiring arbitrary filtering thresholds.

# b) Create an MA plot for the chosen comparison using lfcShrink with the 
#    standard "normal" shrinkage estimator.
#    Newer methods such as ashr or apeglm exist, but they are beyond the scope
#    of this course.
res_shrunk = lfcShrink(dds, coef = which(resultsNames(dds) == chosen), type = "normal")

png(paste0("MA_shrunk_", gsub("[^A-Za-z0-9_]", "_", chosen), ".png"),
    width = 1400, height = 1000, res = 160)
plotMA(res_shrunk, ylim = c(-5, 5))
dev.off(3)
dev.list()
# c)* use a loop to create and save MAplots for every coefficient using
#     lfc shrunk results. Use base R png function to save.
invisible(lapply(seq_along(rn), function(i) {
  nm = rn[i]
  res_i = lfcShrink(dds, coef = i, type = "normal")
  png(paste0("MA_shrunk_", gsub("[^A-Za-z0-9_]", "_", nm), ".png"),
      width = 1400, height = 1000, res = 160)
  plotMA(res_i, ylim = c(-5, 5))
  dev.off(3)
}))

# 3) Create a custom volcano plot for selected lfc shrunk results:
#    a) Use ggplot2 to create a scatter plot with log2FoldChange on the x-axis 
#      and -log10(p-adj) on the y-axis
volc = as.data.frame(res_shrunk)
volc$neglog10_padj = -log10(volc$padj)

# Basic volcano
png(paste0("Volcano_", gsub("[^A-Za-z0-9_]", "_", chosen), ".png"),
    width = 1400, height = 1000, res = 160)
ggplot(volc, aes(x = log2FoldChange, y = neglog10_padj)) +
  geom_point(alpha = 0.5) +
  theme_bw() +
  xlab("log2 Fold Change") +
  ylab("-log10(p-adj)")
dev.off(4)
dev.list()
#    b) Use base R png function to save the plot as a PNG file.


#    c)* Add horizontal line and colors to mark significance thresholds 
#       (e.g. p-adj < 0.05). You can also add vertical lines to mark LFC. 
#       Save the plot.
alpha = 0.05
lfc_thr = 1  # vertical threshold example

volc$signif = factor(
  ifelse(volc$padj < alpha & abs(volc$log2FoldChange) >= lfc_thr, "sig&LFC",
         ifelse(volc$padj < alpha, "sig", "ns")),
  levels = c("ns", "sig", "sig&LFC"), ordered = TRUE
)

png(paste0("Volcano_thresh_", gsub("[^A-Za-z0-9_]", "_", chosen), ".png"),
    width = 1400, height = 1000, res = 160)
ggplot(volc, aes(x = log2FoldChange, y = neglog10_padj, color = signif)) +
  geom_point(alpha = 0.7) +
  geom_hline(yintercept = -log10(alpha), linetype = "dashed", color = "red") +
  geom_vline(xintercept = c(-lfc_thr, lfc_thr), linetype = "dotted", color = "blue") +
  scale_color_manual(values = c("grey70", "orange", "firebrick")) +
  theme_bw() +
  xlab("log2 Fold Change") +
  ylab("-log10(p-adj)")
dev.off(3)
dev.list()