very_good_weights = [0.75, 1]
weight_list = [0, 0.25, 0.5, 0.75, 1]
good_weights = [0.5, 0.75, 1.0]
bad_weights = [-0.25, 0, 0.25]
very_bad_weights = [-0.25, 0]
very_very_bad_weights = [-0.5, -0.25, 0]

# res = [[a, b, c, d, e, f, g, h] for a in good_weights
#                                 for b in very_bad_weights
#                                 for c in very_good_weights
#                                 for d in very_good_weights
#                                 for e in bad_weights
#                                 for f in very_very_bad_weights
#                                 for g in bad_weights
#                                 for h in bad_weights]

# Test for good, bad, and unrelated
# wide_range = [-1.0, -0.5, 0, 0.5, 1.0]
# bad_range = [-1.0, -0.5, 0]
# good_range = [0.5, 1.0]
# not_relevant = [0]
# res = [[a, b, c, d, e, f, g, h] for a in wide_range
#                                 for b in bad_range
#                                 for c in wide_range
#                                 for d in good_range
#                                 for e in wide_range
#                                 for f in bad_range
#                                 for g in bad_range
#                                 for h in not_relevant]

initial = [-1.0, 0, 1.0]
res = [[a, b, c, d, e, f, g, h] for a in initial
                                for b in initial
                                for c in initial
                                for d in initial
                                for e in initial
                                for f in initial
                                for g in initial
                                for h in initial]

weights_file = open("combinations.txt", "w")
for idx in range(0, len(res)):
    weights_file.write(str(res[idx]) + "\n")
weights_file.close()