from parsers import PMAG_PLUS_handler, Handler, GASTS_handler, GapAdj_handler, MGRA_handler, Procars_handler, infercarspro_handler
import os
import csv


def single_tool_data(tool, path):
    dist = []
    accuracy = []
    test = []
    for test_dir in os.listdir(path):
        if tool == 'PMAG':
            dist.append(PMAG_PLUS_handler.PMAG_PLUS_handler().compare_dist_PMAG(path + '/' + test_dir))
            accuracy.append(PMAG_PLUS_handler.PMAG_PLUS_handler().compare_acc_PMAG(path + '/' + test_dir))
            test.append(test_dir)
        elif tool == 'GASTS':
            dist.append(GASTS_handler.GASTS_handler().compare_dist_GASTS(path + '/' + test_dir))
            accuracy.append(GASTS_handler.GASTS_handler().compare_acc_GASTS(path + '/' + test_dir))
            test.append(test_dir)
        # elif tool == 'GapAdj':
        #     run_GapAdj(path, test_dir)
        # elif tool == 'MGRA':
        #     run_MGRA(path, test_dir)
        elif tool == 'Procars':
            dist.append(Procars_handler.Procars_handler().compare_dist_procars(path + '/' + test_dir))
            accuracy.append(Procars_handler.Procars_handler().compare_acc_procars(path + '/' + test_dir))
            test.append(test_dir)
        elif tool == 'InferCarsPro':
            dist.append(infercarspro_handler.Infercarspro_handler().compare_dist_Infercarspro(path + '/' + test_dir))
            accuracy.append(infercarspro_handler.Infercarspro_handler().compare_acc_Infercarspro(path + '/' + test_dir))
            test.append(test_dir)

    mean_dist = sum(dist)/10
    TP, FN, FP = [], [], []
    print(accuracy)
    for i in accuracy:
        TP.append(i[0])
        FN.append(i[1])
        FP.append(i[2])
    mean_TP = sum(TP)/10
    mean_FN = sum(FN) / 10
    mean_FP = sum(FP) / 10
    mean_acc = [mean_TP, mean_FN, mean_FP]
    return mean_dist, mean_acc

def tool_compare_dist(tool, path):
    param_dirs = []
    dist = []
    for param_dir in os.listdir(path):
        try:
            dist.append(single_tool_data(tool, path + '/' + param_dir)[0])
            param_dirs.append(param_dir)
        except:
            print('not done')
    return(list(zip(param_dirs, dist)))

distances = tool_compare_dist('GASTS', '/home/hamster/noindel-sim')
#distances = single_tool_data('Procars', '/home/hamster/noindel-sim/6_200_100_0')
with open('distances_gasts.csv','w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['name','DCJ distance'])
    for row in distances:
        csv_out.writerow(row)
