# -*- coding: utf-8 -*-

from reorder_multiple_drafts import random_seq, alignment_window, get_kmers, remove_reference, align_concat_len, len_cumsum, find_2d_idx
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from random import randint
import itertools


##############################################################################
# REMOVE REFERENCE TESTS
##############################################################################
a,b,c = 10,15,20
reference = 'reference'
not_reference = 'something else'

alignments = [[SeqRecord(Seq(random_seq(a)), id=reference)],
              [SeqRecord(Seq(random_seq(b)), id=reference),
               SeqRecord(Seq(random_seq(b)), id=not_reference),
               SeqRecord(Seq(random_seq(b)), id=reference)],
              [SeqRecord(Seq(random_seq(c)), id=not_reference)]]

new_alignments = remove_reference(alignments, reference)

assert align_concat_len(new_alignments) == a+b+c, "Reference record not removed successfully!"

##############################################################################
# CONCATENATED LENGTH TESTS
##############################################################################

for i in range(1,20): # Length of alignment
    for j in range(1,20): # Num sequences
        for k in range(1,20): # Num alignments
            alignments = [[Seq(random_seq(i)) for _ in range(j)] for __ in range(k)]
            assert align_concat_len(alignments) == i*k, "Concatenated alignment length incorrect."

##############################################################################
# WINDOW TESTS
##############################################################################

for max_size in range(25,30):
    num_alignments = randint(1,max_size)
    alignments = []
    
    for _ in range(num_alignments):
        seq_len = randint(1,max_size)
        num_seqs = randint(1,max_size)
        alignment = [Seq(random_seq(seq_len)) for _ in range(num_seqs)]
        alignments.append(alignment)
    
    alignment_len = align_concat_len(alignments)
    
    for window_size in range(2,int(alignment_len/2)):
        for stagger in range(int(window_size/2), window_size):
            windows = alignment_window(window_size, stagger, alignments)
            assert alignment_len <= len(windows)*stagger <= alignment_len + window_size, "Alignment and window lengths do not match!"

    ##############################################################################
    # LEN CUMULATIVE SUM
    ##############################################################################
    
    assert len_cumsum(alignments) == list(itertools.accumulate(map(len, (e[0] for e in alignments)))), "Cumsum lengths of alignments not accurate."
    

##############################################################################
# GET_KMERS TESTS
##############################################################################

seq1 = Seq('abcde')
seq2 = Seq('a-b-c-d-e')
seq3 = Seq('-----')
k=3

assert get_kmers(k,seq1,upper=False) == ['abc','bcd','cde'], "Issue with capitalisation!"
assert get_kmers(k,seq1) == ['ABC','BCD','CDE'], "Wrong kmers returned!"
assert get_kmers(k,seq2) == ['ABC','BCD','CDE'], "Does not remove gaps correctly!"
assert get_kmers(k,seq3) == [], "Does not remove gaps correctly!"

for n in range(1,1000):
    assert len(get_kmers(k,Seq(random_seq(n)))) == max(0,n-k+1), "Wrong number of kmers generated!"

##############################################################################
# FIND INDEX TESTS
##############################################################################

alignments = [['abc','aaa','bbb'],['de'],['fghijkl'],['mnop','qrst']]
indices = [0,1,3,8,10,15]
indices_2d = [(0,0),(0,1),(1,0),(2,3),(2,5),(3,3)]
cumsum = len_cumsum(alignments)

assert [find_2d_idx(cumsum, i) for i in indices] == indices_2d, "Incorrect 2d indices returned!"
