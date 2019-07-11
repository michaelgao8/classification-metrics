import pandas as pd 
import numpy as np
from sklearn.utils import resample
from sklearn.metrics import roc_auc_score, roc_curve, precision_recall_curve, average_precision_score
from sklearn.calibration import calibration_curve
import argparse
import json

parser = argparse.ArgumentParser(description = 'Generates data for metric plots')
parser.add_argument('-i', '--input-file', action = "store", help = 'path to the input results file')
parser.add_argument('-o', '--output-dir', action = "store", help = 'path to put plot data', default = './data/') #TODO: Can probably be smarter
parser.add_argument('-n', '--num-boots', type=int, action = "store", help = 'select the number of bootstrap samples to take. Default 500', default = 500)
parser.add_argument('-v', '--verbose', action = "store_true", help = 'print out progress and helpful statements', default = False)

if __name__ == '__main__':
    DEV = False # Flag

    if DEV:
        class fakeArgs():
            def __init__(self):
                self.input_file = '../data/test.csv'
                self.output_dir = '../data/'
                self.num_boots = 100
                self.verbose = True
        args = fakeArgs()
    else:
        args = parser.parse_args()

    output_df = pd.read_csv(args.input_file)
    # To make things easier...
    output_df = output_df.sort_values(output_df.columns[1], ascending = False)
    # By specification, the first column should be the y_true 
    # and the second column should be y_pred
    # This should be covered by the user, but may be helpful to raise
    assert all(output_df.iloc[:, 0].isin([0, 1])), 'The first column of the results must be the outcome. Values other than 0 or 1 detected'
    y_true = output_df.iloc[:, 0].values
    y_pred = output_df.iloc[:, 1].values

    # Receiver Operating Characteristic =======================================
    auroc = roc_auc_score(y_true, y_pred)
    fpr, tpr, thresholds = roc_curve(y_true, y_pred)
    auc_final = {'auc': auroc, 
                'fpr': list(fpr),
                'tpr': list(tpr),
                'thresholds': list(thresholds)
    }

    # Precision Recall
    avg_precision = average_precision_score(y_true, y_pred)
    precision, recall, thresholds = precision_recall_curve(y_true, y_pred)
    avg_precision_final = {'avg_precision': avg_precision,
                        'precision': list(precision),
                        'recall': list(recall),
                        'thresholds': list(thresholds)
    }

    # Bootstrapping ===========================================================
    auc_bootstrap_list = []
    pid_bootstrap_list = []
    avg_prec_bootstrap_list = []

    for i in range(args.num_boots):
        y_true_resampled, y_pred_resampled = resample(y_true, y_pred)
        
        car=0
        #roc_auc_score sends error if there is only one class present in y_true, just make sure that random sample has at
        #least one 1 and at least one 0
        if ((0 in y_true_resampled) == False):
            car=1
            continue
        if ((1 in y_true_resampled) == False):
            car=1
            continue


        # ROC
        auc_temp = roc_auc_score(y_true_resampled, y_pred_resampled)
        auc_bootstrap_list.append(auc_temp)

        # Avg_precision
        avg_prec_temp = average_precision_score(y_true_resampled, y_pred_resampled)
        avg_prec_bootstrap_list.append(avg_prec_temp)

        # PID
        deciles = np.quantile(y_pred_resampled, np.linspace(1, .1, 10))
        for j in range(10):
            print(car)
            if j != 9:
                proportion_positive = y_true_resampled[(y_pred_resampled <= deciles[j])
                            & (y_pred_resampled > deciles[j+1])].mean()
            else: 
                proportion_positive = y_true_resampled[y_pred_resampled <= deciles[9]].mean()

            pid_bootstrap_list.append(proportion_positive)


    # Update AUC
    auc_ci_bounds = np.quantile(auc_bootstrap_list, [0.025, 0.975])
    auc_final.update({'auc_lower_bound': auc_ci_bounds[0], 
                      'auc_upper_bound': auc_ci_bounds[1]})
    
    avg_prec_ci_bounds = np.quantile(avg_prec_bootstrap_list, [0.025, 0.975])
    avg_precision_final.update({'avg_precision_lower_bound': avg_prec_ci_bounds[0],
                                'avg_precision_upper_bound': avg_prec_ci_bounds[1]})

    # Update PID
    pid_final = {'decile_midpoint': list(np.linspace(0.95, 0.05, 10)) * args.num_boots,
                'pid': pid_bootstrap_list}

    # TODO: Add bootstrapped version of ROC curve

    # Precision @ k
    precision_k = []

    cutpoints = np.quantile(y_pred, np.linspace(1, 0.01, 100))
    for i in range(len(cutpoints)):
            y_true_temp = y_true[y_pred >= cutpoints[i]]
            precision_k.append(y_true_temp.mean())

    precision_at_k_final = {'precision_at_k': precision_k,
                            'cutpoints': list(np.linspace(0.01, 1, 100))}
    
    # Calibration ===================================================
    prob_true, prob_pred = calibration_curve(y_true, y_pred, n_bins = 10)

    calibration_final = {'prob_true': list(prob_true),
                        'prob_pred': list(prob_pred)}
    
    final_dict = {
        'ROC': auc_final,
        'avg_precision': avg_precision_final,
        'pid': pid_final,
        'precision_at_k': precision_at_k_final,
        'calibration': calibration_final
    }

    with open(args.output_dir + 'plot_data.json', 'w') as f:
        json.dump(final_dict, f, indent = 2)




