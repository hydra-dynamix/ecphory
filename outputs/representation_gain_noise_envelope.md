# Representation Gain Noise Envelope

This grid varies dropout and spurious activation while holding the downstream event-first hierarchy fixed.

Region symbols: `+` positive gain, `-` negative gain, `I` identity collapse, `U` undercapture, `H` hostile collapse, `L` hostile leak, `B` borderline.

## Region Counts

### branch

- `sliding_window_low_threshold` region_counts={'borderline': 3, 'positive_gain': 36, 'identity_collapse': 36} gain_mean=0.183694 gain_min=-0.006771 exact_mean=0.377556 support_mean=0.561249 coverage_mean=1.358327
- `sliding_low_temporal_consensus_pair` region_counts={'borderline': 3, 'positive_gain': 49, 'identity_collapse': 23} gain_mean=0.157921 gain_min=-0.029885 exact_mean=0.550667 support_mean=0.708587 coverage_mean=1.113551
- `union_temporal_consensus_pair` region_counts={'borderline': 3, 'identity_collapse': 38, 'undercapture': 33, 'negative_gain': 1} gain_mean=-0.059856 gain_min=-0.239448 exact_mean=0.364444 support_mean=0.304589 coverage_mean=0.747076

### overlap

- `sliding_window_low_threshold` region_counts={'borderline': 3, 'positive_gain': 37, 'identity_collapse': 35} gain_mean=0.189359 gain_min=0.000000 exact_mean=0.361333 support_mean=0.550692 coverage_mean=1.357213
- `sliding_low_temporal_consensus_pair` region_counts={'borderline': 3, 'positive_gain': 46, 'identity_collapse': 26} gain_mean=0.176398 gain_min=-0.015576 exact_mean=0.521556 support_mean=0.697954 coverage_mean=1.109944
- `union_temporal_consensus_pair` region_counts={'borderline': 3, 'positive_gain': 3, 'identity_collapse': 35, 'undercapture': 34} gain_mean=-0.040127 gain_min=-0.190476 exact_mean=0.350222 support_mean=0.310095 coverage_mean=0.743019

### hostile_unique

- `sliding_window_low_threshold` region_counts={'hostile_collapse': 75} gain_mean=0.000000 gain_min=0.000000 exact_mean=0.000000 support_mean=0.000000 coverage_mean=1.218573
- `sliding_low_temporal_consensus_pair` region_counts={'hostile_collapse': 67, 'hostile_leak': 8} gain_mean=0.000000 gain_min=0.000000 exact_mean=0.000000 support_mean=0.000000 coverage_mean=0.707232
- `union_temporal_consensus_pair` region_counts={'hostile_collapse': 24, 'hostile_leak': 51} gain_mean=0.000000 gain_min=0.000000 exact_mean=0.000000 support_mean=0.000000 coverage_mean=0.508672

## Envelope Maps

### branch

#### branch / sliding_window_low_threshold

| dropout \ spurious | 0.00 | 0.05 | 0.10 | 0.15 | 0.20 |
| --- | --- | --- | --- | --- | --- |
| 0.00 | B | + | I | I | I |
| 0.05 | + | + | I | I | I |
| 0.10 | + | + | + | I | I |
| 0.15 | + | + | + | I | I |
| 0.20 | + | + | + | I | I |

#### branch / sliding_low_temporal_consensus_pair

| dropout \ spurious | 0.00 | 0.05 | 0.10 | 0.15 | 0.20 |
| --- | --- | --- | --- | --- | --- |
| 0.00 | B | + | + | + | I |
| 0.05 | + | + | + | I | I |
| 0.10 | + | + | + | I | I |
| 0.15 | + | + | + | I | I |
| 0.20 | + | + | + | + | I |

#### branch / union_temporal_consensus_pair

| dropout \ spurious | 0.00 | 0.05 | 0.10 | 0.15 | 0.20 |
| --- | --- | --- | --- | --- | --- |
| 0.00 | B | I | I | U | U |
| 0.05 | I | I | I | U | U |
| 0.10 | I | I | I | U | U |
| 0.15 | I | I | I | U | U |
| 0.20 | I | I | U | U | U |

### overlap

#### overlap / sliding_window_low_threshold

| dropout \ spurious | 0.00 | 0.05 | 0.10 | 0.15 | 0.20 |
| --- | --- | --- | --- | --- | --- |
| 0.00 | B | + | I | I | I |
| 0.05 | + | + | I | I | I |
| 0.10 | + | + | + | I | I |
| 0.15 | + | + | + | I | I |
| 0.20 | + | + | + | I | I |

#### overlap / sliding_low_temporal_consensus_pair

| dropout \ spurious | 0.00 | 0.05 | 0.10 | 0.15 | 0.20 |
| --- | --- | --- | --- | --- | --- |
| 0.00 | B | + | + | + | I |
| 0.05 | + | + | + | I | I |
| 0.10 | + | + | + | I | I |
| 0.15 | + | + | + | I | I |
| 0.20 | + | + | + | I | I |

#### overlap / union_temporal_consensus_pair

| dropout \ spurious | 0.00 | 0.05 | 0.10 | 0.15 | 0.20 |
| --- | --- | --- | --- | --- | --- |
| 0.00 | B | + | I | U | U |
| 0.05 | I | I | I | U | U |
| 0.10 | I | I | I | U | U |
| 0.15 | I | I | I | U | U |
| 0.20 | I | I | U | U | U |

### hostile_unique

#### hostile_unique / sliding_window_low_threshold

| dropout \ spurious | 0.00 | 0.05 | 0.10 | 0.15 | 0.20 |
| --- | --- | --- | --- | --- | --- |
| 0.00 | H | H | H | H | H |
| 0.05 | H | H | H | H | H |
| 0.10 | H | H | H | H | H |
| 0.15 | H | H | H | H | H |
| 0.20 | H | H | H | H | H |

#### hostile_unique / sliding_low_temporal_consensus_pair

| dropout \ spurious | 0.00 | 0.05 | 0.10 | 0.15 | 0.20 |
| --- | --- | --- | --- | --- | --- |
| 0.00 | H | H | H | H | H |
| 0.05 | H | H | H | H | H |
| 0.10 | H | H | H | H | H |
| 0.15 | H | H | H | H | H |
| 0.20 | H | H | H | H | H |

#### hostile_unique / union_temporal_consensus_pair

| dropout \ spurious | 0.00 | 0.05 | 0.10 | 0.15 | 0.20 |
| --- | --- | --- | --- | --- | --- |
| 0.00 | H | H | L | L | L |
| 0.05 | H | H | L | L | L |
| 0.10 | H | L | L | L | L |
| 0.15 | H | H | L | L | L |
| 0.20 | H | L | L | L | L |

## Cell Metrics

### branch

#### sliding_window_low_threshold

- dropout=0.00 spurious=0.00 region=borderline gain_mean=0.000000 exact_mean=1.000000 support_mean=1.000000 coverage_mean=1.554497
- dropout=0.00 spurious=0.05 region=positive_gain gain_mean=0.045723 exact_mean=0.800000 support_mean=0.845723 coverage_mean=1.314475
- dropout=0.00 spurious=0.10 region=identity_collapse gain_mean=0.039952 exact_mean=0.411111 support_mean=0.451063 coverage_mean=1.320435
- dropout=0.00 spurious=0.15 region=identity_collapse gain_mean=0.015432 exact_mean=0.183333 support_mean=0.198765 coverage_mean=1.445510
- dropout=0.00 spurious=0.20 region=identity_collapse gain_mean=0.033932 exact_mean=0.000000 support_mean=0.033932 coverage_mean=1.630416
- dropout=0.05 spurious=0.00 region=positive_gain gain_mean=0.050000 exact_mean=0.950000 support_mean=1.000000 coverage_mean=1.507051
- dropout=0.05 spurious=0.05 region=positive_gain gain_mean=0.138744 exact_mean=0.755556 support_mean=0.894300 coverage_mean=1.276890
- dropout=0.05 spurious=0.10 region=identity_collapse gain_mean=0.073611 exact_mean=0.427778 support_mean=0.501389 coverage_mean=1.272613
- dropout=0.05 spurious=0.15 region=identity_collapse gain_mean=0.093651 exact_mean=0.105556 support_mean=0.199207 coverage_mean=1.425518
- dropout=0.05 spurious=0.20 region=identity_collapse gain_mean=0.046445 exact_mean=0.038889 support_mean=0.085334 coverage_mean=1.603977
- dropout=0.10 spurious=0.00 region=positive_gain gain_mean=0.166666 exact_mean=0.833334 support_mean=1.000000 coverage_mean=1.462754
- dropout=0.10 spurious=0.05 region=positive_gain gain_mean=0.302386 exact_mean=0.655556 support_mean=0.957942 coverage_mean=1.227783
- dropout=0.10 spurious=0.10 region=positive_gain gain_mean=0.214315 exact_mean=0.361111 support_mean=0.575426 coverage_mean=1.234291
- dropout=0.10 spurious=0.15 region=identity_collapse gain_mean=0.104332 exact_mean=0.072222 support_mean=0.176554 coverage_mean=1.378895
- dropout=0.10 spurious=0.20 region=identity_collapse gain_mean=0.069614 exact_mean=0.027778 support_mean=0.097391 coverage_mean=1.577920
- dropout=0.15 spurious=0.00 region=positive_gain gain_mean=0.338889 exact_mean=0.661111 support_mean=1.000000 coverage_mean=1.393200
- dropout=0.15 spurious=0.05 region=positive_gain gain_mean=0.422573 exact_mean=0.533333 support_mean=0.955906 coverage_mean=1.145316
- dropout=0.15 spurious=0.10 region=positive_gain gain_mean=0.270718 exact_mean=0.311111 support_mean=0.581830 coverage_mean=1.165751
- dropout=0.15 spurious=0.15 region=identity_collapse gain_mean=0.259028 exact_mean=0.072222 support_mean=0.331251 coverage_mean=1.319047
- dropout=0.15 spurious=0.20 region=identity_collapse gain_mean=0.098208 exact_mean=0.011111 support_mean=0.109319 coverage_mean=1.498928
- dropout=0.20 spurious=0.00 region=positive_gain gain_mean=0.500000 exact_mean=0.500000 support_mean=1.000000 coverage_mean=1.287326
- dropout=0.20 spurious=0.05 region=positive_gain gain_mean=0.531041 exact_mean=0.411111 support_mean=0.942152 coverage_mean=1.056887
- dropout=0.20 spurious=0.10 region=positive_gain gain_mean=0.423319 exact_mean=0.200000 support_mean=0.623319 coverage_mean=1.103713
- dropout=0.20 spurious=0.15 region=identity_collapse gain_mean=0.271547 exact_mean=0.094445 support_mean=0.365992 coverage_mean=1.269343
- dropout=0.20 spurious=0.20 region=identity_collapse gain_mean=0.082211 exact_mean=0.022222 support_mean=0.104433 coverage_mean=1.485639

#### sliding_low_temporal_consensus_pair

- dropout=0.00 spurious=0.00 region=borderline gain_mean=0.000000 exact_mean=1.000000 support_mean=1.000000 coverage_mean=1.554497
- dropout=0.00 spurious=0.05 region=positive_gain gain_mean=0.043961 exact_mean=0.944444 support_mean=0.988406 coverage_mean=1.229452
- dropout=0.00 spurious=0.10 region=positive_gain gain_mean=0.104467 exact_mean=0.794444 support_mean=0.898911 coverage_mean=1.078533
- dropout=0.00 spurious=0.15 region=positive_gain gain_mean=0.053444 exact_mean=0.583333 support_mean=0.636778 coverage_mean=1.002596
- dropout=0.00 spurious=0.20 region=identity_collapse gain_mean=-0.010331 exact_mean=0.333333 support_mean=0.323003 coverage_mean=0.965991
- dropout=0.05 spurious=0.00 region=positive_gain gain_mean=0.050000 exact_mean=0.950000 support_mean=1.000000 coverage_mean=1.507051
- dropout=0.05 spurious=0.05 region=positive_gain gain_mean=0.087591 exact_mean=0.894444 support_mean=0.982036 coverage_mean=1.200735
- dropout=0.05 spurious=0.10 region=positive_gain gain_mean=0.080445 exact_mean=0.744445 support_mean=0.824890 coverage_mean=1.064494
- dropout=0.05 spurious=0.15 region=identity_collapse gain_mean=0.009222 exact_mean=0.461111 support_mean=0.470333 coverage_mean=1.011708
- dropout=0.05 spurious=0.20 region=identity_collapse gain_mean=0.020165 exact_mean=0.316667 support_mean=0.336831 coverage_mean=0.978001
- dropout=0.10 spurious=0.00 region=positive_gain gain_mean=0.166666 exact_mean=0.833334 support_mean=1.000000 coverage_mean=1.462754
- dropout=0.10 spurious=0.05 region=positive_gain gain_mean=0.224852 exact_mean=0.761111 support_mean=0.985963 coverage_mean=1.159278
- dropout=0.10 spurious=0.10 region=positive_gain gain_mean=0.158496 exact_mean=0.588889 support_mean=0.747384 coverage_mean=1.041293
- dropout=0.10 spurious=0.15 region=identity_collapse gain_mean=0.052882 exact_mean=0.350000 support_mean=0.402882 coverage_mean=0.997432
- dropout=0.10 spurious=0.20 region=identity_collapse gain_mean=0.038605 exact_mean=0.255556 support_mean=0.294161 coverage_mean=0.986260
- dropout=0.15 spurious=0.00 region=positive_gain gain_mean=0.338889 exact_mean=0.661111 support_mean=1.000000 coverage_mean=1.393200
- dropout=0.15 spurious=0.05 region=positive_gain gain_mean=0.349836 exact_mean=0.611111 support_mean=0.960947 coverage_mean=1.089473
- dropout=0.15 spurious=0.10 region=positive_gain gain_mean=0.267382 exact_mean=0.477778 support_mean=0.745160 coverage_mean=0.988778
- dropout=0.15 spurious=0.15 region=identity_collapse gain_mean=0.162098 exact_mean=0.305556 support_mean=0.467654 coverage_mean=0.959220
- dropout=0.15 spurious=0.20 region=identity_collapse gain_mean=0.067792 exact_mean=0.116667 support_mean=0.184459 coverage_mean=0.967144
- dropout=0.20 spurious=0.00 region=positive_gain gain_mean=0.500000 exact_mean=0.500000 support_mean=1.000000 coverage_mean=1.287326
- dropout=0.20 spurious=0.05 region=positive_gain gain_mean=0.491055 exact_mean=0.477778 support_mean=0.968833 coverage_mean=1.008050
- dropout=0.20 spurious=0.10 region=positive_gain gain_mean=0.356292 exact_mean=0.383333 support_mean=0.739626 coverage_mean=0.956129
- dropout=0.20 spurious=0.15 region=positive_gain gain_mean=0.262814 exact_mean=0.266667 support_mean=0.529481 coverage_mean=0.965941
- dropout=0.20 spurious=0.20 region=identity_collapse gain_mean=0.071387 exact_mean=0.155555 support_mean=0.226943 coverage_mean=0.983444

#### union_temporal_consensus_pair

- dropout=0.00 spurious=0.00 region=borderline gain_mean=0.000000 exact_mean=1.000000 support_mean=1.000000 coverage_mean=1.000000
- dropout=0.00 spurious=0.05 region=identity_collapse gain_mean=-0.054761 exact_mean=0.833333 support_mean=0.778573 coverage_mean=0.827686
- dropout=0.00 spurious=0.10 region=identity_collapse gain_mean=-0.040571 exact_mean=0.377778 support_mean=0.337207 coverage_mean=0.748834
- dropout=0.00 spurious=0.15 region=undercapture gain_mean=-0.009001 exact_mean=0.161111 support_mean=0.152110 coverage_mean=0.699291
- dropout=0.00 spurious=0.20 region=undercapture gain_mean=-0.012300 exact_mean=0.077778 support_mean=0.065477 coverage_mean=0.670865
- dropout=0.05 spurious=0.00 region=identity_collapse gain_mean=-0.136918 exact_mean=0.872222 support_mean=0.735305 coverage_mean=0.945606
- dropout=0.05 spurious=0.05 region=identity_collapse gain_mean=-0.118554 exact_mean=0.661111 support_mean=0.542557 coverage_mean=0.801615
- dropout=0.05 spurious=0.10 region=identity_collapse gain_mean=-0.048974 exact_mean=0.294444 support_mean=0.245470 coverage_mean=0.737850
- dropout=0.05 spurious=0.15 region=undercapture gain_mean=-0.039761 exact_mean=0.122222 support_mean=0.082461 coverage_mean=0.685858
- dropout=0.05 spurious=0.20 region=undercapture gain_mean=-0.008287 exact_mean=0.055556 support_mean=0.047269 coverage_mean=0.662482
- dropout=0.10 spurious=0.00 region=identity_collapse gain_mean=-0.214263 exact_mean=0.844445 support_mean=0.630182 coverage_mean=0.902346
- dropout=0.10 spurious=0.05 region=identity_collapse gain_mean=-0.112314 exact_mean=0.566667 support_mean=0.454353 coverage_mean=0.775483
- dropout=0.10 spurious=0.10 region=identity_collapse gain_mean=-0.053938 exact_mean=0.233333 support_mean=0.179395 coverage_mean=0.711184
- dropout=0.10 spurious=0.15 region=undercapture gain_mean=-0.029185 exact_mean=0.100000 support_mean=0.070815 coverage_mean=0.691042
- dropout=0.10 spurious=0.20 region=undercapture gain_mean=-0.006497 exact_mean=0.050000 support_mean=0.043503 coverage_mean=0.663449
- dropout=0.15 spurious=0.00 region=identity_collapse gain_mean=-0.194240 exact_mean=0.800000 support_mean=0.605759 coverage_mean=0.853290
- dropout=0.15 spurious=0.05 region=identity_collapse gain_mean=-0.104290 exact_mean=0.461111 support_mean=0.356821 coverage_mean=0.737562
- dropout=0.15 spurious=0.10 region=identity_collapse gain_mean=-0.037692 exact_mean=0.188889 support_mean=0.151197 coverage_mean=0.701000
- dropout=0.15 spurious=0.15 region=undercapture gain_mean=-0.012981 exact_mean=0.055556 support_mean=0.042574 coverage_mean=0.671375
- dropout=0.15 spurious=0.20 region=undercapture gain_mean=-0.017823 exact_mean=0.044444 support_mean=0.026621 coverage_mean=0.658785
- dropout=0.20 spurious=0.00 region=identity_collapse gain_mean=-0.157905 exact_mean=0.705555 support_mean=0.547650 coverage_mean=0.800970
- dropout=0.20 spurious=0.05 region=identity_collapse gain_mean=-0.074936 exact_mean=0.400000 support_mean=0.325064 coverage_mean=0.713884
- dropout=0.20 spurious=0.10 region=undercapture gain_mean=-0.013339 exact_mean=0.133333 support_mean=0.119994 coverage_mean=0.689521
- dropout=0.20 spurious=0.15 region=undercapture gain_mean=0.002251 exact_mean=0.055556 support_mean=0.057807 coverage_mean=0.668679
- dropout=0.20 spurious=0.20 region=undercapture gain_mean=-0.000117 exact_mean=0.016667 support_mean=0.016550 coverage_mean=0.658236

### overlap

#### sliding_window_low_threshold

- dropout=0.00 spurious=0.00 region=borderline gain_mean=0.000000 exact_mean=1.000000 support_mean=1.000000 coverage_mean=1.554629
- dropout=0.00 spurious=0.05 region=positive_gain gain_mean=0.070475 exact_mean=0.811111 support_mean=0.881586 coverage_mean=1.309900
- dropout=0.00 spurious=0.10 region=identity_collapse gain_mean=0.076560 exact_mean=0.344445 support_mean=0.421005 coverage_mean=1.331733
- dropout=0.00 spurious=0.15 region=identity_collapse gain_mean=0.033365 exact_mean=0.138889 support_mean=0.172254 coverage_mean=1.432010
- dropout=0.00 spurious=0.20 region=identity_collapse gain_mean=0.024144 exact_mean=0.038889 support_mean=0.063033 coverage_mean=1.612038
- dropout=0.05 spurious=0.00 region=positive_gain gain_mean=0.072222 exact_mean=0.927778 support_mean=1.000000 coverage_mean=1.513623
- dropout=0.05 spurious=0.05 region=positive_gain gain_mean=0.180974 exact_mean=0.750000 support_mean=0.930974 coverage_mean=1.275897
- dropout=0.05 spurious=0.10 region=identity_collapse gain_mean=0.059358 exact_mean=0.416667 support_mean=0.476025 coverage_mean=1.278746
- dropout=0.05 spurious=0.15 region=identity_collapse gain_mean=0.040128 exact_mean=0.127778 support_mean=0.167906 coverage_mean=1.434810
- dropout=0.05 spurious=0.20 region=identity_collapse gain_mean=0.056240 exact_mean=0.027778 support_mean=0.084018 coverage_mean=1.599706
- dropout=0.10 spurious=0.00 region=positive_gain gain_mean=0.222222 exact_mean=0.777778 support_mean=1.000000 coverage_mean=1.444094
- dropout=0.10 spurious=0.05 region=positive_gain gain_mean=0.290499 exact_mean=0.611111 support_mean=0.901611 coverage_mean=1.220529
- dropout=0.10 spurious=0.10 region=positive_gain gain_mean=0.210356 exact_mean=0.338889 support_mean=0.549245 coverage_mean=1.217508
- dropout=0.10 spurious=0.15 region=identity_collapse gain_mean=0.084350 exact_mean=0.105555 support_mean=0.189905 coverage_mean=1.401747
- dropout=0.10 spurious=0.20 region=identity_collapse gain_mean=0.042842 exact_mean=0.016667 support_mean=0.059509 coverage_mean=1.576248
- dropout=0.15 spurious=0.00 region=positive_gain gain_mean=0.394444 exact_mean=0.605556 support_mean=1.000000 coverage_mean=1.372770
- dropout=0.15 spurious=0.05 region=positive_gain gain_mean=0.387539 exact_mean=0.527778 support_mean=0.915317 coverage_mean=1.152615
- dropout=0.15 spurious=0.10 region=positive_gain gain_mean=0.316561 exact_mean=0.283333 support_mean=0.599894 coverage_mean=1.178005
- dropout=0.15 spurious=0.15 region=identity_collapse gain_mean=0.162910 exact_mean=0.061111 support_mean=0.224022 coverage_mean=1.323842
- dropout=0.15 spurious=0.20 region=identity_collapse gain_mean=0.093434 exact_mean=0.027778 support_mean=0.121212 coverage_mean=1.520023
- dropout=0.20 spurious=0.00 region=positive_gain gain_mean=0.527778 exact_mean=0.472222 support_mean=1.000000 coverage_mean=1.276431
- dropout=0.20 spurious=0.05 region=positive_gain gain_mean=0.575348 exact_mean=0.361111 support_mean=0.936459 coverage_mean=1.071464
- dropout=0.20 spurious=0.10 region=positive_gain gain_mean=0.493174 exact_mean=0.227778 support_mean=0.720952 coverage_mean=1.075068
- dropout=0.20 spurious=0.15 region=identity_collapse gain_mean=0.195385 exact_mean=0.033333 support_mean=0.228719 coverage_mean=1.274641
- dropout=0.20 spurious=0.20 region=identity_collapse gain_mean=0.123660 exact_mean=0.000000 support_mean=0.123660 coverage_mean=1.482257

#### sliding_low_temporal_consensus_pair

- dropout=0.00 spurious=0.00 region=borderline gain_mean=0.000000 exact_mean=1.000000 support_mean=1.000000 coverage_mean=1.554629
- dropout=0.00 spurious=0.05 region=positive_gain gain_mean=0.059091 exact_mean=0.933333 support_mean=0.992424 coverage_mean=1.240037
- dropout=0.00 spurious=0.10 region=positive_gain gain_mean=0.112500 exact_mean=0.772222 support_mean=0.884722 coverage_mean=1.080984
- dropout=0.00 spurious=0.15 region=positive_gain gain_mean=0.044493 exact_mean=0.572222 support_mean=0.616715 coverage_mean=0.989997
- dropout=0.00 spurious=0.20 region=identity_collapse gain_mean=0.026643 exact_mean=0.338889 support_mean=0.365533 coverage_mean=0.957382
- dropout=0.05 spurious=0.00 region=positive_gain gain_mean=0.072222 exact_mean=0.927778 support_mean=1.000000 coverage_mean=1.513623
- dropout=0.05 spurious=0.05 region=positive_gain gain_mean=0.099432 exact_mean=0.888889 support_mean=0.988321 coverage_mean=1.203889
- dropout=0.05 spurious=0.10 region=positive_gain gain_mean=0.076757 exact_mean=0.733333 support_mean=0.810090 coverage_mean=1.056575
- dropout=0.05 spurious=0.15 region=identity_collapse gain_mean=0.076465 exact_mean=0.444445 support_mean=0.520909 coverage_mean=1.000091
- dropout=0.05 spurious=0.20 region=identity_collapse gain_mean=0.044623 exact_mean=0.238889 support_mean=0.283511 coverage_mean=0.972188
- dropout=0.10 spurious=0.00 region=positive_gain gain_mean=0.222222 exact_mean=0.777778 support_mean=1.000000 coverage_mean=1.444094
- dropout=0.10 spurious=0.05 region=positive_gain gain_mean=0.242397 exact_mean=0.744445 support_mean=0.986842 coverage_mean=1.153720
- dropout=0.10 spurious=0.10 region=positive_gain gain_mean=0.156713 exact_mean=0.572222 support_mean=0.728935 coverage_mean=1.028927
- dropout=0.10 spurious=0.15 region=identity_collapse gain_mean=0.038516 exact_mean=0.383333 support_mean=0.421850 coverage_mean=1.004415
- dropout=0.10 spurious=0.20 region=identity_collapse gain_mean=0.091183 exact_mean=0.188889 support_mean=0.280072 coverage_mean=0.981365
- dropout=0.15 spurious=0.00 region=positive_gain gain_mean=0.394444 exact_mean=0.605556 support_mean=1.000000 coverage_mean=1.372770
- dropout=0.15 spurious=0.05 region=positive_gain gain_mean=0.387454 exact_mean=0.583333 support_mean=0.970787 coverage_mean=1.096374
- dropout=0.15 spurious=0.10 region=positive_gain gain_mean=0.294877 exact_mean=0.461111 support_mean=0.755989 coverage_mean=0.999165
- dropout=0.15 spurious=0.15 region=identity_collapse gain_mean=0.116053 exact_mean=0.250000 support_mean=0.366053 coverage_mean=0.977712
- dropout=0.15 spurious=0.20 region=identity_collapse gain_mean=0.070307 exact_mean=0.155555 support_mean=0.225862 coverage_mean=0.977158
- dropout=0.20 spurious=0.00 region=positive_gain gain_mean=0.527778 exact_mean=0.472222 support_mean=1.000000 coverage_mean=1.276431
- dropout=0.20 spurious=0.05 region=positive_gain gain_mean=0.573611 exact_mean=0.405556 support_mean=0.979167 coverage_mean=1.016672
- dropout=0.20 spurious=0.10 region=positive_gain gain_mean=0.404215 exact_mean=0.377778 support_mean=0.781992 coverage_mean=0.931084
- dropout=0.20 spurious=0.15 region=identity_collapse gain_mean=0.191075 exact_mean=0.133333 support_mean=0.324408 coverage_mean=0.946985
- dropout=0.20 spurious=0.20 region=identity_collapse gain_mean=0.086881 exact_mean=0.077778 support_mean=0.164659 coverage_mean=0.972322

#### union_temporal_consensus_pair

- dropout=0.00 spurious=0.00 region=borderline gain_mean=0.000000 exact_mean=1.000000 support_mean=1.000000 coverage_mean=1.000000
- dropout=0.00 spurious=0.05 region=positive_gain gain_mean=0.037061 exact_mean=0.805556 support_mean=0.842617 coverage_mean=0.826835
- dropout=0.00 spurious=0.10 region=identity_collapse gain_mean=0.012075 exact_mean=0.355556 support_mean=0.367631 coverage_mean=0.744057
- dropout=0.00 spurious=0.15 region=undercapture gain_mean=-0.027717 exact_mean=0.183333 support_mean=0.155616 coverage_mean=0.691404
- dropout=0.00 spurious=0.20 region=undercapture gain_mean=-0.006280 exact_mean=0.077778 support_mean=0.071497 coverage_mean=0.653192
- dropout=0.05 spurious=0.00 region=identity_collapse gain_mean=-0.128665 exact_mean=0.888889 support_mean=0.760224 coverage_mean=0.952685
- dropout=0.05 spurious=0.05 region=identity_collapse gain_mean=-0.077500 exact_mean=0.666667 support_mean=0.589167 coverage_mean=0.801390
- dropout=0.05 spurious=0.10 region=identity_collapse gain_mean=-0.064459 exact_mean=0.316667 support_mean=0.252208 coverage_mean=0.728805
- dropout=0.05 spurious=0.15 region=undercapture gain_mean=-0.043632 exact_mean=0.166667 support_mean=0.123035 coverage_mean=0.681981
- dropout=0.05 spurious=0.20 region=undercapture gain_mean=-0.019279 exact_mean=0.055556 support_mean=0.036277 coverage_mean=0.655041
- dropout=0.10 spurious=0.00 region=identity_collapse gain_mean=-0.170052 exact_mean=0.805555 support_mean=0.635504 coverage_mean=0.901781
- dropout=0.10 spurious=0.05 region=identity_collapse gain_mean=-0.068014 exact_mean=0.544444 support_mean=0.476430 coverage_mean=0.765248
- dropout=0.10 spurious=0.10 region=identity_collapse gain_mean=-0.008386 exact_mean=0.188889 support_mean=0.180503 coverage_mean=0.711852
- dropout=0.10 spurious=0.15 region=undercapture gain_mean=-0.042755 exact_mean=0.111111 support_mean=0.068356 coverage_mean=0.678234
- dropout=0.10 spurious=0.20 region=undercapture gain_mean=0.003041 exact_mean=0.027778 support_mean=0.030818 coverage_mean=0.655747
- dropout=0.15 spurious=0.00 region=identity_collapse gain_mean=-0.154707 exact_mean=0.733334 support_mean=0.578626 coverage_mean=0.850752
- dropout=0.15 spurious=0.05 region=identity_collapse gain_mean=-0.084028 exact_mean=0.444445 support_mean=0.360417 coverage_mean=0.736853
- dropout=0.15 spurious=0.10 region=identity_collapse gain_mean=-0.031614 exact_mean=0.155556 support_mean=0.123942 coverage_mean=0.702859
- dropout=0.15 spurious=0.15 region=undercapture gain_mean=-0.017841 exact_mean=0.077778 support_mean=0.059937 coverage_mean=0.675098
- dropout=0.15 spurious=0.20 region=undercapture gain_mean=0.000565 exact_mean=0.022222 support_mean=0.022788 coverage_mean=0.655177
- dropout=0.20 spurious=0.00 region=identity_collapse gain_mean=-0.110519 exact_mean=0.650000 support_mean=0.539480 coverage_mean=0.802226
- dropout=0.20 spurious=0.05 region=identity_collapse gain_mean=-0.024312 exact_mean=0.327778 support_mean=0.303466 coverage_mean=0.708785
- dropout=0.20 spurious=0.10 region=undercapture gain_mean=-0.009049 exact_mean=0.122222 support_mean=0.113173 coverage_mean=0.683133
- dropout=0.20 spurious=0.15 region=undercapture gain_mean=0.026896 exact_mean=0.011111 support_mean=0.038007 coverage_mean=0.658684
- dropout=0.20 spurious=0.20 region=undercapture gain_mean=0.005997 exact_mean=0.016667 support_mean=0.022664 coverage_mean=0.653653

## Interpretation

The useful envelope is the region where exact event recovery degrades before canonical motif support does. Negative gain marks over-entropic identity collapse rather than useful compression.

Hostile unique worlds are expected to remain in hostile collapse across the grid; hostile leak indicates recurrence induced by the detector/decoder rather than by the world.
