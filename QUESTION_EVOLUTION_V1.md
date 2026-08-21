# Question Evolution V1

This file follows only how the question changed. It is not a new taxonomy and does not implement a selection policy.

## P0 → P1

- **P0:** Does Ag75 open a corridor across biocontrol, phosphate solubilization, growth promotion, crops and institutions?
- **Result:** exact patent lookup blocked; OpenAlex returned a specific Ag75 article and exposed Ag109.
- **Sinal:** the exact strain token is a poor patent anchor, while the literature reveals a related strain and UEL–IAP corridor.
- **P1:** Can mechanism/crop/institution terms recover the patent family without treating Ag75 and Ag109 as the same strain?

## P1 → P2

- **P1:** Does the Bacillus velezensis mechanism/crop corridor open a Brazilian family?
- **Result:** 11 patent results, including CMRP 4490 and LABIM22; direct family inspection exposed a stirred-tank bioreactor and bionematicide/inoculant formulation.
- **Sinal:** `CMRP 4490` is a stronger anchor than the broad organism or exact Ag75/Ag109 names.
- **P2:** Does CMRP 4490 connect the biological literature to a process/formulation family, and does the institution recur across neighboring strains?

## P2 → P3

- **P2:** Is CMRP 4490 part of a broader UEL/IAP corridor or only an isolated record?
- **Result:** OpenAlex returned CMRP 4490, CMRP 4489, Ag75 and Ag109 with recurring institutional/author context.
- **Sinal:** the unit of investigation should be a multi-strain institutional corridor, not a single strain.
- **P3:** Do the same UEL team members recur across strains and technologies, does LABIM22 have alternate identifiers, and is there a dated characterization-to-process progression?

## Why the cycle stopped

P3 was preserved as frontier because answering it would require a new scope decision: systematic temporal ordering, deeper author/entity audit or full-text/claim review. The current cycle ended rather than silently expanding its envelope.
