from parsers import PMAG_PLUS_handler, GASTS_handler, GapAdj_handler, MGRA_handler, Procars_handler, infercarspro_handler, Rococo_handler
import csv
import os


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
        elif tool == 'GapAdj':
            dist.append(GapAdj_handler.GapAdj_handler().compare_dist_GapAdj(path + '/' + test_dir))
            accuracy.append(GapAdj_handler.GapAdj_handler().compare_acc_GapAdj(path + '/' + test_dir))
            test.append(test_dir)
        elif tool == 'MGRA':
            dist.append(MGRA_handler.MGRA_handler().compare_dist_MGRA(path + '/' + test_dir))
            accuracy.append(MGRA_handler.MGRA_handler().compare_acc_MGRA(path + '/' + test_dir))
            test.append(test_dir)
        elif tool == 'Procars':
            dist.append(Procars_handler.Procars_handler().compare_dist_procars(path + '/' + test_dir))
            accuracy.append(Procars_handler.Procars_handler().compare_acc_procars(path + '/' + test_dir))
            test.append(test_dir)
        elif tool == 'InferCarsPro':
            dist.append(infercarspro_handler.Infercarspro_handler().compare_dist_Infercarspro(path + '/' + test_dir))
            accuracy.append(infercarspro_handler.Infercarspro_handler().compare_acc_Infercarspro(path + '/' + test_dir))
            test.append(test_dir)
        elif tool == 'Rococo':
            dist.append(Rococo_handler.Rococo_handler().compare_dist_rococo(path + '/' + test_dir))
            accuracy.append(Rococo_handler.Rococo_handler().compare_acc_rococo(path + '/' + test_dir))
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
            dist.append('not done')
            param_dirs.append(param_dir)
    return dist, param_dirs


def tool_compare_acc(tool, path):
    param_dirs = []
    acc = {}
    acc['TP'] = []
    acc['FN'] = []
    acc['FP'] = []
    for param_dir in os.listdir(path):
        try:
            acc['TP'].append(single_tool_data(tool, path + '/' + param_dir)[1][0])
            acc['FN'].append(single_tool_data(tool, path + '/' + param_dir)[1][1])
            acc['FP'].append(single_tool_data(tool, path + '/' + param_dir)[1][2])
            param_dirs.append(param_dir)
        except:
            acc['TP'].append('not done')
            acc['FN'].append('not done')
            acc['FP'].append('not done')
            param_dirs.append(param_dir)
    return acc, param_dirs


def tools_compare_acc(tools, path):
    param_dirs = []
    tool_acc = {}
    tool_acc['TP'] = {}
    tool_acc['FN'] = {}
    tool_acc['FP'] = {}
    for tool in tools:
        tool_acc['TP'][tool] = tool_compare_acc(tool, path)[0]['TP']
        tool_acc['FN'][tool] = tool_compare_acc(tool, path)[0]['FN']
        tool_acc['FP'][tool] = tool_compare_acc(tool, path)[0]['FP']
        param_dirs = tool_compare_dist(tool, path)[1]
    return param_dirs, tool_acc


def tools_compare_dist(tools, path):
    tool_dist = {}
    for tool in tools:
        tool_dist[tool] = tool_compare_dist(tool, path)
    return tool_dist


def create_acc_table(tools, path, result_path):
    accuracies = tools_compare_acc(tools, path)
    with open(result_path, 'w') as out:
        csv_out = csv.writer(out)
        header = [' ']
        for i in accuracies[0]:
            header.append(i)
        csv_out.writerow(header)
        for tool in accuracies[1]['TP']:
            csv_out.writerow(tool)
            row = ['TP']
            for i in accuracies[1]['TP'][tool]:
                row.append(i)
            csv_out.writerow(row)
            row = ['FN']
            for i in accuracies[1]['FN'][tool]:
                row.append(i)
            csv_out.writerow(row)
            row = ['FP']
            for i in accuracies[1]['FP'][tool]:
                row.append(i)
            csv_out.writerow(row)


def create_dist_table(tools, path, result_path):
    distances = tools_compare_dist(tools, path)
    with open(result_path, 'w') as out:
        csv_out = csv.writer(out)
        header = [' ']
        for i in distances:
            for j in distances[i][1]:
                header.append(j)
        csv_out.writerow(header)
        for tool in distances:
            row = [tool]
            for i in distances[tool][0]:
                row.append(i)
            csv_out.writerow(row)






