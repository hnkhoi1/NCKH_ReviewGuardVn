# Literature review (DRAFT v0): opinion spam, fake reviews and group spam

> Draft for ReviewGuard VN. Built from `paper_table.csv` (P01-P16). Items marked **[CHECK]** were verified only from abstracts or search metadata and must be confirmed in the full paper before submission. The survey is not exhaustive: it covers the core papers listed in `docs/literature/README.md`, not a systematic search.

## 1. Opinion spam: definition and early taxonomy

Jindal and Liu (2008) gave the first large-scale study of opinion spam on about 5.8 million Amazon reviews and separated it into three types: (1) untruthful opinions (fake reviews that promote or defame a product), (2) brand-only reviews, and (3) non-reviews such as advertisements or irrelevant text. They detected types 2 and 3 with logistic regression on review, reviewer and product features (AUC up to 98.7%), but type 1 could not be labeled by hand, so duplicate reviews were used as a proxy for spam (AUC 78%). They also found that helpfulness votes do not separate spam from non-spam. This three-type scheme is the origin of the labels later used for Vietnamese data (Section 5).

## 2. Detecting fake (deceptive) reviews from text

Ott et al. (2011) built a gold-standard set of 800 positive hotel reviews (400 truthful from TripAdvisor, 400 deceptive written by Mechanical Turk workers) and compared three approaches: part-of-speech features, psycholinguistic (LIWC) features and n-grams. LIWC plus bigrams with a linear SVM reached 89.8% accuracy, while three human judges scored 53.1-61.9% (Fleiss' kappa 0.11), so people are poor at spotting fakes. Limits: the fakes are crowdsourced rather than real, the data covers only positive hotel reviews, and some submissions were low-effort.

Salminen et al. (2022) look at machine-generated fakes: reviews generated with ULMFiT and GPT-2 from an Amazon dataset were used to train a classifier that detected fakes almost perfectly, and also worked on human-written fakes, while human raters were significantly less accurate **[CHECK: only the abstract was read; dataset size and scores unverified]**. This motivates a robustness test of our models on LLM-generated reviews.

## 3. Behavior, network and metadata approaches

Text alone is limited, so later work uses how reviewers behave. Rayana and Akoglu (2015) proposed SpEagle, which puts users, reviews and products in one graph and combines text and behavioral priors (rating deviation, burstiness, content similarity and others) with a Markov Random Field solved by loopy belief propagation. On three Yelp datasets (YelpChi, YelpNYC, YelpZip) it beat earlier baselines (review-ranking AP on YelpChi 0.3236 vs 0.1518 and 0.1067), and 1% labeled data improved it further. Limits: ground truth is Yelp's recommendation filter rather than verified fraud, absolute precision is modest, and features are hand-designed.

## 4. Coordinated and group spam

Mukherjee et al. (2012) studied fake reviewer groups on Amazon (53,469 reviewers, 109,518 reviews). They mined candidate groups with frequent itemset mining (7,052 candidates), scored them with behavioral indicators (time window, rating deviation, content similarity, group size and others) and ranked them with GSRank, reaching AUC 0.93-0.95 against 0.86-0.88 for RankBoost. Eight judges labeled 2,431 groups (Fleiss' kappa 0.79), and labeling groups was easier than labeling single reviews. Limits: old data (2006), subjective labels, no way to tell sockpuppets from several people, and groups acting only once are missed.

Supporting tools for this direction in our design: Sentence-BERT embeddings with cosine similarity to find near-duplicate reviews (Reimers and Gurevych, 2019), HDBSCAN to cluster them without fixing the number of clusters (Campello et al., 2013 **[CHECK: abstract only]**), Kleinberg's (2002) burst model for sudden waves of reviews, Isolation Forest for anomalous behavior (Liu et al., 2008 **[CHECK: abstract not read]**) and Louvain community detection on a reviewer-product graph (Blondel et al., 2008).

## 5. Vietnamese resources and language models

Van Dinh et al. (2022) introduced ViSpamReviews, about 19,000 annotated Vietnamese e-commerce reviews with four labels (NO-SPAM, SPAM-1 fake, SPAM-2 brand-only, SPAM-3 non-review), following the Jindal and Liu scheme. Annotator agreement started low (Cohen's kappa 0.43 and 0.44) and rose to 0.72 and 0.68 after the guideline was revised and annotators retrained. PhoBERT was best (macro F1 86.89 for spam detection and 72.17 for spam type), ahead of Text-CNN, LSTM, GRU and BERT4News. Van Dinh and Luu (2024) added product metadata (category and description features) and gained about 1.6 points F1 on detection (87.22) and 1.9 on spam type (73.49), which suggests extra signals help. PhoBERT (Nguyen and Nguyen, 2020) is a monolingual Vietnamese model that its authors report beats XLM-R on four tasks; XLM-R (Conneau et al., 2020) is the multilingual alternative trained on 100 languages **[CHECK: abstracts only; corpus and word-segmentation requirement of PhoBERT unverified]**.

## 6. Explaining decisions

SHAP (Lundberg and Lee, 2017) and LIME (Ribeiro et al., 2016) explain single predictions and fit the explanation part of ReviewGuard VN. LIME's venue should be confirmed **[CHECK]**.

## 7. Gaps and how ReviewGuard VN responds

Based on these papers (not a systematic search, so confirm before claiming novelty):

1. **Text vs behavior.** The Vietnamese benchmark papers work mainly on review text, with only product metadata added in 2024, while the group-spam methods (Mukherjee et al., 2012; Rayana and Akoglu, 2015) rely on reviewer, time and network signals. ReviewGuard VN combines a content branch and a pattern branch.
2. **Group labels in Vietnamese.** The ViSpamReviews labels are per review. We did not find in these papers a Vietnamese set labeled at group level; this needs a wider search.
3. **Annotation quality.** ViSpamReviews shows agreement is hard to reach and improved only after guideline revision, so guideline v1 and a kappa check matter.
4. **Machine-generated fakes.** Salminen et al. (2022) show LLM-written fakes are easy for a classifier trained on them but hard for humans; the robustness to such reviews in Vietnamese is untested.
5. **Explanations.** Earlier detection papers report scores more than reasons; we add SHAP and similar-review clusters.

## References

- Blondel, V. D., Guillaume, J.-L., Lambiotte, R., Lefebvre, E. (2008). Fast unfolding of communities in large networks. J. Stat. Mech., P10008. arXiv:0803.0476.
- Campello, R. J. G. B., Moulavi, D., Sander, J. (2013). Density-based clustering based on hierarchical density estimates. PAKDD 2013, LNCS 7819, 160-172.
- Conneau, A., et al. (2020). Unsupervised cross-lingual representation learning at scale. ACL 2020. arXiv:1911.02116.
- Jindal, N., Liu, B. (2008). Opinion spam and analysis. WSDM 2008.
- Kleinberg, J. (2002). Bursty and hierarchical structure in streams. KDD 2002.
- Liu, F. T., Ting, K. M., Zhou, Z.-H. (2008). Isolation forest. ICDM 2008, 413-422.
- Lundberg, S., Lee, S.-I. (2017). A unified approach to interpreting model predictions. NeurIPS 2017. arXiv:1705.07874.
- Mukherjee, A., Liu, B., Glance, N. (2012). Spotting fake reviewer groups in consumer reviews. WWW 2012, 191-200.
- Nguyen, D. Q., Nguyen, A. T. (2020). PhoBERT: Pre-trained language models for Vietnamese. Findings of EMNLP 2020. arXiv:2003.00744.
- Ott, M., Choi, Y., Cardie, C., Hancock, J. T. (2011). Finding deceptive opinion spam by any stretch of the imagination. ACL 2011, 309-319.
- Rayana, S., Akoglu, L. (2015). Collective opinion spam detection: Bridging review networks and metadata. KDD 2015.
- Reimers, N., Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks. EMNLP 2019. arXiv:1908.10084.
- Ribeiro, M. T., Singh, S., Guestrin, C. (2016). "Why should I trust you?": Explaining the predictions of any classifier. KDD 2016. arXiv:1602.04938.
- Salminen, J., Kandpal, C., Kamel, A. M., Jung, S., Jansen, B. J. (2022). Creating and detecting fake reviews of online products. J. Retailing and Consumer Services, 64, 102771.
- Van Dinh, C., Luu, S. T. (2024). Metadata integration for spam reviews detection on Vietnamese e-commerce websites. Int. J. Asian Language Processing. arXiv:2405.13292.
- Van Dinh, C., Luu, S. T., Nguyen, A. G.-T. (2022). Detecting spam reviews on Vietnamese e-commerce websites. ACIIDS 2022. arXiv:2207.14636.
