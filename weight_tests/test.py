very_good_weights = [0.75, 1]
weight_list = [0, 0.25, 0.5, 0.75, 1]
good_weights = [0.5, 0.75, 1.0]
bad_weights = [-0.25, 0, 0.25]
very_bad_weights = [-0.25, 0]
very_very_bad_weights = [-0.5, -0.25, 0]

res = [[a, b, c, d, e, f, g, h] for a in good_weights
                                for b in very_bad_weights
                                for c in very_good_weights
                                for d in very_good_weights
                                for e in bad_weights
                                for f in very_very_bad_weights
                                for g in weight_list
                                for h in bad_weights]

weights_file = open("combinations2.txt", "w")
for idx in range(0, len(res)):
    weights_file.write(str(res[idx]) + "\n")
weights_file.close()